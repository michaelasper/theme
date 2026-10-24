#!/usr/bin/env python3
"""Offline structural checks, not a substitute for terminal rendering tests."""
import hashlib
import json
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    herdr = tomllib.loads((ROOT / 'herdr/config.toml').read_text())
    theme = json.loads((ROOT / 'pi/themes/dr-pepper.json').read_text())
    assert theme['name'] == 'dr-pepper'
    assert json.loads((ROOT / 'pi/settings.example.json').read_text()) == {'theme': 'dr-pepper'}
    variables = theme['vars']
    for colour in [*theme['colors'].values(), *theme['export'].values()]:
        seen = set()
        while colour in variables:
            assert colour not in seen, 'Circular theme variable'
            seen.add(colour)
            colour = variables[colour]
        assert re.fullmatch(r'#[0-9a-fA-F]{6}', colour), f'Invalid colour: {colour}'

    ghostty = {}
    bindings = {}
    palette = {}
    for line in (ROOT / 'ghostty/config.ghostty').read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        key, value = map(str.strip, line.split('=', 1))
        if key == 'keybind':
            chord, action = value.split('=', 1)
            assert chord not in bindings, f'Duplicate chord: {chord}'
            bindings[chord] = action
        elif key == 'palette':
            index, colour = value.split('=', 1)
            assert int(index) not in palette
            palette[int(index)] = colour
        else:
            assert key not in ghostty
            ghostty[key] = value
    assert set(palette) == set(range(16))
    assert ghostty['font-family'] == 'CommitMono'
    assert ghostty['background'] == herdr['theme']['custom']['panel_bg']
    assert ghostty['foreground'] == theme['vars']['text']
    for action, chord in herdr['keys'].items():
        if not chord.startswith('cmd+'):
            continue
        chords = [chord.replace('1..9', str(n)) for n in range(1, 10)] if '1..9' in chord else [chord]
        for expanded in chords:
            parts = expanded.split('+')
            key = parts[-1]
            mods = set(parts[:-1])
            modifier = 1 + sum({'cmd': 8, 'shift': 1, 'alt': 2}[m] for m in mods)
            arrow = {'up': 'A', 'down': 'B', 'right': 'C', 'left': 'D'}.get(key)
            code = 13 if key == 'enter' else ord(key) if len(key) == 1 else None
            expected = f'csi:1;{modifier}{arrow}' if arrow else f'csi:{code};{modifier}u'
            candidates = [value for trigger, value in bindings.items()
                          if set(trigger.split('+')) == {p.replace('cmd', 'super') for p in parts}]
            assert candidates == [expected], f'Forwarding mismatch: {action} / {expanded}'
    assert herdr['ui']['sidebar']['agents']['rows_by_agent']['pi'][0] == ['state_icon', '$session_name', '$subagents']
    for line in (ROOT / 'fonts/CommitMono/SHA256SUMS').read_text().splitlines():
        digest, name = line.split()
        assert hashlib.sha256((ROOT / 'fonts/CommitMono' / name).read_bytes()).hexdigest() == digest
    # Check local Markdown links without fetching external sites.
    for doc in ROOT.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (doc.parent / link.split('#')[0]).exists(), f'Broken link in {doc}: {link}'
    print('Configs, colour references, shortcut forwarding, font hashes, and doc links: OK')


if __name__ == '__main__':
    main()
