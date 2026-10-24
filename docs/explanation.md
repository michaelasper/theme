# Why this setup looks and behaves this way

The first Dr Pepper-inspired palette used a near-black burgundy background. It was too dark. Raising the burgundy alone made the whole screen feel pink, so the final background is a warmer, less saturated charcoal. Cherry accents and cream text retain the colour association without colouring every panel red.

Pi's automatic terminal theme adapts ANSI colours to interface roles. That produced more green than wanted, especially around successful tools. The custom Pi theme gives pending and successful tools the same neutral background. Mint remains a success and diff colour rather than a large panel fill. This is why Pi has its own palette instead of relying entirely on Ghostty.

CommitMono was chosen after comparing Iosevka Term, JetBrains Mono, and Monaspace Neon at 14 pt. The repository preserves the selected font rather than installing every experiment.

## Why each pane has its own outline

Shared dividers are compact, but a highlighted divider touches two panes and can make focus ambiguous. Separate outlines and outer borders give the focused pane a complete bright blush frame. Inactive outlines stay muted. Herdr also renders the focused pane's border label in bold when a label is present. This uses more terminal cells than shared splitters, in exchange for clearer keyboard navigation.

## Why there are two shortcut configurations

Ghostty owns the macOS keyboard shortcuts before Herdr sees terminal input. Merely binding Command+D in Herdr is insufficient if Ghostty consumes it to split its own window.

Ghostty therefore sends explicit modified keyboard sequences. Herdr maps those inputs to pane, tab, and workspace actions. This makes the layout belong to Herdr, but sacrifices those native Ghostty shortcuts globally. Command+N still creates a native Ghostty window.

The existing Ctrl+B prefix remains for less frequent actions. Close-tab and close-workspace actions stay behind that prefix to reduce accidental closure. Workspace confirmation is enabled; that is not a guarantee that every individual pane close prompts.

## Why session names use metadata

A terminal title can include an application marker, a conversation name, and a working-directory label. Stripping terminal escape sequences does not remove those semantic parts.

The custom extension reads Pi's session name directly and publishes a separate `session_name` token. Herdr can then render that token without changing the terminal title or guessing which substring is a path.

Subagent activity already has a Herdr bridge inside `pi-subagents`. The custom extension extracts only its active count and publishes `subagents`, avoiding the bridge's longer task and agent summary. Workflow coordinators are handled by the upstream projection rather than counted again here.

This count depends on an upstream event's formatted label, not a stable numeric API. The source version and parser contract are documented so breakage can be diagnosed instead of silently treated as authoritative.

## Why the official integration is not vendored

Herdr owns its agent-state integration and may overwrite it during updates. This repository keeps its custom label hook in a separate file. The official integration is installed using Herdr itself.

The repository also excludes Pi sessions, personal provider settings, logs, socket files, and authentication data. Those are runtime state, not parts of a theme.
