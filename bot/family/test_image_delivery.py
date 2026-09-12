import hashlib
import io
import json
import tempfile
import time
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import bots
import image_delivery as images
from family_runtime import GroupTelegram


class ImageDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {'state_dir': self.temp.name, 'black_delivery_format': 'photo'}
        self.store = bots.Store(Path(self.temp.name) / 'test.sqlite3')
        self.day = '2026-09-13'
        self.key = 'black:' + self.day + ':news'
        self.data = {'date': self.day, 'sections': [{'labelKr': '기술', 'cards': [{'title': '제목', 'summary': '본문'}]}]}
        self.folder = images.image_folder(self.config)
        self.files = []
        for i in range(1, 7):
            path = self.folder / f'{self.day}-news-{i}.png'
            path.write_bytes(b'\x89PNG\r\n\x1a\n' + b'x' * 100)
            self.files.append({'name': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def test_album_caption_and_restart_duplicate_prevention(self):
        with patch.object(images, 'request_json', return_value=self.data), patch.object(images, 'render', return_value=self.files), patch.object(images, 'send_album', return_value={'message_ids': [1]}) as send:
            self.assertTrue(images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key))
            self.assertEqual(send.call_args.args[2], '🖤 오늘의 뉴스')
            self.assertEqual(len(send.call_args.args[1]), 6)
            self.store.db.close()
            self.store = bots.Store(Path(self.temp.name) / 'test.sqlite3')
            self.assertTrue(images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key))
            self.assertEqual(send.call_count, 1)

    def test_uncertain_album_never_retries(self):
        with patch.object(images, 'request_json', return_value=self.data), patch.object(images, 'render', return_value=self.files), patch.object(images, 'send_album', side_effect=bots.ServiceError()) as send:
            with self.assertRaises(bots.ServiceError):
                images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key)
            with self.assertRaises(RuntimeError):
                images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key)
            self.assertEqual(send.call_count, 1)

    def test_explicit_rejection_retries_using_saved_source(self):
        with patch.object(images, 'request_json', return_value=self.data) as fetch, patch.object(images, 'render', return_value=self.files) as render, patch.object(images, 'send_album', side_effect=[bots.ServiceError(429), {}]) as send:
            with self.assertRaises(bots.ServiceError):
                images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key)
            self.assertTrue(images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key))
            self.assertEqual(fetch.call_count, 1)
            self.assertEqual(render.call_count, 1)
            self.assertEqual(send.call_count, 2)

    def test_wrong_edition_does_not_render_or_send(self):
        with patch.object(images, 'request_json', return_value={'date': '2020-01-01'}), patch.object(images, 'render') as render:
            self.assertFalse(images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key))
            render.assert_not_called()

    def test_legacy_partial_delivery_blocks_photo(self):
        self.store.put('delivery:' + self.key + ':0', 'sent')
        with patch.object(images, 'send_album') as send:
            with self.assertRaises(RuntimeError):
                images.deliver(self.config, self.store, Mock(), 'news', self.day, self.key)
            send.assert_not_called()

    def test_cleanup_preserves_recent_png_and_nonimages_and_symlinks(self):
        recent = self.folder / self.files[0]['name']
        sentinel = self.folder / 'config.json'
        sentinel.write_text('{}')
        fake = self.folder / '2026-01-01-news-1.png'
        fake.write_bytes(b'not an image')
        link = self.folder / '2026-01-01-news-2.png'
        link.symlink_to(recent)
        self.assertEqual(images.cleanup_images(self.config), 0)
        self.assertEqual(images.cleanup_images(self.config, time.time() + 72 * 3600 + 1), 6)
        self.assertTrue(sentinel.exists())
        self.assertTrue(fake.exists())
        self.assertTrue(link.is_symlink())
        self.assertTrue((Path(self.temp.name) / 'test.sqlite3').exists())

    def test_schedule_keeps_hours_deadlines_and_no_text_fallback(self):
        transport = Mock()
        with patch.object(images, 'deliver', return_value=False) as deliver:
            for hour, minute in [(8, 59), (11, 0), (15, 0)]:
                bots.black_tick(self.store, transport, datetime(2026, 9, 13, hour, minute, tzinfo=bots.KST), self.config)
            deliver.assert_not_called()
            bots.black_tick(self.store, transport, datetime(2026, 9, 13, 9, tzinfo=bots.KST), self.config)
            self.assertEqual(deliver.call_args.args[3], 'news')
            bots.black_tick(self.store, transport, datetime(2026, 9, 13, 12, tzinfo=bots.KST), self.config)
            self.assertEqual(deliver.call_args.args[3], 'knowledge')
            transport.send.assert_not_called()
        with patch.object(images, 'deliver', side_effect=RuntimeError('render failed')):
            bots.black_tick(self.store, transport, datetime(2026, 9, 13, 12, 5, tzinfo=bots.KST), self.config)
            transport.send.assert_not_called()

    def test_successful_existing_day_is_not_resent(self):
        self.store.put(self.key, True)
        with patch.object(images, 'deliver') as deliver:
            bots.black_tick(self.store, Mock(), datetime(2026, 9, 13, 9, tzinfo=bots.KST), self.config)
            deliver.assert_not_called()

    def test_album_uses_fixed_transport_destination_and_one_caption(self):
        for transport, target in [(bots.Telegram('test', 123), 123), (GroupTelegram('test', 123, -99), -99)]:
            result = {'ok': True, 'result': [{'chat': {'id': target}, 'media_group_id': 'group', 'message_id': i,
                                            'photo': [{'width': 100, 'height': 100, 'file_size': 100}]} for i in range(3)]}
            with patch('urllib.request.urlopen', return_value=io.BytesIO(json.dumps(result).encode())) as call:
                receipt = images.send_album(transport, [self.folder / f['name'] for f in self.files[:3]], '🖤 오늘의 지식 더하기')
                body = call.call_args.args[0].data.decode(errors='replace')
                self.assertIn('\r\n\r\n' + str(target) + '\r\n', body)
                self.assertEqual(body.count('caption'), 1)
                self.assertEqual(len(receipt['message_ids']), 3)


if __name__ == '__main__':
    unittest.main()
