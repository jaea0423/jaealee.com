"""실행 설정을 생성합니다. 시작 명령은 표시만 하고 자동 실행하지 않습니다."""
import argparse
import os
import plistlib
import shlex
import sys
from pathlib import Path


def make_plist(role, config, python, script, logs):
    return {'Label': 'com.jaealee.family.' + role,
            'ProgramArguments': [str(python), '-u', str(script), role, '--config', str(config)],
            'RunAtLoad': True, 'KeepAlive': True, 'ThrottleInterval': 60,
            'StandardOutPath': str(logs / (role + '.log')),
            'StandardErrorPath': str(logs / (role + '.error.log'))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--role', choices=['white', 'black'], required=True)
    args = parser.parse_args()
    if sys.platform != 'darwin':
        raise RuntimeError('이 도구는 아이맥에서 실행하세요.')
    config = Path(args.config).expanduser().resolve(strict=True)
    logs = Path.home() / 'Library/Logs/jaealee-family-bots'
    logs.mkdir(parents=True, exist_ok=True)
    logs.chmod(0o700)
    folder = Path.home() / 'Library/LaunchAgents'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / ('com.jaealee.family.' + args.role + '.plist')
    content = make_plist(args.role, config, sys.executable, Path(__file__).resolve().with_name('bots.py'), logs)
    # 기존 서비스를 덮어쓰지 않아 중복 실행·설정 유실을 막습니다.
    with target.open('xb') as output:
        plistlib.dump(content, output)
    target.chmod(0o600)
    domain = 'gui/' + str(os.getuid())
    print('설정 파일 생성 완료. 개인방 시험 통과 후 시작:\nlaunchctl bootstrap ' + domain + ' ' + shlex.quote(str(target)))
    print('중지:\nlaunchctl bootout ' + domain + ' ' + shlex.quote(str(target)))


if __name__ == '__main__':
    main()
