# Install and use the optional Herdr plugins

These plugins add a command bar, an editor, diff review, and annotations. Their shortcuts are included in the configurations, but `scripts/install.py` does not download or enable plugins. Each plugin installation executes upstream build/install commands with your user permissions. Review the upstream project before installing.

## Install

Run these from a Herdr pane:

```sh
herdr plugin install jeffarese/herdr-bar
INSTALL_DIR="$HOME/.local/bin" PATH="$HOME/.local/bin:$PATH" \
  herdr plugin install eugenioenko/ttt/herdr-plugin
herdr plugin install persiyanov/herdr-reviewr
herdr plugin install plannotator/herdr-annotate
herdr server reload-config
```

TTT's default macOS installer targets `/usr/local/bin` and may ask for sudo. The override above uses your own `~/.local/bin`; make sure that directory is also on your shell and Herdr server's PATH. The plugin installs TTT automatically if the executable is missing. Git and ripgrep are needed for its full feature set.

Reload Ghostty with Command+Shift+, to activate the direct shortcuts. Prefix shortcuts work without the Ghostty changes. The prefix below means press Ctrl+B, release it, then press the listed chord.

## Open a plugin

| Shortcut | Prefix fallback | Action |
|---|---|---|
| Command+K | prefix, k | Fuzzy command bar |
| Command+E | prefix, Ctrl+E | Open TTT in a new tab |
| Command+R | prefix, Ctrl+R | Toggle Reviewr's diff pane |
| prefix, a | | Annotate selected terminal text |
| prefix, Shift+A | | Copy annotations |
| prefix, Ctrl+A | | Copy and archive annotations |
| prefix, Ctrl+V | | Paste annotations into the agent prompt without sending |
| prefix, Ctrl+S | | Send annotations to the agent and archive them |
| prefix, m | | Manage annotations |
| prefix, Ctrl+O | | Review documents in the focused folder |
| prefix, Shift+O | | Review an agent reply |
| prefix, Ctrl+Shift+O | | Review the newest agent reply |

Command+K replaces Ghostty's native clear-scrollback shortcut. Command+E and Command+R also replace any native Ghostty binding on those chords. The existing pane-navigation shortcuts, prefix-e scrollback editor, prefix-o notification target, and prefix-Shift+R config reload remain intact.

## Plugin behaviour

- **Herdr Bar** automatically names eligible unnamed Claude/Codex tabs by default. It preserves custom names; tab-status prefixes are off by default. On an already running server, opening the bar ensures the title watcher starts. No icon font is installed by this setup; the bar can use text labels.
- **TTT** opens the active worktree or workspace in a new Herdr tab. The executable is installed separately from the plugin registration.
- **Reviewr** automatically opens for newly created/opened worktree workspaces by default. Reviewing does not itself send comments; sending is an explicit action.
- **Annotate** is the full variant, including Plannotator TUI for documents and agent replies. The optional Markdown link-handler add-on is not installed.

No plugin interaction was used to submit feedback to an agent during installation. The Dr Pepper configs do not override these plugins' internal themes.

## Inspect or remove a plugin

```sh
herdr plugin list
herdr plugin action list
herdr plugin disable herdr-bar
```

Other plugin IDs are `ttt.editor`, `persiyanov.reviewr`, and `annotate`. `herdr plugin uninstall <id>` removes the registration/install; a separately installed TTT executable may remain. Remove corresponding `[[keys.command]]` entries and Ghostty forwarding lines when you no longer want their shortcuts.

## Recorded versions

| Project | Plugin version | Source commit |
|---|---|---|
| [herdr-bar](https://github.com/jeffarese/herdr-bar) | 0.11.0 | `261de9b0441a6972941414bbf16eb4f5df27ac34` |
| [ttt/herdr-plugin](https://github.com/eugenioenko/ttt/tree/main/herdr-plugin) | 0.1.2 | `b48bece159d68d93a43dbce72614bac6a7667747` |
| [herdr-reviewr](https://github.com/persiyanov/herdr-reviewr) | 0.48.0 | `a253b1bfe4b34182af3204b7fcc42ccfed1b87d9` |
| [herdr-annotate](https://github.com/plannotator/herdr-annotate) | 0.9.3 | `b8b9de1aee7039651be315441c8d6a0f3e869c84` |

The installed TTT executable reports v1.9.0. The commands above track upstream defaults rather than pinning these commits. Plugins and their binaries are not vendored into the theme repository.
