#!/usr/bin/env python3
"""Preview or install the macOS configuration. No network access or app restarts."""
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
THEME = 'dr-pepper'


def app_home(home: Path) -> Path:
    override = os.environ.get('HERDR_APP_HOME')
    return Path(override).expanduser() if override else home / '.config/herdr-app'


def plan(home: Path):
    """Files copied verbatim."""
    target = app_home(home)
    pairs = [
        (ROOT / 'herdr-app/themes/dr-pepper.json', target / 'themes/dr-pepper.json'),
        (ROOT / 'pi/themes/dr-pepper.json', home / '.pi/agent/themes/dr-pepper.json'),
    ]
    pairs.extend((font, home / 'Library/Fonts' / font.name)
                 for font in sorted((ROOT / 'fonts/CommitMono').glob('*.otf')))
    return pairs


def merge_plan(home: Path):
    """JSON files merged key by key into the user's own: (source or None, destination)."""
    target = app_home(home)
    return [
        (ROOT / 'herdr-app/settings.json', target / 'settings.json'),
        (ROOT / 'herdr-app/keys.json', target / 'keys.json'),
        (None, home / '.pi/agent/settings.json'),
    ]


def merged(source, dest: Path):
    current = json.loads(dest.read_text()) if dest.exists() else {}
    if not isinstance(current, dict):
        raise ValueError(f'{dest} must be a JSON object')
    if source is None:
        current['theme'] = THEME
        return current
    for key, value in json.loads(source.read_text()).items():
        if isinstance(value, dict) and isinstance(current.get(key), dict):
            current[key].update(value)
        else:
            current[key] = value
    return current


def install(home: Path, apply: bool):
    pairs, merges = plan(home), merge_plan(home)
    destinations = [dest for _, dest in pairs] + [dest for _, dest in merges]
    for dest in destinations:
        if dest.is_symlink():
            raise ValueError(f'Refusing symlinked destination: {dest}')
        if dest.exists() and not dest.is_file():
            raise ValueError(f'Destination is not a regular file: {dest}')
    # Parse everything before making any changes; unrelated settings are preserved.
    results = []
    for source, dest in merges:
        if source is not None and not source.is_file():
            raise ValueError(f'Missing source: {source}')
        results.append(merged(source, dest))
    for source, dest in pairs:
        if not source.is_file():
            raise ValueError(f'Missing source: {source}')
        print(f'Copy {source.relative_to(ROOT)} -> {dest}')
    for (source, dest) in merges:
        print(f'Merge {source.relative_to(ROOT) if source else "theme selection"} -> {dest}')
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
    for (_, dest), result in zip(merges, results):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, indent=2) + '\n')
    print(f'Backup: {backup}')
    print('Herdr reloads its files on save; run /reload in each Pi session.')
    return backup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Back up and install; default is preview')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        parser.error('This installer targets macOS only.')
    try:
        install(Path.home(), args.apply)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Installation failed: {error}\n')
