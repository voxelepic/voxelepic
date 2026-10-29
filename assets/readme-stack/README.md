# README Stack integration

The tech-stack panel uses a local adaptation of
[rajin-khan/readme-stack](https://github.com/rajin-khan/readme-stack).
The renderer and configuration module are vendored, along with only the twelve
catalog entries used in this profile. Generated SVGs contain their own icons,
so displaying the README does not contact the upstream service.

The four original categories remain intact. Each strip scrolls at 44 SVG
pixels per second, alternating direction between columns/rows. The original
duplicated-track mechanism provides a continuous loop. The panel's cut black
background and transparent heading are preserved. Stationary lime edge accents
sit at the top-left and bottom-right corners.

## Local adaptations

- Configurable strip width and black background to fit the existing panel.
- A two-column grid with every tool name for reduced motion, placed outside the
  edge-fade mask so stationary content is fully visible.
- Colorful matte 3D illustrations for all thirty-one entries, generated with the
  built-in imagegen tool. Autonomous Agents, LLM Orchestration, Serverless,
  and REST / GraphQL retain neutral capability symbols.
- Seven transparent PNG assets ([original tools](matte/tech-icons.png),
  [additional tools](matte/tools-extra.png), [cloud platforms](matte/cloud-extra.png),
  [ComfyUI](matte/comfyui.png), [Studio/trading tools](matte/studio-trading-extra.png),
  [Supabase](matte/supabase.png), and [Codex](matte/codex.png)), each embedded once in every
  combined panel. `tech-icons.mjs` defines measured SVG viewports for each
  silhouette and supplies the renderer overrides. No remote images are loaded.
- Larger matte marks in the moving strips and static grids. The four category
  headings reuse matching matte illustrations in place of their lime symbols.
- Tools & Ecosystem contains Git, Linux, Figma, Postman, Codex, Claude,
  Antigravity, Affinity, Android Studio, Blender, FL Studio, Roblox Studio,
  MetaTrader 5, and TradingView. Additional entries live in `local-tools.mjs`,
  preserving the upstream catalog snapshot.
  Reduced-motion panels expand to fit seven rows at the original readable size;
  the animated strips retain their original dimensions and speed.
- Cloud & Infrastructure also includes Google Cloud, Azure, Firebase, and Supabase.
  Its reduced-motion grid has four rows; mobile sections reflow according to
  their actual strip heights so the expanded categories cannot overlap.
- AI & Automation also includes ComfyUI. Its reduced-motion grid has three rows;
  the desktop row divider follows the tallest category in the first row.
- Unique IDs per category when embedding SVGs in the combined panel.
- Separate static SVGs selected by the README's `picture` sources for reduced
  motion, in addition to the renderer's own media query. These files contain
  no animation elements, avoiding hidden-animation repaint bugs in browsers.

Run `python assets/readme-panels/build_panels.py` from the repository root with
Python, FontTools, Node.js 22+, and the locally cached Alpino fonts (see the
[panel build instructions](../readme-panels/README.md)). No npm packages are required. The Node helper
`build_stacks.mjs` writes the category/viewport/motion SVG strings to stdout;
the Python generator embeds them and the shared icon definitions in desktop,
mobile, and still panels. Open [the local preview](matte/preview.html) through
an HTTP server to review all four versions. The exact generation prompt is
saved in [generation-prompt.md](matte/generation-prompt.md), with the seven
additional icons documented in [tools-generation-prompt.md](matte/tools-generation-prompt.md).
The cloud additions are documented in [cloud-generation-prompt.md](matte/cloud-generation-prompt.md).
The ComfyUI addition is documented in [comfyui-generation-prompt.md](matte/comfyui-generation-prompt.md).
The latest Tools & Ecosystem additions are documented in [studio-trading-generation-prompt.md](matte/studio-trading-generation-prompt.md).
The Supabase addition is documented in [supabase-generation-prompt.md](matte/supabase-generation-prompt.md).

## Provenance and attribution

Snapshot retrieved on 2026-10-29 from the upstream `main` branch:

| Source | Upstream Git blob SHA |
| --- | --- |
| `src/render.js` | `1da810e9d7f8bafb75812727028e27744c552b25` |
| `src/config.js` | `4303a2a4b6a70e9a5dd0ea0dc18f586bb1c94540` |
| `public/catalog.json` (twelve selected entries) | `419239b7e31b2bb2edef3f4ab5e5a9ae093c25db` |

README Stack is Copyright (c) 2026 Rajin Khan, distributed under the
[MIT License](LICENSE). Local changes are described above. The complete supplied
[upstream third-party notices](UPSTREAM_NOTICES.md) are retained for reference.
Each selected catalog entry retains its provider, source URL, and rights data;
generated strips retain upstream metadata and asset notices.

The retained fallback catalog icons come from Simple Icons 16.28.0, except SQL,
which is an upstream neutral glyph. The fallback Git icon is licensed under
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/), with attribution to
Simple Icons 16.28.0 and the [Git logo source](https://git-scm.com/community/logos).
The JavaScript icon carries an MIT license notice in the source catalog.
Their source paths are preserved in the vendored catalog. The current panels
display generated matte 3D interpretations through explicit renderer overrides;
these are stylized illustrations, not official brand artwork.
Names and marks identify their corresponding tools and do not imply endorsement.
