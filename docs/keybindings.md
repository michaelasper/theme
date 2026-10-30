# Keybinding reference

On macOS, Command = ⌘, Option = ⌥, Shift = ⇧. The Herdr app receives these keys directly; no terminal forwarding is involved.

## Changed by this repository

`herdr-app/keys.json` is merged into the `global` section of your `keys.json`.

| Shortcut | Command | Effect |
|---|---|---|
| ⌘W | `pane.close` | Close the current pane (Herdr's default closes the tab) |
| ⌘⇧← / → | `tab.prev` / `tab.next` | Previous / next tab |
| ⌘⇧N | `space.new` | Create a space |
| ⌘⇧1–9 | `space.select:N` | Select a space |

## Herdr defaults this setup relies on

| Shortcut | Command | Effect |
|---|---|---|
| ⌘D | `pane.split:right` | Side-by-side panes |
| ⌘⇧D | `pane.split:down` | Top/bottom panes |
| ⌘⌥← / ↓ / ↑ / → | `pane.go:*` | Directional pane focus |
| ⌘⌥⇧← / ↓ / ↑ / → | `pane.swap:*` | Swap with a neighbour |
| ⌘⇧Enter | `pane.zoom` | Toggle pane zoom |
| ⌘T | `tab.new` | Create a tab |
| ⌘1–9 | `tab.select:N` | Select a tab |
| ⌘P | `mod.open:picker` | Choose a space |
| ⌘B | `layout.toggle:sidebar` | Toggle sidebar |
| ⌘[ / ⌘] | `agent.prev` / `agent.next` | Previous / next agent |
| ⌘⇧P | `app.palette` | Command palette |

Herdr's defaults can change between releases; `herdr-app commands` and the palette show the current list.

## No longer available

The earlier Herdr TUI setup used a Ctrl+B prefix, direct pane-resize shortcuts, and plugin shortcuts (command bar, TTT, Reviewr, Annotate). The app has no prefix mode or pane-resize command, and those plugins are not mods. Resize by dragging dividers.

## Terminal keys

Copy/paste (⌘C / ⌘V), Ctrl+C / Ctrl+Z / Ctrl+D, and word/line editing keys are in the `terminal` section of the default `keys.json` and are not changed here.
