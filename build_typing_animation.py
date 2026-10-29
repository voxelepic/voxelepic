"""Render the top rotating text in Pixelify Sans while retaining its timing."""
from pathlib import Path
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "assets/fonts/pixelify-sans/PixelifySans-Variable.ttf"
OUTPUT = ROOT / "assets/typing_animation.svg"
LABELS = ["Hey there, I'm Viraj", "Building Things with AI", "Automation & n8n Specialist", "Full-Stack & AI Systems Builder"]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

def main():
    svg = ET.parse(OUTPUT).getroot()
    for group in list(svg.findall(f"{{{NS}}}g")):
        svg.remove(group)
    svg.set("role", "img")
    svg.set("aria-label", "; ".join(LABELS))
    with TTFont(FONT) as font:
        glyphs = font.getGlyphSet(location={"wght":600})
        cmap = font.getBestCmap()
        # Use one scale for every phrase to avoid size changes during the cycle.
        longest = max(sum(glyphs[cmap[ord(c)]].width for c in label) for label in LABELS)
        scale = min(32 / font["head"].unitsPerEm, 442 / longest)
        for index, label in enumerate(LABELS, 1):
            positions = []
            advance = 0
            bounds = BoundsPen(glyphs)
            for char in label:
                glyph = glyphs[cmap[ord(char)]]
                positions.append((glyph, advance))
                glyph.draw(TransformPen(bounds, (1, 0, 0, 1, advance, 0)))
                advance += glyph.width
            left, bottom, right, top = bounds.bounds
            x = 237 - (left+right)*scale/2
            baseline = 26 + (bottom+top)*scale/2
            pen = SVGPathPen(glyphs)
            for glyph, offset in positions:
                glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x+offset*scale, baseline)))
            group = ET.SubElement(svg, f"{{{NS}}}g", {"class":f"line line-{index}"})
            ET.SubElement(group, f"{{{NS}}}path", {"d":pen.getCommands(), "fill":"#bffb4f", "data-font":"Pixelify Sans"})
    ET.indent(svg, space="  ")
    ET.ElementTree(svg).write(OUTPUT, encoding="utf-8")

if __name__ == "__main__":
    main()
