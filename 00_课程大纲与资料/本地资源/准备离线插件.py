#!/usr/bin/env python3
"""Copy the fixed Linux/Python 3.12 wheel set and build a local package index."""
import argparse
import html
from pathlib import Path
import re
import shutil

base = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('docker_directory', type=Path)
args = parser.parse_args()
source = base / '下载文件/04_服务器依赖/Tongyi_Python312'
target = args.docker_directory / 'course-wheels'
wheels = sorted(source.glob('*.whl'))
if len(wheels) != 62:
    parser.exit(1, '需要资源清单中的62个wheel文件，请先执行资源校验。\n')
if target.exists():
    parser.exit(1, '目标已存在，保留原目录。无需重复准备：' + str(target) + '\n')
shutil.copytree(source, target)
for wheel in wheels:
    package = re.sub(r'[-_.]+', '-', wheel.name.split('-')[0]).lower()
    folder = target / 'simple' / package
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / 'index.html').open('a', encoding='utf-8') as index:
        index.write('<a href="../../' + html.escape(wheel.name, quote=True) + '">' + html.escape(wheel.name) + '</a>\n')
print('已准备62个依赖及本地索引：', target)
