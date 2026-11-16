import re
import os

def enhance_svg(file_path, is_dark=True):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        svg = f.read()

    # 1. Extract eat timestamps from cell keyframes
    eat_times = []
    for m in re.finditer(r'@keyframes (c[0-9a-z]+)\{([0-9.]+)%\{fill:var\(--c[0-9]\)\}', svg):
        c_name = m.group(1)
        t = float(m.group(2))
        eat_times.append((t, c_name))

    eat_times.sort()
    print(f"[{file_path}] Detected {len(eat_times)} eat events")

    # 2. Build pulse keyframes
    all_points_head = [(0.0, 1.0, 1.0, False), (0.2, 1.0, 1.0, False)]
    all_points_body = [(0.0, 1.0, 1.0, False), (0.2, 1.0, 1.0, False)]

    for t, _ in eat_times:
        t_start = max(0.0, t - 0.05)
        t_peak = min(99.0, t + 0.35)
        t_settle = min(99.5, t + 1.15)
        
        all_points_head.append((t_start, 1.0, 1.0, False))
        all_points_head.append((t_peak, 1.65, 2.8, True)) # 165% size + huge bloom!
        all_points_head.append((t_settle, 1.0, 1.0, False))
        
        t_b_peak = min(99.0, t + 0.55)
        t_b_settle = min(99.5, t + 1.35)
        all_points_body.append((t_start, 1.0, 1.0, False))
        all_points_body.append((t_b_peak, 1.45, 2.0, True)) # 145% size
        all_points_body.append((t_b_settle, 1.0, 1.0, False))

    all_points_head.append((100.0, 1.0, 1.0, False))
    all_points_body.append((100.0, 1.0, 1.0, False))

    all_points_head.sort(key=lambda x: x[0])
    all_points_body.sort(key=lambda x: x[0])

    def clean_points(pts):
        res = []
        for p in pts:
            if not res or abs(p[0] - res[-1][0]) > 0.08:
                res.append(p)
        return res

    head_pts = clean_points(all_points_head)
    body_pts = clean_points(all_points_body)

    keyframes_head = ["@keyframes snake-head-eat {\n"]
    keyframes_body = ["@keyframes snake-body-eat {\n"]

    snake_color = "#00ff88" if is_dark else "#0969da"
    flash_color = "#00ffff" if is_dark else "#2ea043"

    for t, scale, glow, flash in head_pts:
        if is_dark:
            glow_px = 6 * glow
            glow_wide = 14 * glow
            color_prop = f"fill: {flash_color};" if flash else "fill: var(--cs);"
            keyframes_head.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px #00ff88) drop-shadow(0 0 {glow_wide:.1f}px #00f0ff); {color_prop} }}\n"
            )
        else:
            glow_px = 4 * glow
            color_prop = f"fill: {flash_color};" if flash else "fill: var(--cs);"
            keyframes_head.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px rgba(9,105,218,0.5)); {color_prop} }}\n"
            )
    keyframes_head.append("}\n")

    for t, scale, glow, flash in body_pts:
        if is_dark:
            glow_px = 4 * glow
            keyframes_body.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px #00ff88); }}\n"
            )
        else:
            glow_px = 3 * glow
            keyframes_body.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px rgba(9,105,218,0.4)); }}\n"
            )
    keyframes_body.append("}\n")

    kf_head_str = "".join(keyframes_head)
    kf_body_str = "".join(keyframes_body)

    # 3. Enhance styles
    extra_css = f"""
:root {{
  --cs: {snake_color};
}}
.s {{
  shape-rendering: geometricPrecision;
  animation: none linear 15700ms infinite;
}}
.snake-seg {{
  shape-rendering: geometricPrecision;
  fill: var(--cs);
  transform-box: fill-box;
  transform-origin: center;
  transition: transform 0.1s ease;
}}
.snake-head {{
  animation: snake-head-eat 15700ms ease infinite;
}}
.snake-body {{
  animation: snake-body-eat 15700ms ease infinite;
}}
{kf_head_str}
{kf_body_str}
"""

    # Remove old .s rule from style
    svg_enhanced = re.sub(r'\.s\{[^}]+\}', '', svg)
    # Update --cs default
    svg_enhanced = re.sub(r'--cs:[^;]+;', f'--cs:{snake_color};', svg_enhanced)
    # Insert extra CSS before closing </style>
    svg_enhanced = svg_enhanced.replace('</style>', extra_css + '</style>')

    # Replace the 4 snake rects with <g class="s s0"><rect class="snake-seg snake-head" .../></g>
    pattern = r'(<rect class="s (s[0-3])" (x="[^"]+" y="[^"]+" width="[^"]+" height="[^"]+" rx="[^"]+" ry="[^"]+")/>)'

    def repl(match):
        s_class = match.group(2)
        attrs = match.group(3)
        seg_type = "snake-head" if s_class == "s0" else "snake-body"
        return f'<g class="s {s_class}"><rect class="snake-seg {seg_type}" {attrs}/></g>'

    svg_enhanced = re.sub(pattern, repl, svg_enhanced)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(svg_enhanced)

    print(f"[{file_path}] Successfully enhanced with glowing and eating effects!")

if __name__ == '__main__':
    enhance_svg('assets/github-contribution-grid-snake-dark.svg', is_dark=True)
    enhance_svg('assets/github-contribution-grid-snake.svg', is_dark=False)
