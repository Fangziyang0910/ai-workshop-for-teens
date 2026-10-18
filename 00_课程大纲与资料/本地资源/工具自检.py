#!/usr/bin/env python3
"""Check configuration safety without starting services or calling a model."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

folder = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('course_config', folder / '准备服务器配置.py')
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


class ConfigurationTests(unittest.TestCase):
    def test_credentials_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / '.env.example').write_text('DB_PASSWORD=old\n', encoding='utf-8')
            target = config.prepare(root, 'http://localhost:18080')
            data = dict(line.split('=', 1) for line in target.read_text().splitlines() if '=' in line)
            self.assertNotEqual(data['DB_PASSWORD'], 'old')
            self.assertEqual(data['PLUGIN_DIFY_INNER_API_KEY'], data['INNER_API_KEY_FOR_PLUGIN'])
            self.assertEqual(data['SANDBOX_API_KEY'], data['CODE_EXECUTION_API_KEY'])
            self.assertIn(data['REDIS_PASSWORD'], data['CELERY_BROKER_URL'])
            original = target.read_bytes()
            with self.assertRaises(FileExistsError):
                config.prepare(root, 'http://localhost:18080')
            self.assertEqual(target.read_bytes(), original)

    def test_bad_urls(self):
        for value in ['http://school.example', 'https://user:password@school.example', 'https://school.example/path', 'https://school.example\nX=1', 'https://school.example:99999', 'https://${SECRET_KEY}']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                config.prepare(Path('/does-not-exist'), value)


resource_spec = importlib.util.spec_from_file_location('resources', folder / '资源管理.py')
resources = importlib.util.module_from_spec(resource_spec)
resource_spec.loader.exec_module(resources)


class ResourceTests(unittest.TestCase):
    def test_path_boundary(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            self.assertEqual(resources.destination(base, 'cache/file'), base / 'cache/file')
            for value in ['../outside', '/tmp/outside']:
                with self.assertRaises(ValueError):
                    resources.destination(base, value)

    def test_corruption_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'file'
            row = {'bytes': 3, 'sha256': hashlib.sha256(b'abc').hexdigest()}
            self.assertFalse(resources.matches(path, row))
            path.write_bytes(b'abc')
            self.assertTrue(resources.matches(path, row))
            path.write_bytes(b'abd')
            self.assertFalse(resources.matches(path, row))


if __name__ == '__main__':
    unittest.main()
