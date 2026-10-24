# Keybinding reference

On macOS, Command = ⌘, Option = ⌥, Shift = ⇧. These are direct Herdr actions forwarded by Ghostty.

## Direct shortcuts

| Shortcut | Herdr action | Effect |
|---|---|---|
| ⌘D | `split_vertical` | Side-by-side panes |
| ⌘⇧D | `split_horizontal` | Top/bottom panes |
| ⌘⌥← / ↓ / ↑ / → | `focus_pane_*` | Directional pane focus |
| ⌘⌥⇧← / ↓ / ↑ / → | `resize_pane_*` | Directional resize |
| ⌘⇧Enter | `zoom` | Toggle pane zoom |
| ⌘T | `new_tab` | Create a Herdr tab |
| ⌘W | `close_pane` | Close current pane, not the native window |
| ⌘⇧← / → | `previous_tab` / `next_tab` | Previous / next Herdr tab |
| ⌘1–9 | `switch_tab` | Select a Herdr tab |
| ⌘⇧N | `new_workspace` | Create workspace |
| ⌘P | `workspace_picker` | Choose workspace |
| ⌘B | `toggle_sidebar` | Toggle sidebar |

The config does not add direct destructive close-workspace or close-tab shortcuts.

## Prefix shortcuts

Ctrl+B enters Herdr's prefix mode. The following actions retain the Herdr 0.9.5 defaults; they are not duplicated in the file.

| After Ctrl+B | Action |
|---|---|
| ? | Help |
| s | Settings |
| q | Detach |
| Shift+R | Reload configuration |
| o | Open notification target |
| w | Workspace picker |
| g | Go to |
| Shift+G | New worktree |
| Shift+W | Rename workspace |
| Shift+D | Close workspace |
| Shift+T | Rename tab |
| Shift+X | Close tab |
| Shift+P | Rename pane |
| e | Edit scrollback |
| Tab / Shift+Tab | Cycle panes forward / backward |
| r | Resize mode |

Custom action bindings replace that action's default prefix binding. For example, Ctrl+B then v is not an additional split shortcut in this setup; ⌘D replaces it. Use `herdr --default-config` for the installed version's full default list.

## Keys left to Ghostty or pane applications

| Keys | Behaviour |
|---|---|
| ⌘C / ⌘V | Native copy / paste |
| ⌘N | Native Ghostty window |
| ⌘, | Ghostty configuration |
| ⌘⇧, | Reload Ghostty configuration |
| Native font zoom shortcuts | Unchanged |
| Ctrl+C / Ctrl+Z / Ctrl+D | Passed through under normal terminal behaviour |

## Forwarding format

Ghostty emits CSI sequences using the command modifier bit rather than performing its built-in action.

| Chord | Ghostty action |
|---|---|
| ⌘D | `csi:100;9u` |
| ⌘⇧D | `csi:100;10u` |
| ⌘⌥Left | `csi:1;11D` |
| ⌘⌥⇧Left | `csi:1;12D` |
| ⌘⇧Enter | `csi:13;10u` |

Modifier parameters include the protocol's offset of one: 9 is Command, 10 adds Shift, 11 adds Option, and 12 adds both. Letter/digit bindings use Unicode code points with the `u` suffix; arrows use their CSI final byte.

The full forwarding map is in [Ghostty's config](../ghostty/config.ghostty), with matching action bindings in [Herdr's config](../herdr/config.toml).

These mappings apply to every Ghostty surface. Outside Herdr, the foreground program receives the sequences and may ignore or interpret them differently.
