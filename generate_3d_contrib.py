import os
import sys
import json
import math
import re
import xml.etree.ElementTree as ET
import subprocess
import urllib.request
from datetime import date
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

WEEK_STEP = (15.2, 5.2)
DAY_STEP = (7.6, -4.2)
CELL_FILL_RATIO = 0.72



def alpino_legend(markup):
    """Outline only the four language legend labels with Alpino Medium."""
    sys.path.insert(0, str(Path(__file__).resolve().parent / "assets" / "readme-panels"))
    from alpino import FONT_DIR, FONT_FILES, outline_labels
    labels = re.findall(r'<text\b[^>]*>(?:Python|TypeScript|n8n / Workflows|JavaScript)</text>', markup)
    if len(labels) != 4:
        raise ValueError("Expected four language legend labels")
    legend = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(labels) + '</svg>')
    with TTFont(FONT_DIR / FONT_FILES[500]) as font:
        outline_labels(legend, {500: font})
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    for original, node in zip(labels, list(legend)[:4]):
        node.attrib.pop('class', None)
        markup = markup.replace(original, ET.tostring(node, encoding='unicode'), 1)
    definitions = ET.tostring(list(legend)[-1], encoding='unicode')
    return markup.replace('</svg>', definitions + '</svg>')


def date_range_badge(date_range):
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    start, end = [date.fromisoformat(value.replace(".", "-")) for value in date_range.split(" — ")]
    label = " – ".join(f"{value.day:02d} {months[value.month - 1]} {value.year}" for value in (start, end))
    font_path = Path(__file__).resolve().parent / "assets" / "fonts" / "pixelify-sans" / "PixelifySans-Variable.ttf"
    with TTFont(font_path) as font:
        glyphs = font.getGlyphSet(location={"wght": 500})
        cmap = font.getBestCmap()
        bounds = BoundsPen(glyphs)
        positions = []
        advance = 0
        for character in label:
            name = cmap[ord(character)]
            positions.append((name, advance))
            glyphs[name].draw(TransformPen(bounds, (1, 0, 0, 1, advance, 0)))
            advance += glyphs[name].width
        x_min, y_min, x_max, y_max = bounds.bounds
        scale = 14 / font["head"].unitsPerEm
        width = max(240, math.ceil((x_max - x_min) * scale + 28))
        offset_x = width / 2 - (x_min + x_max) * scale / 2
        baseline = 16 + (y_min + y_max) * scale / 2
        pen = SVGPathPen(glyphs)
        for name, offset in positions:
            glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, offset_x + offset * scale, baseline)))

    return f'''<g id="date-range" transform="translate({1052 - width}, 16)" role="img" aria-label="{label}">
    <title>{label}</title>
    <path d="{pen.getCommands()}" fill="#dce5d4"/>
  </g>'''


def day_footprint(cx, cy):
    """Inset a day cell within the projected calendar lattice."""
    ux, uy = (value * CELL_FILL_RATIO / 2 for value in WEEK_STEP)
    vx, vy = (value * CELL_FILL_RATIO / 2 for value in DAY_STEP)
    return (
        (cx - ux + vx, cy - uy + vy),
        (cx + ux + vx, cy + uy + vy),
        (cx + ux - vx, cy + uy - vy),
        (cx - ux - vx, cy - uy - vy),
    )


def svg_point(point):
    return f"{point[0]:.1f},{point[1]:.1f}"


def get_font_base64():
    """Load GeistPixelTriangle from the bundled profile asset."""
    font_path = Path(__file__).resolve().parent / "assets" / "geist_pixel_triangle.txt"
    return font_path.read_text(encoding="utf-8").strip()

def fetch_github_data(target_username="voxelepic"):
    """Fetch live contribution calendar, stats, and languages from GitHub."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    
    query = """query($u: String!) {
      user(login: $u) {
        login
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          nodes {
            name
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node {
                  name
                  color
                }
              }
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalPullRequestReviewContributions
          totalRepositoriesWithContributedCommits
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
              }
            }
          }
        }
      }
    }"""
    
    try:
        cmd = ["gh", "api", "graphql", "-F", f"u={target_username}", "-f", f"query={query}"]
        res = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        data = json.loads(res.decode('utf-8'))
        if "data" in data and data["data"].get("user"):
            return data["data"]["user"]
    except Exception:
        pass

    if token:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"u": target_username}}).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "GitHub-3D-Contrib"
            }
        )
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                if "data" in data and data["data"].get("user"):
                    return data["data"]["user"]
        except Exception as e:
            print(f"GraphQL request error: {e}")

    return None

def build_3d_svg(user_data):
    if user_data and "contributionsCollection" in user_data:
        col = user_data["contributionsCollection"]
        cal = col["contributionCalendar"]
        weeks_data = cal["weeks"]
        total_contributions = cal["totalContributions"]
        commits = col.get("totalCommitContributions", 16)
        issues = col.get("totalIssueContributions", 2)
        prs = col.get("totalPullRequestContributions", 1)
        reviews = col.get("totalPullRequestReviewContributions", 0)
        repos = col.get("totalRepositoriesWithContributedCommits", 5)
    else:
        raise ValueError("Real contribution calendar required; keeping the existing assets")

    # Get start and end date
    if weeks_data and weeks_data[0].get("contributionDays") and weeks_data[-1].get("contributionDays"):
        start_date = weeks_data[0]["contributionDays"][0]["date"].replace("-", ".")
        end_date = weeks_data[-1]["contributionDays"][-1]["date"].replace("-", ".")
        date_str = f"{start_date} — {end_date}"
    else:
        date_str = "2025.08.31 — 2026.08.31"

    # Tech stack slices
    tech_slices = [
        {"name": "Python", "color": "#bffb4f", "pct": 52},
        {"name": "TypeScript", "color": "#38bdf8", "pct": 24},
        {"name": "n8n / Workflows", "color": "#f43f5e", "pct": 14},
        {"name": "JavaScript", "color": "#facc15", "pct": 10},
    ]

    # Compact SVG dimensions
    svg_w = 1080
    svg_h = 370
    y_offset = -8.0

    # Collect all cells
    all_cells = []
    for w_idx, week in enumerate(weeks_data):
        for day in week.get("contributionDays", []):
            d_idx = day.get("weekday", 0)
            count = day.get("contributionCount", 0)
            
            cx = 24.4 + w_idx * WEEK_STEP[0] + d_idx * DAY_STEP[0]
            cy = 84.0 + y_offset + w_idx * WEEK_STEP[1] + d_idx * DAY_STEP[1]
            
            all_cells.append({
                "w": w_idx,
                "d": d_idx,
                "count": count,
                "date": day.get("date", ""),
                "cx": cx,
                "cy": cy
            })

    # Sort strictly by cy ascending (painter's algorithm depth sort)
    all_cells.sort(key=lambda c: (c["cy"], c["cx"]))

    # Generate isometric grid polygons
    grid_polygons = []
    for cell in all_cells:
        cx = cell["cx"]
        cy = cell["cy"]
        count = cell["count"]

        footprint = day_footprint(cx, cy)
        p_top, p_right, p_bottom, p_left = map(svg_point, footprint)

        if count == 0:
            poly = f'<g class="cell empty"><polygon points="{p_top} {p_right} {p_bottom} {p_left}" fill="#0e131a" stroke="#18202c" stroke-width="0.5"/></g>'
            grid_polygons.append(poly)
        else:
            if count <= 2:
                h = 10.0 + count * 3.0
                lvl = "lvl-1"
                c_left = "#0d3319"
                c_right = "#082211"
                c_top = "#155328"
            elif count <= 5:
                h = 20.0 + count * 3.5
                lvl = "lvl-2"
                c_left = "#155026"
                c_right = "#0e381b"
                c_top = "#2ea043"
            elif count <= 9:
                h = 36.0 + count * 3.0
                lvl = "lvl-3"
                c_left = "#247e3e"
                c_right = "#17572a"
                c_top = "#4bc557"
            else:
                h = 50.0 + min(count * 2.5, 34.0)
                lvl = "lvl-4"
                c_left = "#3ebd68"
                c_right = "#298548"
                c_top = "#bffb4f"

            t_top, t_right, t_bottom, t_left = (
                svg_point((x, y - h)) for x, y in footprint
            )

            left_poly = f'<polygon points="{p_left} {t_left} {t_bottom} {p_bottom}" fill="{c_left}" />'
            right_poly = f'<polygon points="{p_bottom} {t_bottom} {t_right} {p_right}" fill="{c_right}" />'
            # Keep bright caps crisp so glow cannot fill the day-to-day gutters.
            top_poly = f'<polygon points="{t_top} {t_right} {t_bottom} {t_left}" fill="{c_top}"/>'

            grid_polygons.append(f'<g class="cell bar {lvl}">{left_poly}{right_poly}{top_poly}</g>')

    grid_svg = "\n    ".join(grid_polygons)

    # Radar Chart (Adjusted center for clean clearance below pill)
    radar_cx, radar_cy = 930.0, 160.0
    angles = [-90, -18, 54, 126, 198]
    
    def val_to_r(val, max_val=100):
        if val <= 0:
            return 14.0
        norm = math.log10(val + 1) / math.log10(max_val + 1)
        return max(16.0, min(70.0, 16.0 + norm * 54.0))

    r_commit = val_to_r(max(commits, 25), 1000)
    r_issue = val_to_r(max(issues, 8), 100)
    r_pr = val_to_r(max(prs, 15), 100)
    r_review = val_to_r(max(reviews, 5), 100)
    r_repo = val_to_r(max(repos, 12), 50)

    radii = [r_commit, r_issue, r_pr, r_review, r_repo]
    radar_points = []
    radar_circles = []
    for angle_deg, r in zip(angles, radii):
        rad = math.radians(angle_deg)
        x = radar_cx + r * math.cos(rad)
        y = radar_cy + r * math.sin(rad)
        radar_points.append(f"{x:.1f},{y:.1f}")
        radar_circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#bffb4f" stroke="#000000" stroke-width="1.5"/>')

    radar_pts_str = " ".join(radar_points)
    radar_dots_str = "\n    ".join(radar_circles)

    # Donut Chart (Adjusted center)
    donut_cx, donut_cy = 95.0, 280.0
    r_out, r_in = 46.0, 26.0
    
    donut_paths = []
    accum_pct = 0.0
    for sl in tech_slices:
        pct = sl["pct"]
        start_angle = (accum_pct / 100.0) * 360.0 - 90.0
        end_angle = ((accum_pct + pct) / 100.0) * 360.0 - 90.0
        accum_pct += pct

        rad1 = math.radians(start_angle)
        rad2 = math.radians(end_angle)

        x1_out = donut_cx + r_out * math.cos(rad1)
        y1_out = donut_cy + r_out * math.sin(rad1)
        x2_out = donut_cx + r_out * math.cos(rad2)
        y2_out = donut_cy + r_out * math.sin(rad2)

        x1_in = donut_cx + r_in * math.cos(rad1)
        y1_in = donut_cy + r_in * math.sin(rad1)
        x2_in = donut_cx + r_in * math.cos(rad2)
        y2_in = donut_cy + r_in * math.sin(rad2)

        large_arc = 1 if pct > 50 else 0
        path_d = f"M {x1_out:.2f} {y1_out:.2f} A {r_out} {r_out} 0 {large_arc} 1 {x2_out:.2f} {y2_out:.2f} L {x2_in:.2f} {y2_in:.2f} A {r_in} {r_in} 0 {large_arc} 0 {x1_in:.2f} {y1_in:.2f} Z"
        donut_paths.append(f'<path d="{path_d}" fill="{sl["color"]}" stroke="#000000" stroke-width="1.5"/>')

    donut_paths_str = "\n    ".join(donut_paths)

    # Pixelated Legend text
    donut_legend = []
    for idx, sl in enumerate(tech_slices):
        y_pos = idx * 19
        donut_legend.append(f'''<rect x="0" y="{y_pos}" width="10" height="10" rx="2" fill="{sl["color"]}"/>
      <text x="18" y="{y_pos + 9}" fill="#f0f6fc" font-size="12" class="pixel-text">{sl["name"]}</text>''')

    donut_legend_str = "\n      ".join(donut_legend)

    # Load embedded pixel font
    font_b64 = get_font_base64()

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" preserveAspectRatio="xMidYMid meet" style="background: #000000; border-radius: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; width: 100%; height: auto; display: block;">
  <defs>
    <!-- Pixel Typography Style -->
    <style>
      @font-face {{
        font-family: 'GeistPixelTriangle';
        src: url('data:font/woff2;charset=utf-8;base64,{font_b64}') format('woff2');
        font-weight: normal;
        font-style: normal;
      }}
      .pixel-text {{
        font-family: 'GeistPixelTriangle', monospace;
        letter-spacing: 0.5px;
      }}
    </style>

    <!-- Cyber Neon Lime Glow Filter -->
    <filter id="glowLime" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <filter id="subtleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#bffb4f" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#00ff88" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="bottomBeamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#bffb4f" stop-opacity="0"/>
      <stop offset="20%" stop-color="#bffb4f" stop-opacity="0"/>
      <stop offset="40%" stop-color="#bffb4f" stop-opacity="0.7"/>
      <stop offset="50%" stop-color="#bffb4f" stop-opacity="1"/>
      <stop offset="60%" stop-color="#bffb4f" stop-opacity="0.7"/>
      <stop offset="80%" stop-color="#bffb4f" stop-opacity="0"/>
      <stop offset="100%" stop-color="#bffb4f" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Pitch Black Base Card -->
  <rect width="{svg_w}" height="{svg_h}" rx="12" fill="#000000"/>
  <rect width="{svg_w}" height="{svg_h}" rx="12" fill="none" stroke="#161b22" stroke-width="1"/>

  <!-- Border Beam — single straight glowing line, transparent at edges so no corner curves -->
  <rect x="0" y="366" width="{svg_w}" height="3" fill="url(#bottomBeamGrad)"/>

  <!-- Top Right Date Header Pill -->
  {date_range_badge(date_str)}

  <!-- 3D Isometric Calendar Grid -->
  <g id="isometric-grid">
    {grid_svg}
  </g>

  <!-- Radar Chart Widget (Top Right) -->
  <g id="radar-chart" transform="translate(0, 0)">
    <!-- Concentric Guidelines -->
    <polygon points="{radar_cx},{radar_cy - 18.8} {radar_cx + 17.8},{radar_cy - 5.8} {radar_cx + 11.0},{radar_cy + 15.2} {radar_cx - 11.0},{radar_cy + 15.2} {radar_cx - 17.8},{radar_cy - 5.8}" fill="none" stroke="#1c2330" stroke-width="1" stroke-dasharray="2,3"/>
    <polygon points="{radar_cx},{radar_cy - 37.5} {radar_cx + 35.7},{radar_cy - 11.6} {radar_cx + 22.0},{radar_cy + 30.3} {radar_cx - 22.0},{radar_cy + 30.3} {radar_cx - 35.7},{radar_cy - 11.6}" fill="none" stroke="#1c2330" stroke-width="1" stroke-dasharray="2,3"/>
    <polygon points="{radar_cx},{radar_cy - 56.2} {radar_cx + 53.5},{radar_cy - 17.4} {radar_cx + 33.1},{radar_cy + 45.5} {radar_cx - 33.1},{radar_cy + 45.5} {radar_cx - 53.5},{radar_cy - 17.4}" fill="none" stroke="#222b3a" stroke-width="1" stroke-dasharray="2,3"/>
    <polygon points="{radar_cx},{radar_cy - 75.0} {radar_cx + 71.3},{radar_cy - 23.2} {radar_cx + 44.1},{radar_cy + 60.7} {radar_cx - 44.1},{radar_cy + 60.7} {radar_cx - 71.3},{radar_cy - 23.2}" fill="none" stroke="#2d3748" stroke-width="1"/>

    <!-- Axis Spokes -->
    <line x1="{radar_cx}" y1="{radar_cy}" x2="{radar_cx}" y2="{radar_cy - 75.0}" stroke="#222b3a" stroke-width="1"/>
    <line x1="{radar_cx}" y1="{radar_cy}" x2="{radar_cx + 71.3}" y2="{radar_cy - 23.2}" stroke="#222b3a" stroke-width="1"/>
    <line x1="{radar_cx}" y1="{radar_cy}" x2="{radar_cx + 44.1}" y2="{radar_cy + 60.7}" stroke="#222b3a" stroke-width="1"/>
    <line x1="{radar_cx}" y1="{radar_cy}" x2="{radar_cx - 44.1}" y2="{radar_cy + 60.7}" stroke="#222b3a" stroke-width="1"/>
    <line x1="{radar_cx}" y1="{radar_cy}" x2="{radar_cx - 71.3}" y2="{radar_cy - 23.2}" stroke="#222b3a" stroke-width="1"/>

    <!-- Radar Data Shape with Glow -->
    <polygon points="{radar_pts_str}" fill="url(#radarFill)" stroke="#bffb4f" stroke-width="2" filter="url(#subtleGlow)"/>

    <!-- Vertex Points -->
    {radar_dots_str}

    <!-- Labels -->
    <text x="{radar_cx}" y="{radar_cy - 88.0}" fill="#f0f6fc" font-size="12" class="pixel-text" text-anchor="middle">Commit</text>
    <text x="{radar_cx + 86.0}" y="{radar_cy - 25.0}" fill="#f0f6fc" font-size="12" class="pixel-text" text-anchor="start">Issue</text>
    <text x="{radar_cx + 54.0}" y="{radar_cy + 76.0}" fill="#f0f6fc" font-size="12" class="pixel-text" text-anchor="start">PullReq</text>
    <text x="{radar_cx - 54.0}" y="{radar_cy + 76.0}" fill="#f0f6fc" font-size="12" class="pixel-text" text-anchor="end">Review</text>
    <text x="{radar_cx - 86.0}" y="{radar_cy - 25.0}" fill="#f0f6fc" font-size="12" class="pixel-text" text-anchor="end">Repo</text>
    
    <!-- Scale Numbers -->
    <text x="{radar_cx + 4}" y="{radar_cy - 70.0}" fill="#586069" font-size="9" class="pixel-text">10K</text>
    <text x="{radar_cx + 4}" y="{radar_cy - 51.25}" fill="#586069" font-size="9" class="pixel-text">1K</text>
    <text x="{radar_cx + 4}" y="{radar_cy - 32.5}" fill="#586069" font-size="9" class="pixel-text">100</text>
    <text x="{radar_cx + 4}" y="{radar_cy - 13.75}" fill="#586069" font-size="9" class="pixel-text">10</text>
  </g>

  <!-- Donut Chart Widget (Bottom Left) -->
  <g id="donut-chart" transform="translate(10, 0)">
    <!-- Outer Glow Under Donut -->
    <circle cx="{donut_cx}" cy="{donut_cy}" r="46" fill="none" stroke="#bffb4f" stroke-width="1" opacity="0.15"/>
    
    <!-- Donut Arcs -->
    {donut_paths_str}

    <!-- Center Icon or Text inside Donut Hole -->
    <circle cx="{donut_cx}" cy="{donut_cy}" r="26" fill="#040608"/>
    <text x="{donut_cx}" y="{donut_cy + 4}" fill="#8b949e" font-size="11" class="pixel-text" text-anchor="middle">TECH</text>

    <!-- Legend Badges & Labels -->
    <g transform="translate(162, {donut_cy - 39})">
      {donut_legend_str}
    </g>
  </g>
</svg>
'''
    return alpino_legend(svg_content)

def main():
    target_user = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "voxelepic"
    print(f"Fetching GitHub 3D contribution metrics for: {target_user}...")
    user_data = fetch_github_data(target_user)
    
    if user_data:
        print(f"Successfully fetched live data for @{user_data.get('login', target_user)}!")
        total = user_data.get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions", 0)
        print(f"Total Live Contributions: {total}")
    else:
        sys.exit("Could not fetch real contribution data. Existing assets were not changed.")

    weeks = user_data.get("contributionsCollection", {}).get("contributionCalendar", {}).get("weeks", [])
    if not weeks or not any(week.get("contributionDays") for week in weeks):
        sys.exit("GitHub returned no contribution days. Existing assets were not changed.")

    svg = build_3d_svg(user_data)
    
    os.makedirs("profile-3d-contrib", exist_ok=True)
    targets = [
        "profile-3d-contrib/profile-night-green.svg",
    ]
    
    for t in targets:
        with open(t, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated: {t}")

    from build_contrib_animation import write_animation
    write_animation()
    print("Done! Static SVG and one-shot contribution animations generated successfully.")

if __name__ == "__main__":
    main()
