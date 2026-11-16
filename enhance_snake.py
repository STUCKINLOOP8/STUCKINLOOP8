import os

def set_blue_neon(file_path, color='#00d4ff', glow='filter:drop-shadow(0 0 6px #00d4ff) drop-shadow(0 0 12px #0077ff);'):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        svg = f.read()

    # Set snake color
    svg = svg.replace('--cs:purple', f'--cs:{color}')
    # Add blue neon glow
    old_s = '.s{shape-rendering:geometricPrecision;fill:var(--cs);animation:none linear 15700ms infinite}'
    new_s = f'.s{{shape-rendering:geometricPrecision;fill:var(--cs);{glow}animation:none linear 15700ms infinite}}'
    if old_s in svg:
        svg = svg.replace(old_s, new_s)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Updated {file_path} to Blue Neon")

if __name__ == '__main__':
    set_blue_neon('assets/github-contribution-grid-snake-dark.svg', '#00d4ff', 'filter:drop-shadow(0 0 6px #00d4ff) drop-shadow(0 0 12px #0077ff);')
    set_blue_neon('assets/github-contribution-grid-snake.svg', '#0088ff', 'filter:drop-shadow(0 0 4px #0088ff);')
