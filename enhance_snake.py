import re
import os

def enhance_svg(file_path, is_dark=True):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        svg_text = f.read()

    # 1. Parse eat timestamps from cell keyframes
    eat_times = []
    for m in re.finditer(r'@keyframes (c[0-9a-z]+)\{([0-9.]+)%\{fill:var\(--c[0-9]\)\}', svg_text):
        c_name = m.group(1)
        t = float(m.group(2))
        eat_times.append((t, c_name))
    eat_times.sort()
    print(f"[{file_path}] Detected {len(eat_times)} eat events: {[round(t, 2) for t, _ in eat_times]}")

    # 2. Parse s0 keyframe steps
    token = '@keyframes s0{'
    idx = svg_text.find(token)
    if idx == -1:
        token = '@keyframes s0 {'
        idx = svg_text.find(token)
    start = idx + len(token)
    depth = 1
    i = start
    while i < len(svg_text) and depth > 0:
        if svg_text[i] == '{': depth += 1
        elif svg_text[i] == '}': depth -= 1
        i += 1
    s0_body = svg_text[start:i-1]

    pattern = r'([0-9.,%]+)\s*\{transform:translate\(([^)]+)\)\}'
    s0_steps = []
    for m in re.finditer(pattern, s0_body):
        pcts = m.group(1).split(',')
        coord = m.group(2)
        for p in pcts:
            s0_steps.append((float(p.replace('%', '')), coord))
    s0_steps.sort(key=lambda x: x[0])

    dt = 100.0 / 157.0 # 0.636942675... (1 grid step delay)

    def generate_sk_keyframes(k):
        steps = []
        steps.append((0.0, f"{k*16}px,-16px"))
        if k > 0:
            steps.append((round(k * dt, 2), "0px,-16px"))
            steps.append((round((k + 1) * dt, 2), "0px,0px"))
        
        for p, c in s0_steps:
            if p <= 0.64: continue
            if p >= 96.82: continue
            p_k = round(p + k * dt, 2)
            steps.append((p_k, c))
        
        steps.append((round(96.18 + k * dt, 2), "64px,0px"))
        steps.append((round(96.82 + k * dt, 2), "64px,-16px"))
        steps.append((99.36, f"{k*16}px,-16px"))
        
        steps.sort(key=lambda x: x[0])
        kf_str = f"@keyframes s{k}{{"
        for p, c in steps:
            kf_str += f"{p:.2f}%{{transform:translate({c})}}"
        kf_str += "}"
        return kf_str

    # Palette
    # Electric Neon Blue
    snake_color = "#00d4ff" if is_dark else "#0969da"
    glow_color = "#0077ff" if is_dark else "rgba(9,105,218,0.5)"
    flash_color = "#e0f7ff" if is_dark else "#2ea043"

    extra_sk_keyframes = []
    extra_sk_classes = []
    extra_rects = []

    # Generate segments s4 through s14 (+1 segment per eaten box)
    for idx, (eat_t, _) in enumerate(eat_times):
        k = idx + 4
        extra_sk_keyframes.append(generate_sk_keyframes(k))
        extra_sk_classes.append(f".s.s{k}{{transform:translate({k*16}px,-16px);animation-name:s{k}}}")
        
        t_spawn = eat_t
        t_pop = min(99.0, eat_t + 0.35)
        t_norm = min(99.2, eat_t + 1.1)
        t_exit = min(99.36, 96.82 + k * dt)
        
        if is_dark:
            app_kf = f"""@keyframes s{k}-appear {{
  0%, {max(0.0, t_spawn - 0.05):.2f}% {{ opacity: 0; transform: scale(0); }}
  {t_spawn:.2f}% {{ opacity: 1; transform: scale(0.2); filter: drop-shadow(0 0 10px #00d4ff); }}
  {t_pop:.2f}% {{ opacity: 1; transform: scale(1.4); filter: drop-shadow(0 0 16px #00d4ff) drop-shadow(0 0 24px #0077ff); fill: {flash_color}; }}
  {t_norm:.2f}% {{ opacity: 1; transform: scale(1); filter: drop-shadow(0 0 5px #00d4ff); fill: var(--cs); }}
  {t_exit:.2f}% {{ opacity: 1; transform: scale(1); }}
  {min(99.36, t_exit + 0.5):.2f}%, 100% {{ opacity: 0; transform: scale(0); }}
}}"""
        else:
            app_kf = f"""@keyframes s{k}-appear {{
  0%, {max(0.0, t_spawn - 0.05):.2f}% {{ opacity: 0; transform: scale(0); }}
  {t_spawn:.2f}% {{ opacity: 1; transform: scale(0.2); filter: drop-shadow(0 0 8px rgba(9,105,218,0.6)); }}
  {t_pop:.2f}% {{ opacity: 1; transform: scale(1.35); fill: {flash_color}; }}
  {t_norm:.2f}% {{ opacity: 1; transform: scale(1); fill: var(--cs); }}
  {t_exit:.2f}% {{ opacity: 1; transform: scale(1); }}
  {min(99.36, t_exit + 0.5):.2f}%, 100% {{ opacity: 0; transform: scale(0); }}
}}"""

        extra_sk_keyframes.append(app_kf)
        extra_rects.append(
            f'<g class="s s{k}"><rect class="snake-seg" style="animation: s{k}-appear 15700ms ease infinite;" x="3.0" y="3.0" width="9.9" height="9.9" rx="3.3" ry="3.3"/></g>'
        )

    # 3. Head eat pulse (scales up by 165% on each chomp)
    head_points = [(0.0, 1.0, 1.0, False), (0.2, 1.0, 1.0, False)]
    body_points = [(0.0, 1.0, 1.0, False), (0.2, 1.0, 1.0, False)]
    for t, _ in eat_times:
        head_points.append((max(0.0, t - 0.05), 1.0, 1.0, False))
        head_points.append((min(99.0, t + 0.35), 1.65, 2.8, True))
        head_points.append((min(99.5, t + 1.15), 1.0, 1.0, False))

        body_points.append((max(0.0, t - 0.05), 1.0, 1.0, False))
        body_points.append((min(99.0, t + 0.55), 1.35, 2.0, True))
        body_points.append((min(99.5, t + 1.35), 1.0, 1.0, False))

    head_points.append((100.0, 1.0, 1.0, False))
    body_points.append((100.0, 1.0, 1.0, False))
    head_points.sort(key=lambda x: x[0])
    body_points.sort(key=lambda x: x[0])

    def clean(pts):
        res = []
        for p in pts:
            if not res or abs(p[0] - res[-1][0]) > 0.08: res.append(p)
        return res

    head_pts = clean(head_points)
    body_pts = clean(body_points)

    kf_head = ["@keyframes snake-head-eat {\n"]
    for t, scale, glow, flash in head_pts:
        color_prop = f"fill: {flash_color};" if flash else "fill: var(--cs);"
        if is_dark:
            glow_px = 6 * glow
            glow_wide = 15 * glow
            kf_head.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px #00d4ff) drop-shadow(0 0 {glow_wide:.1f}px #0077ff); {color_prop} }}\n"
            )
        else:
            glow_px = 4 * glow
            kf_head.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px rgba(9,105,218,0.6)); {color_prop} }}\n"
            )
    kf_head.append("}\n")

    kf_body = ["@keyframes snake-body-eat {\n"]
    for t, scale, glow, flash in body_pts:
        if is_dark:
            glow_px = 4 * glow
            kf_body.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px #00d4ff); }}\n"
            )
        else:
            glow_px = 3 * glow
            kf_body.append(
                f"  {t:.2f}% {{ transform: scale({scale:.2f}); filter: drop-shadow(0 0 {glow_px:.1f}px rgba(9,105,218,0.4)); }}\n"
            )
    kf_body.append("}\n")

    filter_style = "filter: drop-shadow(0 0 5px #00d4ff) drop-shadow(0 0 10px rgba(0, 119, 255, 0.6));" if is_dark else "filter: drop-shadow(0 0 3px rgba(9, 105, 218, 0.4));"

    all_extra_css = f"""
:root {{
  --cs: {snake_color};
}}
.s {{
  shape-rendering: geometricPrecision;
  animation: none linear 15700ms infinite;
}}
{chr(10).join(extra_sk_classes)}
.snake-seg {{
  shape-rendering: geometricPrecision;
  fill: var(--cs);
  transform-box: fill-box;
  transform-origin: center;
  {filter_style}
}}
.snake-head {{
  animation: snake-head-eat 15700ms ease infinite;
}}
.snake-body {{
  animation: snake-body-eat 15700ms ease infinite;
}}
{"".join(kf_head)}
{"".join(kf_body)}
{"".join(extra_sk_keyframes)}
"""

    # Clean existing injected CSS if re-running
    svg_clean = re.sub(r':root\s*\{[^}]*--cs:[^}]*\}', '', svg_text)
    svg_clean = re.sub(r'\.s\{[^}]+\}', '', svg_clean)
    svg_clean = re.sub(r'\.s\.s[0-9]+\{[^}]+\}', '', svg_clean)
    svg_clean = re.sub(r'\.snake-seg\{[^}]+\}', '', svg_clean)
    svg_clean = re.sub(r'\.snake-head\{[^}]+\}', '', svg_clean)
    svg_clean = re.sub(r'\.snake-body\{[^}]+\}', '', svg_clean)
    svg_clean = re.sub(r'@keyframes snake-[a-z-]+eat\s*\{[^}]+\}', '', svg_clean)
    svg_clean = re.sub(r'@keyframes s[0-9]+-appear\s*\{[^}]+\}', '', svg_clean)
    for k in range(4, 30):
        svg_clean = re.sub(rf'@keyframes s{k}\{{[^}}]+\}}', '', svg_clean)
        svg_clean = re.sub(rf'<g class="s s{k}">.*?</g>', '', svg_clean)

    std_classes = """
.s.s0{transform:translate(0px,-16px);animation-name:s0}
.s.s1{transform:translate(16px,-16px);animation-name:s1}
.s.s2{transform:translate(32px,-16px);animation-name:s2}
.s.s3{transform:translate(48px,-16px);animation-name:s3}
"""
    svg_clean = svg_clean.replace('</style>', std_classes + all_extra_css + '</style>')

    # Convert initial rects s0..s3 to groups
    def repl_init(m):
        full = m.group(1)
        s_class = m.group(2)
        attrs = m.group(3)
        seg_type = "snake-head" if s_class == "s0" else "snake-body"
        return f'<g class="s {s_class}"><rect class="snake-seg {seg_type}" {attrs}/></g>'

    pattern_rect = r'(<rect class="s (s[0-3])" (x="[^"]+" y="[^"]+" width="[^"]+" height="[^"]+" rx="[^"]+" ry="[^"]+")/>)'
    svg_clean = re.sub(pattern_rect, repl_init, svg_clean)

    # Append extra rects before </svg>
    svg_clean = svg_clean.replace('</svg>', "".join(extra_rects) + '</svg>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(svg_clean)

    print(f"[{file_path}] Successfully enhanced with Blue Neon and +1 box growth per eat!")

if __name__ == '__main__':
    enhance_svg('assets/github-contribution-grid-snake-dark.svg', is_dark=True)
    enhance_svg('assets/github-contribution-grid-snake.svg', is_dark=False)
