from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent


def counter_svg(font, value, center_x, color):
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    positions = []
    advance = 0
    bounds = BoundsPen(glyphs)
    for digit in value:
        name = cmap[ord(digit)]
        positions.append((name, advance))
        glyphs[name].draw(TransformPen(bounds, (1, 0, 0, 1, advance, 0)))
        advance += font["hmtx"][name][0]

    # Center the visible outlines, including the font's side bearings.
    x_min, y_min, x_max, y_max = bounds.bounds
    scale = 28 / (y_max - y_min)
    offset_x = center_x - (x_min + x_max) * scale / 2
    baseline = 52 + (y_min + y_max) * scale / 2
    pen = SVGPathPen(glyphs)
    for name, offset in positions:
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, offset_x + offset * scale, baseline)))
    return f'<g role="img" aria-label="{value}" data-counter="{value}"><title>{value}</title><path d="{pen.getCommands()}" fill="{color}"/></g>'

def build_streak_stats():
    with open(ROOT / "assets" / "geist_pixel_triangle.txt", "r", encoding="utf-8") as f:
        font_b64 = f.read().strip()

    with TTFont(ROOT / "assets" / "fonts" / "press-start-2p" / "PressStart2P-Regular.ttf") as number_font:
        total_number = counter_svg(number_font, "158", 180, "#bffb4f")
        current_number = counter_svg(number_font, "0", 540, "#ffffff")
        longest_number = counter_svg(number_font, "7", 900, "#ffffff")

    # 120 pixel-blocks forming the pixelated streak circle ring
    # Shifted down by +8px so center is at (540, 52), spanning y=22 to y=82, x=509 to x=571
    raw_rects = """
      <rect x="509.0" y="44.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="46.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="48.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="50.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="52.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="54.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="56.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="58.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="509.0" y="60.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="511.0" y="40.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="511.0" y="42.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="511.0" y="44.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="511.0" y="60.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="511.0" y="62.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="511.0" y="64.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="513.0" y="36.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="513.0" y="38.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="513.0" y="40.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="513.0" y="64.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="513.0" y="66.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="513.0" y="68.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="515.0" y="34.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="515.0" y="36.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="515.0" y="68.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="515.0" y="70.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="517.0" y="32.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="517.0" y="34.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="517.0" y="70.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="517.0" y="72.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="519.0" y="30.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="519.0" y="32.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="519.0" y="72.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="519.0" y="74.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="521.0" y="28.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="521.0" y="30.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="521.0" y="74.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="521.0" y="76.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="523.0" y="26.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="523.0" y="28.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="523.0" y="76.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="523.0" y="78.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="525.0" y="26.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="525.0" y="78.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="527.0" y="24.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="527.0" y="26.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="527.0" y="78.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="527.0" y="80.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="529.0" y="24.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="529.0" y="80.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="531.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="531.0" y="24.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="531.0" y="80.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="531.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="533.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="533.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="535.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="537.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="539.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="541.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="543.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="545.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="545.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="547.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="547.0" y="24.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="547.0" y="80.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="547.0" y="82.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="549.0" y="24.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="549.0" y="80.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="551.0" y="24.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="551.0" y="26.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="551.0" y="78.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="551.0" y="80.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="553.0" y="26.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="553.0" y="78.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="555.0" y="26.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="555.0" y="28.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="555.0" y="76.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="555.0" y="78.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="557.0" y="28.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="557.0" y="30.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="557.0" y="74.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="557.0" y="76.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="559.0" y="30.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="559.0" y="32.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="559.0" y="72.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="559.0" y="74.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="561.0" y="32.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="561.0" y="34.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="561.0" y="70.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="561.0" y="72.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="563.0" y="34.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="563.0" y="36.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="563.0" y="68.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="563.0" y="70.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="565.0" y="36.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="565.0" y="38.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="565.0" y="40.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="565.0" y="64.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="565.0" y="66.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="565.0" y="68.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="567.0" y="40.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="567.0" y="42.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="567.0" y="44.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="567.0" y="60.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="567.0" y="62.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="567.0" y="64.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="44.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="46.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="48.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="50.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="52.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="54.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="56.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="58.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="569.0" y="60.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="535.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="537.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="539.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="541.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
      <rect x="543.0" y="22.0" width="2.0" height="2.0" fill="#1f242c"/>
"""

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 140" width="1080" height="140" preserveAspectRatio="xMidYMid meet" style="background: #000000; border-radius: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; width: 100%; height: auto; display: block;">
  <defs>
    <style>
      @font-face {{
        font-family: 'GeistPixelTriangle';
        src: url('data:font/woff2;charset=utf-8;base64,{font_b64}') format('woff2');
        font-weight: normal;
        font-style: normal;
      }}
      .pixel-label {{
        font-family: 'GeistPixelTriangle', monospace;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1.4px;
      }}
      .pixel-sub {{
        font-family: 'GeistPixelTriangle', monospace;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 0.8px;
      }}
    </style>
    <linearGradient id="divGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#161b22" stop-opacity="0.1"/>
      <stop offset="50%" stop-color="#bffb4f" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#161b22" stop-opacity="0.1"/>
    </linearGradient>
  </defs>

  <!-- Pitch Black Base Card with subtle border -->
  <rect width="1080" height="140" rx="12" fill="#000000"/>
  <rect width="1080" height="140" rx="12" fill="none" stroke="#161b22" stroke-width="1"/>

  <!-- Vertical Divider Lines with Cyber Glow -->
  <line x1="360" y1="16" x2="360" y2="124" stroke="url(#divGrad)" stroke-width="1.5"/>
  <line x1="720" y1="16" x2="720" y2="124" stroke="url(#divGrad)" stroke-width="1.5"/>

  <!-- Column 1: Total Contributions -->
  <g id="col-total">
    {total_number}
    <text x="180" y="102" fill="#f0f6fc" class="pixel-label" text-anchor="middle">TOTAL CONTRIBUTIONS</text>
    <text x="180" y="122" fill="#38bdf8" class="pixel-sub" text-anchor="middle">Aug 24, 2025 – Present</text>
  </g>

  <!-- Column 2: Current Streak -->
  <g id="col-current">
    <!-- Pixelated Circle Ring (Centered at 540, 52) -->
    <g id="pixel-circle-ring">
{raw_rects}
    </g>
    
    <!-- Pixel Flame Icon (sits above circle top at y=22) -->
    <g id="pixel-flame" transform="translate(536, 8)">
      <rect x="3" y="0" width="2" height="2" fill="#bffb4f"/>
      <rect x="2" y="2" width="4" height="2" fill="#bffb4f"/>
      <rect x="1" y="4" width="6" height="2" fill="#bffb4f"/>
      <rect x="2" y="6" width="4" height="2" fill="#bffb4f"/>
      <rect x="2" y="8" width="4" height="2" fill="#bffb4f"/>
      <rect x="3" y="10" width="2" height="2" fill="#bffb4f"/>
    </g>

    <!-- Press Start 2P outlines centered in the existing ring. -->
    {current_number}
    <text x="540" y="102" fill="#bffb4f" class="pixel-label" text-anchor="middle">CURRENT STREAK</text>
    <text x="540" y="122" fill="#8b949e" class="pixel-sub" text-anchor="middle">Live: Aug 30</text>
  </g>

  <!-- Column 3: Longest Streak -->
  <g id="col-longest">
    {longest_number}
    <text x="900" y="102" fill="#f0f6fc" class="pixel-label" text-anchor="middle">LONGEST STREAK</text>
    <text x="900" y="122" fill="#38bdf8" class="pixel-sub" text-anchor="middle">Jun 25 – Jul 01</text>
  </g>
</svg>
'''
    with open(ROOT / "assets" / "streak_stats.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Generated streak_stats.svg with Press Start 2P counter outlines")

if __name__ == "__main__":
    build_streak_stats()
