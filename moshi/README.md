# Dr Pepper for Moshi

Warm charcoal, cherry accents, and cream text, using the same 16-colour palette as this repository's Herdr theme.

## Import

1. Open [the raw theme JSON](https://raw.githubusercontent.com/michaelasper/theme/main/moshi/dr-pepper.json) and copy its contents.
2. In Moshi, open **Settings → Theme → Import theme**.
3. Paste the JSON, import it, and select **Dr Pepper**.

Moshi uses the imported terminal palette to derive its surrounding app colours too. No host installation or terminal restart is needed. The repository's macOS installer does not import themes into the phone app.

The file uses [Moshi's documented v1 theme format](https://getmoshi.app/docs/personalization), with all 16 ANSI colours plus background, foreground, cursor, and selection colours specified. Structural validation runs through `python3 scripts/check.py`; on-device appearance still needs visual verification.

[Theme file](dr-pepper.json) · [Back to the repository](../README.md)
