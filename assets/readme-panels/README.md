# README panels

The Tech Stack heading has a transparent background
so GitHub's page color shows through. The panel's content area starts at
`y=82` with an opaque `#000000` background. GitHub does not retain custom
table background CSS, so this background is part of each local SVG. Mobile
variants reflow the content instead of shrinking the desktop layout.

The content area has matching seven-pixel diagonal cuts in the black
background and the lime border. Two stationary lime highlights sit at the
top-left and bottom-right corners, fading along their adjoining edges.
The glow is clipped to the cut shape. Only the technology strips animate;
reduced-motion variants contain no animation elements.

Internal dividers have stationary lime highlights with a subtle glow. On desktop,
the cross is brightest at its intersection and fades to zero opacity at all four
ends. Mobile separators use the same fade from their center to both endpoints.

The three section headings—My GitHub Analytics, My Tech Stack, and Connect &
Collaborate—use the bundled Pixelify Sans SemiBold font (weight 600) at 26px,
converted to SVG paths by `update_headline_fonts.py` for reliable GitHub rendering. Font
source and regeneration details are in [the font notes](../fonts/pixelify-sans/README.md). They
retain the lime color and existing pixel icons. The icons are embedded from
the assets exported from the supplied [Figma Community icon library](https://www.figma.com/design/SNxwoPfHDsljFF0LvXbtfF/1-300-Free-Pixel-Icons-%E2%80%93-Vector-Pixel-icons--svg---Community-?node-id=1128-1455).
The SVG paths retain the source artwork. Within the tech-stack content area,
the four category symbols and all thirty-one marquee marks use colorful matte 3D
illustrations generated with the built-in imagegen tool. Six transparent PNG
assets are embedded once in each panel, with individual SVG viewports selecting the
icons. The tech stack uses four locally rendered
[README Stack](../readme-stack/README.md) strips with these icons and names.
Adjacent categories scroll in opposite directions at the upstream fast speed (44 SVG pixels per second).
The strips have isolated IDs so their animation, masks, and styles cannot
affect each other. With reduced motion, all thirty-one entries appear as labelled
grids, without edge fading. The README selects separate `-static.svg` files
with no animation elements for this mode. No remote images or fonts are needed
to display these panels. The README image's alt text lists every technology.

Category headings and technology labels use [Alpino](https://www.fontshare.com/fonts/alpino)
by Indian Type Foundry: Bold (700) for headings and moving labels, Medium (500)
for the smaller static labels. Copyright 2016–2021 Indian Type Foundry. All rights
reserved. Font use is governed by [Fontshare's terms](https://www.fontshare.com/terms).
The generator converts the lettering to reusable SVG paths, keeping accessible
labels and the existing spacing. Only the rendered artwork is tracked; the
unmodified TTFs stay in the ignored `.cache/fontshare/` directory.

Regenerate from the repository root with Python and Node.js 22 or newer
(the vendored renderer needs no npm install):

```sh
python -m pip install fonttools
python assets/readme-panels/build_panels.py --download-fonts
```

Subsequent builds can omit `--download-fonts` and run without network access.
Use `--font-dir` to select another local directory containing the two TTFs.

To rebuild the section heading artwork as well, install FontTools and run
`python update_headline_fonts.py` before regenerating the panel.
