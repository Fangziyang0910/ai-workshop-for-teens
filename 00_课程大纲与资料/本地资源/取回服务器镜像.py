#!/usr/bin/env python3
"""Fetch official images by digest, restore course tags and export an offline tar."""
import argparse
import json
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mirror', action='store_true', help='使用DaoCloud公共镜像缓存；仍按官方源摘要校验')
args = parser.parse_args()
manifest = json.loads((base / '镜像清单.json').read_text(encoding='utf-8'))
target = base / '下载文件/04_服务器依赖/dify-course-images.tar'
partial = target.with_name(target.name + '.part')
target.parent.mkdir(parents=True, exist_ok=True)
for row in manifest['images']:
    ref = ('m.daocloud.io/' if args.mirror else '') + row['source']
    subprocess.run(['docker', 'pull', '--platform', manifest['platform'], ref], check=True)
    subprocess.run(['docker', 'tag', ref, row['name']], check=True)
    actual = json.loads(subprocess.check_output(['docker', 'image', 'inspect', row['name']]))[0]
    if actual['Id'] != row['image_id']:
        raise RuntimeError('镜像内容与清单不符：' + row['name'])
subprocess.run(['docker', 'save', '--output', str(partial)] + [row['name'] for row in manifest['images']], check=True)
partial.replace(target)
print('镜像已按官方摘要取得并导出：', target)
print('重建tar的字节排列可能与首次留存不同；核对镜像摘要后重新记录本地包SHA-256。')
