# Dr Pepper terminal theme

Warm charcoal, cherry accents, cream text, and CommitMono for Ghostty, Herdr, and Pi.

[Get started](docs/tutorial.md) · [Customise](docs/how-to.md) · [Keybindings](docs/keybindings.md) · [Reference](docs/reference.md)

## What's included

- The complete Ghostty configuration, including its 16-colour palette and Command-key forwarding.
- Matching Herdr colours, pane layout settings, and workspace/tab/pane shortcuts.
- A Pi theme with neutral tool panels and mint success indicators.
- A Pi extension that shows the session name and a compact active-subagent badge, such as `3 👾`, in Herdr.
- CommitMono 1.143, with regular, italic, bold, and bold italic fonts and the upstream OFL licence.

This is a macOS setup for running Pi inside Herdr inside Ghostty. It is a snapshot of a personal configuration, not a standalone terminal application.

## Install

Requires Ghostty, Herdr, Pi, and Python 3.11+. The optional count badge also requires `pi-subagents`.

```sh
git clone https://github.com/michaelasper/theme.git
cd theme
python3 scripts/install.py
```

The command above only previews destinations. Read the plan, then run:

```sh
python3 scripts/install.py --apply
```

**The installer replaces Ghostty and Herdr configurations after backing them up.** It merges only the theme selection into Pi's existing settings. For an existing customised setup, use the [selective installation guide](docs/how-to.md#install-only-the-colours) instead.

Reload Ghostty with **Command+Shift+,**, run `herdr server reload-config`, and run `/reload` in each Pi session. Select `dr-pepper` in Pi's `/settings` if the current session retains its old theme.

## Daily use

| Shortcut | Action |
|---|---|
| Command+D | Split side by side |
| Command+Shift+D | Split top/bottom |
| Command+Option+arrows | Focus a pane |
| Command+Option+Shift+arrows | Resize a pane |
| Command+Shift+Enter | Zoom the current pane |
| Command+P | Pick a workspace |

These shortcuts act on Herdr, not Ghostty. The forwarding applies to **all Ghostty windows**, including ones without Herdr. Copy/paste, native new-window, font-size controls, and native settings remain unchanged.

The [complete keybinding reference](docs/keybindings.md) covers tabs, workspaces, prefix actions, and the forwarding protocol.

## Documentation

The docs use the [Diátaxis](https://diataxis.fr/) approach, with each page serving a distinct need:

- [Tutorial](docs/tutorial.md): reproduce the setup and try a split.
- [How-to guides](docs/how-to.md): customise, restore backups, or fix missing names and badges.
- [Reference](docs/reference.md): files, colours, dependencies, and metadata contracts.
- [Keybinding reference](docs/keybindings.md): actions and their exact shortcuts.
- [Explanation](docs/explanation.md): why the palette and integrations work this way.

## Validation

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests
```

Checks cover file formats, palette/shortcut consistency, theme tokens, font checksums, and installation behaviour. Actual rendering and font availability still require a terminal.

## Credits and licensing

[CommitMono](https://commitmono.com/) remains under the [SIL Open Font License](fonts/CommitMono/OFL.txt). The Pi theme started from Pi's built-in dark theme; see [third-party notices](THIRD_PARTY_NOTICES.md).

This repository is not affiliated with Dr Pepper. No brand artwork is included. Other original material in this repository is published without an additional licence grant.
