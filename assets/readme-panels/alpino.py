"""Cache official Alpino fonts and render reusable, accessible SVG lettering."""

from pathlib import Path
import re
from urllib.request import urlopen

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT_DIR = Path(__file__).resolve().parents[2] / ".cache" / "fontshare"
FONT_FILES = {500: "Alpino-Medium.ttf", 700: "Alpino-Bold.ttf"}
CSS_URL = "https://api.fontshare.com/v2/css?f[]=alpino@500,700&display=swap"
NS = "{http://www.w3.org/2000/svg}"


def download_fonts(directory=FONT_DIR):
    """Download unmodified TTFs from Fontshare's official stylesheet."""
    directory.mkdir(parents=True, exist_ok=True)
    with urlopen(CSS_URL, timeout=30) as response:
        stylesheet = response.read().decode("utf-8")
    for block in re.findall(r"@font-face\s*\{([^}]+)\}", stylesheet):
        weight = int(re.search(r"font-weight:\s*(\d+)", block)[1])
        if weight not in FONT_FILES:
            continue
        url = re.search(r"url\(['\"](//cdn\.fontshare\.com/[^'\"]+\.ttf)['\"]\)", block)[1]
        with urlopen("https:" + url, timeout=30) as response:
            (directory / FONT_FILES[weight]).write_bytes(response.read())
    for filename in FONT_FILES.values():
        if not (directory / filename).is_file():
            raise RuntimeError(f"Fontshare did not supply {filename}")


def outline_labels(svg, fonts):
    """Reuse each label's path across duplicated tracks and preserve its name."""
    from xml.etree.ElementTree import SubElement

    definitions = SubElement(svg, NS + "defs", {"id": "alpino-label-definitions"})
    labels = {}
    for parent in list(svg.iter()):
        for node in list(parent):
            if node.tag != NS + "text":
                continue
            label = node.text or ""
            size = float(node.get("font-size", "17"))
            weight = 700 if float(node.get("font-weight", "400")) >= 600 else 500
            spacing = float(node.get("letter-spacing", "0"))
            key = (label, size, weight, spacing)
            if key not in labels:
                font = fonts[weight]
                glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
                scale = size / font["head"].unitsPerEm
                pen = SVGPathPen(glyphs)
                cursor = 0
                for character in label:
                    glyph = cmap[ord(character)]
                    glyphs[glyph].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, 0)))
                    cursor += font["hmtx"][glyph][0] * scale + spacing
                identifier = f"alpino-label-{len(labels)}"
                SubElement(definitions, NS + "path", {"id": identifier, "d": pen.getCommands()})
                labels[key] = identifier
            node.tag = NS + "use"
            node.text = None
            for attribute in ("font-family", "font-size", "font-weight", "letter-spacing"):
                node.attrib.pop(attribute, None)
            node.set("href", f"#{labels[key]}")
            node.set("role", "img")
            node.set("aria-label", label)
            node.set("data-font", "Alpino")
            node.set("data-weight", str(weight))
