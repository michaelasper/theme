#!/usr/bin/env python3
"""Preview or install the macOS configuration. No network access or app restarts."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def plan(home: Path):
    pairs = [
        (ROOT / 'ghostty/config.ghostty', home / 'Library/Application Support/com.mitchellh.ghostty/config.ghostty'),
        (ROOT / 'herdr/config.toml', home / '.config/herdr/config.toml'),
        (ROOT / 'pi/themes/dr-pepper.json', home / '.pi/agent/themes/dr-pepper.json'),
        (ROOT / 'pi/extensions/herdr-session-label.ts', home / '.pi/agent/extensions/herdr-session-label.ts'),
    ]
    pairs.extend((font, home / 'Library/Fonts' / font.name)
                 for font in sorted((ROOT / 'fonts/CommitMono').glob('*.otf')))
    return pairs


def install(home: Path, apply: bool):
    pairs = plan(home)
    settings = home / '.pi/agent/settings.json'
    destinations = [dest for _, dest in pairs] + [settings]
    for dest in destinations:
        if dest.is_symlink():
            raise ValueError(f'Refusing symlinked destination: {dest}')
        if dest.exists() and not dest.is_file():
            raise ValueError(f'Destination is not a regular file: {dest}')
    # Parse before making any changes; preserve all unrelated Pi settings.
    config = json.loads(settings.read_text()) if settings.exists() else {}
    if not isinstance(config, dict):
        raise ValueError('Pi settings must be a JSON object')
    config['theme'] = 'dr-pepper'
    for source, dest in pairs:
        if not source.is_file():
            raise ValueError(f'Missing source: {source}')
        print(f'Copy {source.relative_to(ROOT)} -> {dest}')
    print(f'Merge theme selection -> {settings}')
    if not apply:
        print('Preview only. Use --apply to back up and install these files.')
        return None

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    backup = home / '.local/state/michaelasper-theme/backups' / stamp
    backup.mkdir(parents=True, exist_ok=False)
    manifest = []
    for index, dest in enumerate(destinations):
        saved = backup / f'{index:02d}-{dest.name}' if dest.exists() else None
        if saved:
            shutil.copy2(dest, saved)
        manifest.append({'destination': str(dest), 'original': str(saved) if saved else None})
    (backup / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for source, dest in pairs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(config, indent=2) + '\n')
    print(f'Backup: {backup}')
    print('Reload Ghostty, reload Herdr config, and run /reload in Pi.')
    return backup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Back up and replace configs; default is preview')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        parser.error('This installer targets macOS only.')
    try:
        install(Path.home(), args.apply)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Installation failed: {error}\n')
