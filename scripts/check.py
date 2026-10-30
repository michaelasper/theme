#!/usr/bin/env python3
"""Offline structural checks, not a substitute for rendering in Herdr."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HEX = re.compile(r'#[0-9a-fA-F]{6}')
ACTION = re.compile(r'^[a-z_]+\.[a-z_]+(:[\w]+)?$')


def main():
    pi = json.loads((ROOT / 'pi/themes/dr-pepper.json').read_text())
    assert pi['name'] == 'dr-pepper'
    assert json.loads((ROOT / 'pi/settings.example.json').read_text()) == {'theme': 'dr-pepper'}
    variables = pi['vars']
    for colour in [*pi['colors'].values(), *pi['export'].values()]:
        seen = set()
        while colour in variables:
            assert colour not in seen, 'Circular theme variable'
            seen.add(colour)
            colour = variables[colour]
        assert HEX.fullmatch(colour), f'Invalid colour: {colour}'

    theme = json.loads((ROOT / 'herdr-app/themes/dr-pepper.json').read_text())
    for key in ('background', 'foreground', 'selection', 'cursor'):
        assert HEX.fullmatch(theme[key]), key
    assert len(theme['ansi']) == 16 and all(HEX.fullmatch(c) for c in theme['ansi'])
    assert all(HEX.fullmatch(c) for c in theme['colors'].values())
    assert theme['foreground'] == pi['vars']['text']
    assert theme['colors']['accent'] != theme['colors']['muted']
    assert theme['colors']['surface'] == theme['background']

    settings = json.loads((ROOT / 'herdr-app/settings.json').read_text())
    assert settings['theme'] == 'dr-pepper' and settings['font'] == 'CommitMono'

    keys = json.loads((ROOT / 'herdr-app/keys.json').read_text())
    assert set(keys) == {'global'}
    for chord, action in keys['global'].items():
        assert re.fullmatch(r'(cmd|ctrl|alt|shift)(-(cmd|ctrl|alt|shift))*-[^-]+|(cmd|ctrl|alt|shift)+-?-', chord), chord
        assert ACTION.match(action), f'Bad action: {action}'

    for line in (ROOT / 'fonts/CommitMono/SHA256SUMS').read_text().splitlines():
        digest, name = line.split()
        assert hashlib.sha256((ROOT / 'fonts/CommitMono' / name).read_bytes()).hexdigest() == digest
    # Check local Markdown links without fetching external sites.
    for doc in ROOT.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (doc.parent / link.split('#')[0]).exists(), f'Broken link in {doc}: {link}'
    print('Themes, settings, shortcuts, font hashes, and doc links: OK')


if __name__ == '__main__':
    main()
