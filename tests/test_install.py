import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install.py')
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop('HERDR_APP_HOME', None)
        self.app = self.home / '.config/herdr-app'

    def run_install(self, apply):
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.install(self.home, apply)

    def test_preview_writes_nothing(self):
        self.assertIsNone(self.run_install(False))
        self.assertEqual(list(self.home.iterdir()), [])

    def test_install_merges_without_dropping_user_settings(self):
        pi = self.home / '.pi/agent/settings.json'
        pi.parent.mkdir(parents=True)
        pi_original = '{"theme":"system","defaultModel":"keep-me"}'
        pi.write_text(pi_original)
        self.app.mkdir(parents=True)
        (self.app / 'settings.json').write_text('{"zoom":1.2,"sounds":{"enabled":true,"done":"x.mp3"}}')
        (self.app / 'keys.json').write_text('{"global":{"cmd-w":"tab.close","cmd-q":"app.quit"},"terminal":{"cmd-c":"terminal.copy"}}')
        backup = self.run_install(True)

        self.assertEqual(json.loads(pi.read_text()), {'theme': 'dr-pepper', 'defaultModel': 'keep-me'})
        settings = json.loads((self.app / 'settings.json').read_text())
        self.assertEqual(settings['zoom'], 1.2)
        self.assertEqual(settings['theme'], 'dr-pepper')
        self.assertEqual(settings['sounds'], {'enabled': False, 'done': 'x.mp3'})
        keys = json.loads((self.app / 'keys.json').read_text())
        self.assertEqual(keys['global']['cmd-w'], 'pane.close')
        self.assertEqual(keys['global']['cmd-q'], 'app.quit')
        self.assertEqual(keys['terminal'], {'cmd-c': 'terminal.copy'})

        manifest = {m['destination']: m['original'] for m in json.loads((backup / 'manifest.json').read_text())}
        self.assertEqual(Path(manifest[str(pi)]).read_text(), pi_original)
        for source, dest in installer.plan(self.home):
            self.assertEqual(source.read_bytes(), dest.read_bytes())
        self.assertNotEqual(self.run_install(True), backup)

    def test_herdr_app_home_override(self):
        other = self.home / 'elsewhere'
        os.environ['HERDR_APP_HOME'] = str(other)
        self.run_install(True)
        self.assertTrue((other / 'themes/dr-pepper.json').is_file())
        self.assertFalse(self.app.exists())

    def test_invalid_json_fails_before_copying(self):
        self.app.mkdir(parents=True)
        (self.app / 'keys.json').write_text('[]')
        with self.assertRaises(ValueError):
            self.run_install(True)
        self.assertFalse((self.home / 'Library').exists())
        self.assertFalse((self.app / 'themes').exists())

    def test_symlinks_are_refused(self):
        dest = installer.plan(self.home)[0][1]
        dest.parent.mkdir(parents=True)
        original = self.home / 'dotfile'
        original.write_text('unchanged')
        dest.symlink_to(original)
        with self.assertRaises(ValueError):
            self.run_install(True)
        self.assertEqual(original.read_text(), 'unchanged')


if __name__ == '__main__':
    unittest.main()
