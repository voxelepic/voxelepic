"""Rebuild section lettering with Pixelify Sans and existing icons."""

import argparse
from copy import deepcopy
from math import ceil
from pathlib import Path
import xml.etree.ElementTree as ET

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ASSETS = Path(__file__).resolve().parent / "assets"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
HEADLINES = {
    "github_analytics": "My GitHub Analytics",
    "tech_stack": "My Tech Stack",
    "connect": "Connect & Collaborate",
}
FONT_PATH = ASSETS / "fonts" / "pixelify-sans" / "PixelifySans-Variable.ttf"
FONT_SIZE = 26
FONT_WEIGHT = 600
WORD_SPACING = 0
TEXT_X = 38
BASELINE = 32
HEIGHT = 46
LIME = "#bffb4f"


def update_headlines(font_path=FONT_PATH):
    if not font_path.is_file():
        raise FileNotFoundError(
            "The bundled Pixelify Sans font is missing. "
            "Restore it or pass its TTF/OTF file with --font. See assets/fonts/pixelify-sans/README.md."
        )
    with TTFont(font_path) as font:
        glyphs = font.getGlyphSet(location={"wght": FONT_WEIGHT})
        cmap = font.getBestCmap()
        scale = FONT_SIZE / font["head"].unitsPerEm
        for name, label in HEADLINES.items():
            path = ASSETS / f"header_{name}.svg"
            original = ET.parse(path).getroot()
            # The icon is the curated source artwork; replace only the lettering.
            icon = deepcopy(original.find(f"{{{NS}}}g"))
            icon.set("id", "header-icon")
            icon.set("aria-hidden", "true")
            pen = SVGPathPen(glyphs)
            advance = 0
            for character in label:
                glyph = glyphs[cmap[ord(character)]]
                glyph.draw(TransformPen(pen, (scale, 0, 0, -scale,
                                             TEXT_X + advance * scale, BASELINE)))
                advance += glyph.width
                if character == " ":
                    advance += WORD_SPACING / scale
            width = ceil(TEXT_X + advance * scale + 6)
            svg = ET.Element(f"{{{NS}}}svg", {
                "viewBox": f"0 0 {width} {HEIGHT}", "width": str(width), "height": str(HEIGHT),
                "role": "img", "aria-label": label,
            })
            ET.SubElement(svg, f"{{{NS}}}title").text = label
            svg.append(icon)
            # Paths render identically in GitHub image embeds without font loading.
            ET.SubElement(svg, f"{{{NS}}}path", {
                "id": "header-lettering", "d": pen.getCommands(), "fill": LIME,
                "data-font": "Pixelify Sans", "data-weight": str(FONT_WEIGHT),
            })
            ET.indent(svg, space="  ")
            ET.ElementTree(svg).write(path, encoding="utf-8")
    print(f"Updated {len(HEADLINES)} section headings with Pixelify Sans")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=FONT_PATH,
                        help="Pixelify Sans TTF/OTF")
    update_headlines(parser.parse_args().font)
