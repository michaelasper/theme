# Set up your first themed workspace

This tutorial takes you from the repository to a themed Herdr workspace with two panes. It assumes macOS with Ghostty, Herdr, Pi, and Python 3.11+ already installed.

## 1. Get the files

```sh
git clone https://github.com/michaelasper/theme.git
cd theme
python3 scripts/install.py
```

You will see a preview of the files that would be installed. No configuration has changed yet.

## 2. Apply the setup

The next command replaces Ghostty and Herdr's configurations, including their keybindings. It saves existing files first.

```sh
python3 scripts/install.py --apply
```

Keep the backup directory printed by the installer. The four CommitMono fonts are installed into your user font directory.

## 3. Reload Ghostty

Press **Command+Shift+,** in Ghostty. The background should become warm charcoal with light cream text. If the font does not change, close and reopen Ghostty when it is safe to do so.

## 4. Open Herdr

In a Ghostty shell, run:

```sh
herdr
```

If Herdr is already running, reload its configuration from a pane instead:

```sh
herdr server reload-config
```

Press **Command+D**. You should now have two side-by-side panes. Press **Command+Option+Left** and **Command+Option+Right** to move between them.

## 5. Name a Pi session

Install Herdr's official Pi integration before starting Pi:

```sh
herdr integration install pi
pi
```

In Pi, use `/name theme-test`. Select `dr-pepper` in `/settings` if needed.

The Agents list should show `theme-test` with `pi` beneath it, without a path or the Greek-letter prefix. Existing Pi sessions need `/reload` to load the extension.

## 6. Check the compact badge

If `pi-subagents` is installed, ask Pi to launch two short, read-only test agents. While they run, the session row should include `2 👾`. As they finish, the count drops and then disappears.

You now have the palette, font, pane shortcuts, and session labels in place. See the [how-to guides](how-to.md) for changing individual parts.
