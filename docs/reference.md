# Configuration reference

## Files

| Repository file | macOS destination | How |
|---|---|---|
| `herdr-app/themes/dr-pepper.json` | `~/.config/herdr-app/themes/dr-pepper.json` | Copied |
| `herdr-app/settings.json` | `~/.config/herdr-app/settings.json` | Merged (top-level keys; `sounds` entries merged) |
| `herdr-app/keys.json` | `~/.config/herdr-app/keys.json` | Merged (per section) |
| `pi/themes/dr-pepper.json` | `~/.pi/agent/themes/dr-pepper.json` | Copied |
| `pi/settings.example.json` | `~/.pi/agent/settings.json` | Theme selection merged |
| `fonts/CommitMono/*.otf` | `~/Library/Fonts/` | Copied |

`$HERDR_APP_HOME` replaces `~/.config/herdr-app`. Pi provider/model settings and package lists are deliberately not included.

## Recorded environment

| Component | Version |
|---|---|
| Herdr app | 0.1.9 |
| Pi | 1.4.0 |
| CommitMono | 1.143 |
| Installer and checks | Python 3.11+ |

These are the source machine's versions, not a tested compatibility range. The font is bundled; application binaries are not.

## Main colours

| Role | Value |
|---|---|
| Terminal background / Herdr surface | `#352f32` |
| Foreground | `#faf3ea` |
| Herdr sidebar and chrome | `#2d272a` |
| Herdr selected row | `#514047` |
| Cursor / Pi border accent | `#f29aaa` |
| Herdr accent | `#ffd0d8` |
| Herdr muted | `#82717a` |
| Selection | `#704555` |
| Pi neutral tool panel | `#3c3539` |
| Pi mint success | `#a4d2c2` |
| Pi error | `#ff98a3` |
| Pi muted text | `#c3b7bd` |

The theme file's `ansi` array is the 16-colour palette. ANSI green stays `#a9c68b`; Pi's mint overrides its own success roles. `minimum_contrast` is 1, so program colours are not adjusted. The earlier Ghostty setup used 5.

## Other settings

- CommitMono at 14 px, before Herdr's `zoom`.
- Sounds are disabled.
- Pane frames, sidebar width, and other layout details are the shipped layout's; the shipped `main` layout is read-only, so this repository does not override them. Clone a layout (`layout.clone`) to change them.

## Installer

`python3 scripts/install.py` previews; `--apply` writes. There are no other command-line options except help. It makes no network requests, installs no application packages, and restarts no applications.

JSON destinations must parse as objects, and are checked before anything is written. Existing files are backed up first. Symlinked destination files are rejected; parent-directory symlinks are not. The operation is not transactional; an I/O error during copying may leave a partial installation, with the backup manifest available for recovery.

## Font integrity

`fonts/CommitMono/SHA256SUMS` records SHA-256 hashes for all four OTF files. `scripts/check.py` verifies them.
