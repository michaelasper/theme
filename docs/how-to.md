# Customise and maintain the setup

Herdr app files live in `~/.config/herdr-app` (or `$HERDR_APP_HOME`). Herdr's own guide, `AGENTS.md` in that folder, is the authority on their format.

## Install only the colours

Do not run the full installer if you want to preserve your existing shortcuts.

- Herdr: copy `herdr-app/themes/dr-pepper.json` to `~/.config/herdr-app/themes/`, then set `"theme": "dr-pepper"` in `settings.json`.
- Pi: copy `pi/themes/dr-pepper.json` to `~/.pi/agent/themes/`, then select it in `/settings`.
- Fonts: copy the four `fonts/CommitMono/*.otf` files to `~/Library/Fonts/`, then set `"font": "CommitMono"` in `settings.json`.

## Change the font or size

Edit `settings.json`:

```json
{ "font": "CommitMono", "font_size": 14 }
```

Use an installed family's exact name. A terminal font the machine lacks falls back to JetBrains Mono. `zoom` scales everything, including the font.

Iosevka Term, JetBrains Mono, and Monaspace Neon were tried before settling on CommitMono. They are not bundled here.

## Change the palette

Edit `herdr-app/themes/dr-pepper.json` for terminal colours and Herdr's interface (`colors` overrides any named theme colour), and `pi/themes/dr-pepper.json` for Pi's role colours. Keep the matching copy in `~/.config/herdr-app/themes/` in sync, or reinstall. Herdr and Pi reload on save.

## Change a shortcut

Edit `~/.config/herdr-app/keys.json`. Keys are `global`, `terminal`, `layout:<name>` or `mod:<name>` sections of `"chord": "command"`. `herdr-app commands` lists every command. Run `herdr-app status` afterwards: a broken file keeps the old version running and reports the error there.

## Restore previous files

The installer prints a backup path under `~/.local/state/michaelasper-theme/backups/`. Its `manifest.json` records every destination and the saved original, if one existed.

1. Copy each saved original back to its recorded destination.
2. For a destination that had no original, remove only that installed file if you no longer want it.

Restoring Pi's entire settings backup also undoes settings changes made since installation. To keep those, change only its `theme` setting.

The installer refuses symlinked destination files to avoid changing another dotfiles checkout.

## Fix a missing session name

The Agents list shows what Pi puts in its terminal title. Give the session a name with `/name`, and check `herdr-app ls` for the pane's title. Sub-agents started with `hc run` appear under their parent natively.

An older `~/.pi/agent/extensions/herdr-session-label.ts` from earlier versions of this repository talks to the legacy `herdr` CLI, is not used by the app, and can be deleted.

## Validate changes

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests
herdr-app status
```
