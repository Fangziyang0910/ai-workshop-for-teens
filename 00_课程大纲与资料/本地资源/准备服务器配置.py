#!/usr/bin/env python3
"""Create credentials for a fresh Dify 1.17.1 instance. Never overwrite .env."""
import argparse
import os
import re
from pathlib import Path
import secrets
from urllib.parse import urlsplit


def prepare(folder, address):
    if not re.fullmatch(r'https?://[A-Za-z0-9.-]+(?::[0-9]{1,5})?/?', address):
        raise ValueError('入口只能包含协议、域名或IPv4地址、端口；不能含空白或配置表达式')
    url = urlsplit(address)
    if url.port is not None and not 1 <= url.port <= 65535:
        raise ValueError('端口范围为1～65535')
    if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password or url.query or url.fragment or url.path not in ('', '/'):
        raise ValueError('入口必须是完整的HTTP(S)地址，不带账号、路径或参数')
    if url.scheme == 'http' and url.hostname not in ('localhost', '127.0.0.1'):
        raise ValueError('HTTP只用于本机演练；学校入口请使用HTTPS')
    address = address.rstrip('/')
    template = folder / '.env.example'
    target = folder / '.env'
    text = template.read_text(encoding='utf-8')
    values = {}
    for line in text.splitlines():
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            values[key] = value
    for key in ('SECRET_KEY', 'DB_PASSWORD', 'REDIS_PASSWORD', 'PLUGIN_DAEMON_KEY', 'INNER_API_KEY_FOR_PLUGIN', 'SANDBOX_API_KEY', 'WEAVIATE_API_KEY', 'DIFY_AGENT_API_TOKEN', 'DIFY_AGENT_LOCAL_SANDBOX_AUTH_TOKEN', 'DIFY_AGENT_SERVER_SECRET_KEY'):
        values[key] = secrets.token_hex(32)
    values.update(
        CELERY_BROKER_URL='redis://:' + values['REDIS_PASSWORD'] + '@redis:6379/1',
        CODE_EXECUTION_API_KEY=values['SANDBOX_API_KEY'],
        PLUGIN_DIFY_INNER_API_KEY=values['INNER_API_KEY_FOR_PLUGIN'],
        WEAVIATE_AUTHENTICATION_APIKEY_ALLOWED_KEYS=values['WEAVIATE_API_KEY'],
        WEAVIATE_AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED='false',
        WEAVIATE_DISABLE_TELEMETRY='true',
        LOG_TZ='Asia/Shanghai',
        ALLOW_REGISTER='false',
        ALLOW_CREATE_WORKSPACE='false',
        NEXT_PUBLIC_SOCKET_URL=('wss://' if url.scheme == 'https' else 'ws://') + url.netloc,
        NEXT_PUBLIC_ENABLE_AGENT_V2='false',
        EXPOSE_NGINX_PORT='127.0.0.1:18080',
        EXPOSE_NGINX_SSL_PORT='127.0.0.1:18443',
        EXPOSE_PLUGIN_DEBUGGING_PORT='15003',
        PLUGIN_PYTHON_ENV_INIT_TIMEOUT='600',
        PIP_MIRROR_URL='file:///opt/course-wheels/simple',
    )
    for key in ('CONSOLE_API_URL', 'CONSOLE_WEB_URL', 'SERVICE_API_URL', 'APP_API_URL', 'APP_WEB_URL', 'FILES_URL', 'TRIGGER_URL'):
        values[key] = address
    values['ENDPOINT_URL_TEMPLATE'] = address + '/e/{hook_id}'
    # Exclusive creation prevents destroying a running instance's encryption keys.
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as output:
        output.write('# Private course configuration. Do not commit or distribute.\n')
        output.write('\n'.join(key + '=' + value for key, value in values.items()) + '\n')
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docker_directory', type=Path)
    parser.add_argument('--url', default='http://localhost:18080')
    args = parser.parse_args()
    try:
        result = prepare(args.docker_directory, args.url)
        print('已创建私有配置：', result, '；未输出任何密钥。')
    except (OSError, ValueError) as error:
        parser.exit(1, '未创建配置：' + str(error) + '\n')
