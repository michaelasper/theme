# Why this setup looks and behaves this way

The first Dr Pepper-inspired palette used a near-black burgundy background. It was too dark. Raising the burgundy alone made the whole screen feel pink, so the final background is a warmer, less saturated charcoal. Cherry accents and cream text retain the colour association without colouring every panel red.

Pi's automatic terminal theme adapts ANSI colours to interface roles. That produced more green than wanted, especially around successful tools. The custom Pi theme gives pending and successful tools the same neutral background. Mint remains a success and diff colour rather than a large panel fill. This is why Pi has its own palette instead of relying entirely on the terminal's.

CommitMono was chosen after comparing Iosevka Term, JetBrains Mono, and Monaspace Neon at 14 pt. The repository preserves the selected font rather than installing every experiment.

## Why there is no terminal emulator layer

Earlier versions ran the Herdr TUI inside Ghostty. Ghostty owned the macOS shortcuts, so it had to forward each chord to Herdr as an explicit keyboard sequence, and that forwarding took those shortcuts away from every Ghostty window. The Herdr app draws its own window and receives keys directly. Palette, font, and shortcuts now live in one place, and nothing outside Herdr is affected.

## Why the installer merges

The app's `settings.json` holds personal choices such as zoom, and `keys.json` holds the full shortcut table. Replacing either would discard them. The installer therefore writes only the entries this theme owns and leaves the rest.

## Why the shipped layouts are untouched

Herdr replaces its own layouts and mods on every start; an edited copy is moved aside. A look this repository wants therefore goes through theme colours and settings, which survive, not through layout edits. Pane outline and sidebar details come from the shipped layout until you clone one.

## Why session names need no extension

The earlier setup published `session_name` and a subagent count through the legacy `herdr` metadata CLI. The app's Agents list reads the terminal title and shows sub-agents under their parent natively, so the extension was removed.

The repository also excludes Pi sessions, personal provider settings, logs, socket files, and authentication data. Those are runtime state, not parts of a theme.
