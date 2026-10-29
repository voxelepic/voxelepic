"""Build README panels with local README Stack strips and moving lime edges."""

from copy import deepcopy
import argparse
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from fontTools.ttLib import TTFont

from alpino import FONT_DIR, FONT_FILES, download_fonts, outline_labels

OUTPUT = Path(__file__).resolve().parent
ASSETS = OUTPUT.parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
WHITE = "#f0f3ed"
LIME = "#bffb4f"

GROUPS = [
    ("AI & Automation", "robot", [
        ("n8n", "#ff6d5a"), ("LangChain", "#22c55e"),
        ("Autonomous Agents", "#a855f7"), ("LLM Orchestration", "#ec4899"),
        ("ComfyUI", "#f3ff4f"),
    ]),
    ("Languages & Core", "code", [
        ("Python", "#38bdf8"), ("TypeScript", "#60a5fa"),
        ("JavaScript", "#facc15"), ("SQL", "#2dd4bf"),
    ]),
    ("Cloud & Infrastructure", "globe", [
        ("Cloudflare", "#fb923c"), ("Docker", "#38bdf8"),
        ("Serverless", "#f43f5e"), ("REST / GraphQL", "#e879f9"),
        ("Google Cloud", "#4285f4"), ("Azure", "#0089d6"),
        ("Firebase", "#ff9100"), ("Supabase", "#3ecf8e"),
    ]),
    ("Tools & Ecosystem", "design", [
        ("Git", "#f97316"), ("Linux", "#fbbf24"),
        ("Figma", "#c084fc"), ("Postman", "#ff7849"),
        ("Codex", "#eae5d9"), ("Claude", "#d97757"),
        ("Antigravity", "#4285f4"), ("Affinity", "#aff078"),
        ("Android Studio", "#3ddc84"), ("Blender", "#e87d0d"),
        ("FL Studio", "#ff9900"),
        ("Roblox Studio", "#00a2ff"), ("MetaTrader 5", "#46a65a"),
        ("TradingView", "#2962ff"),
    ]),
]


def element(parent, tag, **attributes):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {name.replace("_", "-"): str(value) for name, value in attributes.items()})


def body_outline(width, height, inset=0):
    """Use the same seven-pixel corner cuts for the body, clip, and border."""
    left, top, right, bottom = inset, 82+inset, width-inset, height-inset
    bevel = 7-inset*(2-2**0.5)
    return (f"M{left+bevel:g} {top:g} H{right-bevel:g} L{right:g} {top+bevel:g} "
            f"V{bottom-bevel:g} L{right-bevel:g} {bottom:g} H{left+bevel:g} "
            f"L{left:g} {bottom-bevel:g} V{top+bevel:g} Z")


def panel(width, height, title, description):
    svg = ET.Element(f"{{{NS}}}svg", {
        "width": str(width), "height": str(height), "viewBox": f"0 0 {width} {height}",
        "role": "img", "aria-labelledby": "panel-title panel-description",
    })
    element(svg, "title", id="panel-title").text = title
    element(svg, "desc", id="panel-description").text = description
    # Leave the section heading transparent so it uses GitHub's page background.
    element(svg, "path", id="panel-body-background", d=body_outline(width, height), fill="#000000")
    edge_frame(svg, width, height)
    return svg


def edge_frame(parent, width, height):
    """Frame the content, leaving the transparent heading and text clear."""
    # Half the core stroke width keeps the line flush with the cut black body.
    left, top, right, bottom = 0.625, 82.625, width-0.625, height-0.625
    bevel = 7-0.625*(2-2**0.5)
    body_height = bottom-top
    outline = body_outline(width, height, inset=0.625)
    defs = element(parent, "defs")
    clip = element(defs, "clipPath", id="frame-body-clip")
    element(clip, "path", d=body_outline(width, height))
    glow = element(defs, "filter", id="frame-glow", x="-10%", y="-10%", width="120%", height="120%",
                   color_interpolation_filters="sRGB")
    element(glow, "feGaussianBlur", stdDeviation="1.5")
    for name, x, y in [("upper", left, top), ("lower", right, bottom)]:
        gradient = element(defs, "radialGradient", id=f"frame-{name}", gradientUnits="userSpaceOnUse",
                           cx="0", cy="0", r="1",
                           gradientTransform=f"translate({x} {y}) scale({width*0.44:g} {body_height*0.64:g})")
        for offset, opacity in [("0", "1"), ("0.2", "0.85"), ("0.65", "0.25"), ("1", "0")]:
            element(gradient, "stop", offset=offset, stop_color=LIME, stop_opacity=opacity)
    frame = element(parent, "g", id="panel-edge-frame", aria_hidden="true", fill="none",
                    pointer_events="none", clip_path="url(#frame-body-clip)")
    element(frame, "path", d=outline, stroke=LIME, stroke_opacity="0.1", stroke_width="0.75")
    stationary = element(frame, "g", id="frame-stationary")
    corners = [
        ("upper", f"M{left+width*0.44:g} {top} H{left+bevel:g} L{left} {top+bevel:g} V{top+body_height*0.64:g}"),
        ("lower", f"M{right} {bottom-body_height*0.64:g} V{bottom-bevel:g} L{right-bevel:g} {bottom} H{right-width*0.44:g}"),
    ]
    for name, commands in corners:
        element(stationary, "path", d=commands, stroke=f"url(#frame-{name})", stroke_width="4",
                opacity="0.3", filter="url(#frame-glow)")
        element(stationary, "path", d=commands, stroke=f"url(#frame-{name})", stroke_width="1.25")


def embed(parent, source, x, y, width, height):
    svg = deepcopy(ET.parse(source).getroot())
    svg.set("x", str(x))
    svg.set("y", str(y))
    svg.set("width", str(width))
    svg.set("height", str(height))
    parent.append(svg)


def heading(parent, source, width):
    original = ET.parse(source).getroot()
    native_width = float(original.get("width"))
    embed(parent, source, (width - native_width) / 2, 20, native_width, 46)


def text(parent, label, x, y, size=17, color=WHITE, weight="400"):
    node = element(parent, "text", x=x, y=y, fill=color, font_size=size,
                   font_family="Arial, Helvetica, sans-serif", font_weight=weight)
    node.text = label


def stack_strip(parent, markup, index, x, y, width):
    strip = ET.fromstring(markup)
    # Nested SVGs share an ID space in an image. Isolate masks and style selectors.
    identifiers = {node.get("id"): f"stack-{index}-{node.get('id')}"
                   for node in strip.iter() if node.get("id")}
    for node in strip.iter():
        if node.get("id"):
            node.set("id", identifiers[node.get("id")])
        for key, value in list(node.attrib.items()):
            for old, new in identifiers.items():
                value = value.replace(f"url(#{old})", f"url(#{new})")
                if value == f"#{old}":
                    value = f"#{new}"
            node.set(key, value)
        if node.tag == f"{{{NS}}}style":
            for old, new in identifiers.items():
                node.text = node.text.replace(f"#{old}", f"#{new}")
    strip.attrib.update(x=str(x), y=str(y), width=str(width), **{"data-stack-category": str(index)})
    parent.append(strip)


def divider_highlight(parent, name, x1, y1, x2, y2, focus=0.5):
    """Fade a stationary lime divider completely out at both endpoints."""
    defs = element(parent, "defs")
    gradient_id = f"divider-{name}"
    gradient = element(defs, "linearGradient", id=gradient_id,
                       gradientUnits="userSpaceOnUse", x1=x1, y1=y1, x2=x2, y2=y2)
    for offset, opacity in [(0, 0), (focus / 2, 0.18), (focus, 0.85),
                            ((1 + focus) / 2, 0.18), (1, 0)]:
        element(gradient, "stop", offset=f"{offset:g}", stop_color=LIME, stop_opacity=opacity)
    group = element(parent, "g", aria_hidden="true", pointer_events="none", fill="none",
                    stroke=f"url(#{gradient_id})")
    commands = f"M{x1} {y1}L{x2} {y2}"
    element(group, "path", d=commands, stroke_width="3", opacity="0.2", filter="url(#frame-glow)")
    element(group, "path", d=commands, stroke_width="1")


def tech_stack(stacks, mobile, static=False):
    width, height = (400, 674) if mobile else (900, 424)
    variant = ("mobile" if mobile else "desktop") + ("-static" if static else "")
    strip_heights = [int(ET.fromstring(markup).get("height")) for markup in stacks[variant]]
    if mobile:
        height += sum(strip_height - 92 for strip_height in strip_heights)
    else:
        height += sum(max(strip_heights[row:row+2]) - 92 for row in range(0, len(GROUPS), 2))
    svg = panel(width, height, "My Tech Stack", "; ".join(
        f"{name}: {', '.join(label for label, _ in labels)}" for name, _, labels in GROUPS))
    svg.append(ET.fromstring(stacks["iconDefinitions"]))
    heading(svg, ASSETS / "header_tech_stack.svg", width)
    if not mobile:
        row_divider_y = 98 + max(strip_heights[:2]) + 56
        divider_highlight(svg, "vertical", 450, 94, 450, height-26,
                          focus=(row_divider_y-94)/(height-26-94))
        divider_highlight(svg, "horizontal", 32, row_divider_y, 868, row_divider_y)
    for index, (name, icon_name, labels) in enumerate(GROUPS):
        x = 28 if mobile else 32 + (index % 2) * 450
        y = (92 + sum(strip_height + 52 for strip_height in strip_heights[:index]) if mobile
             else 98 + sum(max(strip_heights[row:row+2]) + 70 for row in range(0, index-1, 2)))
        if mobile and index:
            divider_highlight(svg, f"mobile-{index}", 28, y-18, 372, y-18)
        heading_icon = ["autonomous-agents", "typescript", "cloudflare", "figma"][index]
        element(svg, "use", href=f"#tech-icon-{heading_icon}", x=x-2, y=y-3, width=30, height=30,
                aria_hidden="true")
        text(svg, name, x+36, y+19, 18 if mobile else 19, weight="600")
        stack_strip(svg, stacks[variant][index], index, x, y+34, 344 if mobile else 386)
    return svg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", type=Path, default=FONT_DIR, help="Directory containing Alpino Bold and Medium TTFs")
    parser.add_argument("--download-fonts", action="store_true", help="Cache Alpino from the official Fontshare CDN first")
    args = parser.parse_args()
    if args.download_fonts:
        download_fonts(args.font_dir)
    if any(not (args.font_dir / name).is_file() for name in FONT_FILES.values()):
        parser.error("Alpino fonts are missing; run this script with --download-fonts first.")
    rendered = subprocess.run(["node", str(ASSETS / "readme-stack" / "build_stacks.mjs")],
                              check=True, capture_output=True, encoding="utf-8")
    stacks = json.loads(rendered.stdout)
    with TTFont(args.font_dir / FONT_FILES[700]) as bold, TTFont(args.font_dir / FONT_FILES[500]) as medium:
        for mobile in (False, True):
            for static in (False, True):
                svg = tech_stack(stacks, mobile, static)
                outline_labels(svg, {700: bold, 500: medium})
                ET.indent(svg, space="  ")
                suffix = ("-mobile" if mobile else "") + ("-static" if static else "")
                ET.ElementTree(svg).write(OUTPUT / f"tech-stack{suffix}.svg", encoding="utf-8")
    print("Generated animated/still tech stacks with stationary top-left and bottom-right lime edges")


if __name__ == "__main__":
    main()
