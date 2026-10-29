# Pixelify Sans

The rotating hero introduction uses Pixelify Sans SemiBold (weight 600),
with a consistent size across all four phrases. The three section headings—My
GitHub Analytics, My Tech Stack, and Connect & Collaborate—use the same weight
at 26px.

Unmodified variable font from the official
[Google Fonts repository](https://github.com/google/fonts/tree/main/ofl/pixelifysans).
The original SIL Open Font License is retained in `OFL.txt`.
The font includes all punctuation used in the introduction.

Regenerate with `python build_typing_animation.py`. Text is rendered as SVG
paths, so GitHub needs no external font requests. The existing 12-second
animation cycle is preserved.

Regenerate the three section headings and their panel embeds with:

```sh
python update_headline_fonts.py
python assets/readme-panels/build_panels.py
```
