# Dr Pepper terminal theme

Warm charcoal, cherry accents, cream text, and CommitMono for the Herdr app and Pi.

[Get started](docs/tutorial.md) · [Customise](docs/how-to.md) · [Keybindings](docs/keybindings.md) · [Reference](docs/reference.md)

## What's included

- A Herdr app theme (`herdr-app/themes/dr-pepper.json`) with the 16-colour terminal palette and interface colours.
- Herdr app settings (font, sounds) and shortcuts, merged into your existing files.
- A Pi theme with neutral tool panels and mint success indicators.
- CommitMono 1.143, with regular, italic, bold, and bold italic fonts and the upstream OFL licence.

This is a macOS setup for running Pi inside the [Herdr app](https://herdr.dev), which draws its own window and no longer needs Ghostty. It is a snapshot of a personal configuration, not a standalone terminal application.

## Install

Requires the Herdr app, Pi, and Python 3.11+.

```sh
git clone https://github.com/michaelasper/theme.git
cd theme
python3 scripts/install.py
```

The command above only previews destinations. Read the plan, then run:

```sh
python3 scripts/install.py --apply
```

The installer **merges** into `~/.config/herdr-app/settings.json` and `keys.json` (or `$HERDR_APP_HOME`) and Pi's `settings.json`, keeping unrelated entries, and copies the themes and fonts. Everything it touches is backed up first.

Herdr reloads its files when they are saved. Run `/reload` in each Pi session, and select `dr-pepper` in Pi's `/settings` if the current session retains its old theme.

## Daily use

| Shortcut | Action |
|---|---|
| Command+D | Split side by side |
| Command+Shift+D | Split top/bottom |
| Command+Option+arrows | Focus a pane |
| Command+Shift+Enter | Zoom the current pane |
| Command+W | Close the pane |
| Command+P | Pick a space |

The [complete keybinding reference](docs/keybindings.md) covers tabs, spaces, and what this setup leaves at Herdr's defaults.

## Documentation

The docs use the [Diátaxis](https://diataxis.fr/) approach, with each page serving a distinct need:

- [Tutorial](docs/tutorial.md): reproduce the setup and try a split.
- [How-to guides](docs/how-to.md): customise, restore backups, or fix missing names and badges.
- [Reference](docs/reference.md): files, colours, dependencies, and metadata contracts.
- [Keybinding reference](docs/keybindings.md): actions and their exact shortcuts.
- [Explanation](docs/explanation.md): why the palette and layers work this way.

## Validation

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests
```

Checks cover file formats, palette/shortcut consistency, theme tokens, font checksums, and installation behaviour. Actual rendering and font availability still require a terminal.

## Credits and licensing

[CommitMono](https://commitmono.com/) remains under the [SIL Open Font License](fonts/CommitMono/OFL.txt). The Pi theme started from Pi's built-in dark theme; see [third-party notices](THIRD_PARTY_NOTICES.md).

This repository is not affiliated with Dr Pepper. No brand artwork is included. Other original material in this repository is published without an additional licence grant.
