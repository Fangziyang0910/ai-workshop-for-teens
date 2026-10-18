#!/usr/bin/env python3
"""Download or verify official course files using the committed SHA-256 manifest."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parent


def destination(base, relative):
    target = (base / relative).resolve()
    if target == base.resolve() or base.resolve() not in target.parents:
        raise ValueError('资源路径超出本目录：' + relative)
    return target


def matches(path, row):
    if not path.is_file() or path.stat().st_size != row['bytes']:
        return False
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest() == row['sha256']


def process(row, download=False):
    path = destination(BASE, row['path'])
    if matches(path, row):
        return True, '完整：' + row['name']
    if not download:
        return False, '缺失或校验不符：' + row['path']
    if urlsplit(row['url']).scheme != 'https':
        return False, '下载源必须使用HTTPS：' + row['name']
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + '.part')
    try:
        subprocess.run(['curl', '--fail', '--location', '--proto', '=https', '--proto-redir', '=https', '--retry', '3', '--connect-timeout', '20', '--output', str(partial), row['url']], check=True)
        if not matches(partial, row):
            return False, '来源内容已变化或下载不完整，保留.part供检查，未覆盖原文件：' + row['name']
        partial.replace(path)
        return True, '已下载并校验：' + row['name']
    except (OSError, subprocess.CalledProcessError) as error:
        return False, '下载失败：' + row['name'] + '；' + str(error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['verify', 'download'])
    parser.add_argument('--category', choices=['all', 'core', 'server', 'docs'], default='all')
    args = parser.parse_args()
    manifest = json.loads((BASE / '资源清单.json').read_text(encoding='utf-8'))
    rows = [row for row in manifest['files'] if args.category == 'all' or row['category'] == args.category]
    if args.action == 'verify' and args.category in ('all', 'server'):
        images = json.loads((BASE / '镜像清单.json').read_text(encoding='utf-8'))
        if 'archive' in images:
            rows.append(images['archive'])
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda row: process(row, args.action == 'download'), rows))
    for ok, message in results:
        print(message)
    failures = sum(not ok for ok, _ in results)
    print('文件数：{}；通过：{}；未通过：{}'.format(len(rows), len(rows) - failures, failures))
    print('镜像恢复使用取回服务器镜像.py；本命令不启动服务。')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
