"""기존 원고를 실제 발송 없이 변환해 봅니다."""
import json
import sys
from pathlib import Path
from bots import digest

root = Path(sys.argv[1])
day = sys.argv[2]
for kind in ('news', 'knowledge'):
    data = json.loads((root / kind / 'data' / (day + '.json')).read_text(encoding='utf-8'))
    messages = digest(kind, data)
    assert len(messages) > 1
    assert all('https://' not in text and 'http://' not in text for text in messages)
    assert all(len(text.encode('utf-16-le')) // 2 <= 4096 for text in messages)
    print(kind, len(messages), 'messages; length and URL exclusion OK')
