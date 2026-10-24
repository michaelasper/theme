import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install.py')
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def run_install(self, apply):
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.install(self.home, apply)

    def test_preview_writes_nothing(self):
        self.assertIsNone(self.run_install(False))
        self.assertEqual(list(self.home.iterdir()), [])

    def test_install_preserves_settings_and_backs_up(self):
        settings = self.home / '.pi/agent/settings.json'
        settings.parent.mkdir(parents=True)
        original = '{"theme":"system","defaultModel":"keep-me","packages":["keep"]}'
        settings.write_text(original)
        ghostty = installer.plan(self.home)[0][1]
        ghostty.parent.mkdir(parents=True)
        ghostty.write_text('font-size = 18\n')
        backup = self.run_install(True)
        config = json.loads(settings.read_text())
        self.assertEqual(config, {'theme': 'dr-pepper', 'defaultModel': 'keep-me', 'packages': ['keep']})
        manifest = json.loads((backup / 'manifest.json').read_text())
        originals = {item['destination']: item['original'] for item in manifest}
        self.assertEqual(Path(originals[str(settings)]).read_text(), original)
        self.assertEqual(Path(originals[str(ghostty)]).read_text(), 'font-size = 18\n')
        for source, dest in installer.plan(self.home):
            self.assertEqual(source.read_bytes(), dest.read_bytes())
        second = self.run_install(True)
        self.assertNotEqual(second, backup)

    def test_invalid_settings_fail_before_copying(self):
        settings = self.home / '.pi/agent/settings.json'
        settings.parent.mkdir(parents=True)
        settings.write_text('[]')
        with self.assertRaises(ValueError):
            self.run_install(True)
        self.assertFalse((self.home / 'Library').exists())

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
