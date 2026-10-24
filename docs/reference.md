# Configuration reference

## Files

| Repository file | macOS destination | Purpose |
|---|---|---|
| `ghostty/config.ghostty` | `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty` | Palette, font, padding, keyboard forwarding |
| `herdr/config.toml` | `~/.config/herdr/config.toml` | Theme, shortcuts, pane UI, agent rows |
| `pi/themes/dr-pepper.json` | `~/.pi/agent/themes/dr-pepper.json` | Pi role colours |
| `pi/extensions/herdr-session-label.ts` | `~/.pi/agent/extensions/herdr-session-label.ts` | Session and subagent metadata |
| `pi/settings.example.json` | Merged into `~/.pi/agent/settings.json` | Theme selection only |
| `fonts/CommitMono/*.otf` | `~/Library/Fonts/` | Four font styles |

Pi provider/model settings and package lists are deliberately not included.

## Recorded environment

| Component | Version |
|---|---|
| Ghostty | 1.3.1 |
| Herdr | 0.9.5 |
| Pi | 1.4.0 |
| pi-subagents | 0.81.0 |
| CommitMono | 1.143 |
| Installer and checks | Python 3.11+ |

These are the source machine's versions, not a tested compatibility range. The font is bundled; application binaries and Pi packages are not.

## Main colours

| Role | Value |
|---|---|
| Terminal / Herdr background | `#352f32` |
| Foreground | `#faf3ea` |
| Herdr sidebar | `#2d272a` |
| Ghostty cursor / Pi border accent | `#f29aaa` |
| Herdr accent / focused pane outline | `#ffd0d8` |
| Herdr inactive pane outline | `#82717a` |
| Selection | `#704555` |
| Pi neutral tool panel | `#3c3539` |
| Pi mint success | `#a4d2c2` |
| Pi error | `#ff98a3` |
| Pi muted text | `#c3b7bd` |

Ghostty's minimum contrast is 5. Its ANSI green remains `#a9c68b`; Pi's mint overrides its own success roles. Not every application uses ANSI colours, and the contrast setting does not guarantee every rendered UI element meets a particular accessibility standard.

## Other settings

- CommitMono at 14 pt; opaque background; 8 px horizontal and 6 px vertical padding.
- Herdr sidebar: default 24 columns, minimum 18, maximum 32.
- New panes inherit the source working directory.
- New tabs do not prompt for a name.
- Workspace close confirmation remains enabled.
- Pane borders are always visible, with outer borders and separate pane outlines enabled. Focused outlines use bright blush; inactive outlines use muted mauve.
- Agent state indicators use symbols; in-app toasts remain enabled; sounds are disabled.
- Per-pane scrollback limit: 10,000,000 bytes.

## Agent-label contract

The custom hook is enabled only when `HERDR_ENV=1`, `HERDR_PANE_ID` exists, and Pi starts in TUI mode.

| Token | Source | Value |
|---|---|---|
| `$session_name` | `pi.getSessionName()` | Name, or `Unnamed session` |
| `$subagents` | `pi-subagents` `herdr:busy` event | `N 👾` for N > 0; cleared at zero |

Herdr metadata source is `pi-session-label`, scoped to agent `pi` and lifecycle source `herdr:pi`. The sidebar's Pi-specific rows are:

```toml
pi = [["state_icon", "$session_name", "$subagents"], ["agent"]]
```

The hook samples changes every two seconds, suppresses unchanged reports, serialises its CLI writes, and retries failed reports on later ticks. Each CLI call has a two-second timeout. It never starts or stops agents.

The parser recognises labels beginning with `⏳ N subagent` or `⏳ N subagents`. An inactive event clears the count. The upstream bridge supplies the active-run projection and excludes workflow coordinators. This repository does not independently enumerate child processes.

Metadata has no custom TTL. A clean runtime shutdown stops the timer and unsubscribes the listener; abrupt termination may leave metadata until Herdr removes the agent or a later report replaces it.

## Installer

`python3 scripts/install.py` previews; `--apply` writes. There are no other command-line options except help. It makes no network requests, installs no application packages, and restarts no applications.

Existing files are backed up before any destinations are overwritten. Pi settings must be a JSON object. Symlinked destination files are rejected. Parent-directory symlinks are not rejected. The operation is not transactional; an I/O error during copying may leave a partial installation, with the backup manifest available for recovery.

## Font integrity

`fonts/CommitMono/SHA256SUMS` records SHA-256 hashes for all four OTF files. `scripts/check.py` verifies them.
