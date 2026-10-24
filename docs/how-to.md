# Customise and maintain the setup

## Install only the colours

Do not run the full installer if you want to preserve your existing shortcuts.

- Ghostty: merge the colour, palette, contrast, and font lines from `ghostty/config.ghostty` into your existing configuration. Omit its `keybind` lines.
- Herdr: merge the `[theme]` and `[theme.custom]` tables into your configuration. Do not duplicate TOML tables.
- Pi: copy `pi/themes/dr-pepper.json` to `~/.pi/agent/themes/`, then select it in `/settings`.
- Fonts: copy the four `fonts/CommitMono/*.otf` files to `~/Library/Fonts/`.

## Change the font or size

Edit Ghostty's configuration:

```ini
font-family = CommitMono
font-size = 14
```

Use an installed family's exact name. Ghostty's `+list-fonts` command lists recognised families. Reload with Command+Shift+,. If a newly installed font is absent, restart Ghostty when safe.

Iosevka Term, JetBrains Mono, and Monaspace Neon were tried before settling on CommitMono. They are not bundled here.

## Change the palette

Edit `ghostty/config.ghostty` for terminal defaults and ANSI colours, `herdr/config.toml` for Herdr's interface, and `pi/themes/dr-pepper.json` for Pi's role colours.

Reinstall only if you intend to replace the live files again. Otherwise edit the installed files directly. Reload Ghostty and Herdr; Pi hot-reloads an already selected user theme.

## Restore previous files

The installer prints a backup path under `~/.local/state/michaelasper-theme/backups/`. Its `manifest.json` records every destination and the saved original, if one existed.

1. Stop editing the affected configuration files.
2. Copy each saved original back to its recorded destination.
3. For a destination that had no original, remove only that specific installed file if you no longer want it.
4. Reload the affected applications.

Restoring Pi's entire settings backup also undoes settings changes made since installation. To retain those changes, change only its `theme` setting instead.

The installer refuses symlinked destination files to avoid changing another dotfiles checkout. Resolve that layout manually instead.

## Fix missing session names

1. Check that Pi is running inside a Herdr pane.
2. Run `herdr integration install pi` if the official integration is missing.
3. Check that `~/.pi/agent/extensions/herdr-session-label.ts` exists.
4. Run `/reload` in Pi and give the session a name with `/name`.
5. Run `herdr config check`, then `herdr server reload-config`.

Unnamed sessions display `Unnamed session`. Non-Pi agents retain their terminal-title labels.

## Fix a missing or stale subagent badge

Install `pi-subagents` through Pi's package mechanism, then run `/reload`. The configured version was 0.81.0. The count bridge listens for that package's `herdr:busy` event and parses its count label; it is not a general process counter.

Allow up to two seconds after a lifecycle event. The count is hidden at zero. If a package update changes the event or label format, the parser in the extension needs updating.

A badge surviving an abrupt Pi exit can be cleared from the original Herdr pane:

```sh
herdr pane report-metadata "$HERDR_PANE_ID" \
  --source pi-session-label --agent pi --applies-to-source herdr:pi \
  --clear-token subagents
```

## Keep Ghostty's own shortcuts

Remove the corresponding `keybind` forwarding lines from Ghostty and change the matching `[keys]` entries in Herdr to unused chords or prefix bindings. Reload both applications. Changing just one layer can leave a shortcut intercepted or unmatched.

## Validate changes

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests
herdr config check
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
```

The last two commands validate installed configurations. For the repository copy of Herdr, set `HERDR_CONFIG_PATH="$PWD/herdr/config.toml"`. For Ghostty, pass `--config-file="$PWD/ghostty/config.ghostty"`.
