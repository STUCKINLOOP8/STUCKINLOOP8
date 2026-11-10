"""
convert_photo_to_ascii.py

Takes any image (e.g. avatar.png, photo.jpg) and converts it to a 25-line, 40-character ASCII portrait,
and updates dark_mode.svg and light_mode.svg automatically.

Usage:
    python convert_photo_to_ascii.py my_face.jpg
"""

import sys
import os
import re
from PIL import Image

CHARS_DARK = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW8%B@$"
CHARS_LIGHT = CHARS_DARK[::-1]

def escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def image_to_ascii(image_path, width=40, height=25, invert=False):
    img = Image.open(image_path).convert("L")
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    chars = CHARS_DARK if not invert else CHARS_LIGHT
    scale = (len(chars) - 1) / 255.0
    
    lines = []
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = img.getpixel((x, y))
            idx = int(pixel * scale)
            row += chars[idx]
        lines.append(f"{row:<{width}}")
    return lines

def update_svg_ascii(svg_path, ascii_lines):
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new tspans
    tspans = []
    for i, line in enumerate(ascii_lines):
        y_pos = 30 + i * 20
        tspans.append(f'<tspan x="15" y="{y_pos}">{escape_xml(line)}</tspan>')
    new_ascii_block = f'<text x="15" y="30" fill="VAR_FILL" class="ascii">\n' + '\n'.join(tspans) + '\n</text>'

    # Regex replace <text x="15" y="30" fill=".*?" class="ascii">.*?</text>
    pattern = r'<text x="15" y="30" fill="([^"]+)" class="ascii">.*?</text>'
    
    def repl(match):
        fill_color = match.group(1)
        return new_ascii_block.replace("VAR_FILL", fill_color)

    updated = re.sub(pattern, repl, content, flags=re.DOTALL)
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(updated)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_photo_to_ascii.py <path_to_image>")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.exists(img_path):
        print(f"Error: file '{img_path}' not found!")
        sys.exit(1)

    dark_ascii = image_to_ascii(img_path, width=40, height=25, invert=False)
    light_ascii = image_to_ascii(img_path, width=40, height=25, invert=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    dark_svg = os.path.join(script_dir, "dark_mode.svg")
    light_svg = os.path.join(script_dir, "light_mode.svg")

    if os.path.exists(dark_svg):
        update_svg_ascii(dark_svg, dark_ascii)
        print("Updated dark_mode.svg with new ASCII art!")
    if os.path.exists(light_svg):
        update_svg_ascii(light_svg, light_ascii)
        print("Updated light_mode.svg with new ASCII art!")

    print("\nPreview of ASCII (Dark Mode):")
    for l in dark_ascii:
        print(l)
