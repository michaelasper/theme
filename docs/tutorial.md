# Set up your first themed space

This tutorial takes you from the repository to a themed Herdr app window with two panes. It assumes macOS with the Herdr app, Pi, and Python 3.11+ already installed.

## 1. Get the files

```sh
git clone https://github.com/michaelasper/theme.git
cd theme
python3 scripts/install.py
```

You will see a preview of the files that would be installed. No configuration has changed yet.

## 2. Apply the setup

```sh
python3 scripts/install.py --apply
```

The installer merges the theme, font, sound, and shortcut entries into your existing Herdr app files, so your other settings stay. It saves the originals first; keep the backup directory it prints. The four CommitMono fonts are installed into your user font directory.

## 3. Look at the window

Herdr reloads its files on save. The background should become warm charcoal with cream text, in CommitMono. If the font did not change, quit and reopen the Herdr app when it is safe to do so.

Confirm nothing was rejected:

```sh
herdr-app status
```

Its `errors` list should be empty.

## 4. Split a pane

Press **Command+D**. You should now have two side-by-side panes. Press **Command+Option+Left** and **Command+Option+Right** to move between them.

## 5. Name a Pi session

Start `pi` in a pane and use `/name theme-test`. Select `dr-pepper` in `/settings` if needed. The Agents list shows the session by its terminal title.

You now have the palette, font, and pane shortcuts in place. See the [how-to guides](how-to.md) for changing individual parts.
