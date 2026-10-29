# Profile hero delivery

The README displays `profile-hero.svg`, which embeds the lossless animated
`profile-hero.webp` and the transparent signature in the card's lower-right
corner. The portrait keeps its original timing and looping; the tilted signature
draws once in 1.4 seconds and stays visible. Pen strokes use the Emil design
engineering skill's `cubic-bezier(0.23, 1, 0.32, 1)` ease-out curve for quick starts
and a soft finish. The SVG is self-contained because GitHub README
images cannot use custom positioning CSS or load external SVG image resources.
No client script is required.

For reduced motion, `<picture>` selects `profile-hero-static.svg`, containing a
still portrait frame and the completed signature. Both variants keep the original
1925 × 720 card dimensions. The signature clears the interests text and border.

After changing the original GIF, regenerate from the repository root:

```sh
python -m pip install Pillow==12.2.0
python build_profile_hero.py
```

After changing only the signature, rebuild the two SVG compositions without
re-encoding the portrait:

```sh
python build_profile_hero.py --signature-only
```

The encoder verifies every decoded pixel and the complete display timeline
against the original GIF, including merged identical frames. Commit the new
WebP and generated SVG compositions together with the original GIF. The hero is manually authored, so it has
no daily data refresh and is not rebuilt by the contribution graph workflow.

The original GIF was 19,603,968 bytes at 1925 × 720, with 195 frames over 6.16
seconds. The verified WebP is 1,051,016 bytes, **94.6% smaller**. A full image
download can be slow even from a CDN. The signed SVG is about 1.41 MB including
the embedded WebP; its reduced-motion counterpart is about 208 KB. The WebP reduces transfer size without a
change in appearance. Actual loading time still depends
on the connection, browser caching and GitHub's asset delivery.

Cloudflare hosting can be added later, using a dedicated subdomain or asset
path with versioned filenames and cache headers. It does not remove GitHub's
[external image proxy](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-anonymized-urls),
so a faster origin alone does not guarantee a faster README. No Cloudflare or
epicvoxel.com settings were changed for this optimization.
