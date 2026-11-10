import os

ASCII_ART = [
    r"         .-----.         .-----.        ",
    r"       .'       '.     .'       '.      ",
    r"      /   .---.   \   /   .---.   \     ",
    r"     /   /     \   \ /   /     \   \    ",
    r"    |   |       |   X   |       |   |   ",
    r"    |   |       |  / \  |       |   |   ",
    r"     \   \     /  /   \  \     /   /    ",
    r"      \   '---'  /     \  '---'  /      ",
    r"       '.     .'       '.     .'        ",
    r"         '---'           '---'          ",
    r"                                        ",
    r"    .==============================.    ",
    r"    |  >> IDENTITY : STUCKINLOOP8  |    ",
    r"    |  >> PROCESS  : QUANT_RESEARCH|    ",
    r"    |  >> STATE    : INFINITE_LOOP |    ",
    r"    |  >> BREAK COND: FALSE        |    ",
    r"    |  >> WHILE (1) { CODE(); }    |    ",
    r"    '=============================='    ",
    r"                                        ",
    r"         ___ _____ _   _ ____ _  __     ",
    r"        / ___|_   _| | | | ___| |/ /    ",
    r"        \___ \ | | | | | | |   | ' /     ",
    r"         ___) || | | |_| | |___| . \    ",
    r"        |____/ |_|  \___/|____/|_|\_\   ",
    r"             [ I N   L O O P   8 ]      "
]

def escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def create_svg(is_dark=True):
    bg_color = "#161b22" if is_dark else "#f6f8fa"
    text_color = "#c9d1d9" if is_dark else "#24292f"
    key_color = "#ffa657" if is_dark else "#953800"
    val_color = "#a5d6ff" if is_dark else "#0a3069"
    cc_color = "#616e7f" if is_dark else "#c2cfde"
    add_color = "#3fb950" if is_dark else "#1a7f37"
    del_color = "#f85149" if is_dark else "#cf222e"

    width = "1020px"
    height = "530px"
    start_x = "365"

    lines = []
    lines.append("<?xml version='1.0' encoding='UTF-8'?>")
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{width}" height="{height}" font-size="16px">')
    lines.append('<style>')
    lines.append('@font-face {')
    lines.append("src: local('Consolas'), local('Consolas Bold');")
    lines.append("font-family: 'ConsolasFallback';")
    lines.append("font-display: swap;")
    lines.append("-webkit-size-adjust: 109%;")
    lines.append("size-adjust: 109%;")
    lines.append("}")
    lines.append(f".key {{fill: {key_color};}}")
    lines.append(f".value {{fill: {val_color};}}")
    lines.append(f".addColor {{fill: {add_color};}}")
    lines.append(f".delColor {{fill: {del_color};}}")
    lines.append(f".cc {{fill: {cc_color};}}")
    lines.append("text, tspan {white-space: pre;}")
    lines.append("</style>")
    lines.append(f'<rect width="{width}" height="{height}" fill="{bg_color}" rx="15"/>')
    lines.append(f'<text x="15" y="30" fill="{text_color}" class="ascii">')

    # 25 ASCII lines (y=30 to y=510, step 20)
    for i, line_text in enumerate(ASCII_ART):
        y_pos = 30 + i * 20
        padded = f"{line_text:<40}"
        lines.append(f'<tspan x="15" y="{y_pos}">{escape_xml(padded)}</tspan>')
    lines.append('</text>')

    # Right side text (starting at x="365")
    sx = start_x
    lines.append(f'<text x="{sx}" y="30" fill="{text_color}">')
    lines.append(f'<tspan x="{sx}" y="30">sambhav@stuckinloop8</tspan> -————————————————————————————————————————————-—-')
    lines.append(f'<tspan x="{sx}" y="50" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ............................ </tspan><tspan class="value">Windows 11, Linux (Ubuntu)</tspan>')
    lines.append(f'<tspan x="{sx}" y="70" class="cc">. </tspan><tspan class="key">Uptime</tspan>:<tspan class="cc" id="age_data_dots"> ..................... </tspan><tspan class="value" id="age_data">21 years, 4 months, 26 days</tspan>')
    lines.append(f'<tspan x="{sx}" y="90" class="cc">. </tspan><tspan class="key">Host</tspan>:<tspan class="cc"> ................................. </tspan><tspan class="value">Quantitative Research &amp; CS</tspan>')
    lines.append(f'<tspan x="{sx}" y="110" class="cc">. </tspan><tspan class="key">Kernel</tspan>:<tspan class="cc"> .......... </tspan><tspan class="value">Algorithmic Trading, DSA, ML</tspan>')
    lines.append(f'<tspan x="{sx}" y="130" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ............................ </tspan><tspan class="value">VS Code, Cursor, Neovim</tspan>')
    lines.append(f'<tspan x="{sx}" y="150" class="cc">. </tspan>')
    lines.append(f'<tspan x="{sx}" y="170" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">Python, C++, JavaScript, SQL</tspan>')
    lines.append(f'<tspan x="{sx}" y="190" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Computer</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">HTML, CSS, JSON, Git, Bash</tspan>')
    lines.append(f'<tspan x="{sx}" y="210" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Real</tspan>:<tspan class="cc"> ............................. </tspan><tspan class="value">English, Hindi</tspan>')
    lines.append(f'<tspan x="{sx}" y="230" class="cc">. </tspan>')
    lines.append(f'<tspan x="{sx}" y="250" class="cc">. </tspan><tspan class="key">Hobbies</tspan>.<tspan class="key">Software</tspan>:<tspan class="cc"> ........ </tspan><tspan class="value">Quant Backtesting, Algorithms, Systems</tspan>')
    lines.append(f'<tspan x="{sx}" y="270" class="cc">. </tspan><tspan class="key">Hobbies</tspan>.<tspan class="key">Hardware</tspan>:<tspan class="cc"> ................. </tspan><tspan class="value">Custom PC Building, Benchmarks</tspan>')
    lines.append(f'<tspan x="{sx}" y="310">- Contact</tspan> -——————————————————————————————————————————————————-—-')
    lines.append(f'<tspan x="{sx}" y="330" class="cc">. </tspan><tspan class="key">Email</tspan>.<tspan class="key">Personal</tspan>:<tspan class="cc"> ......................... </tspan><tspan class="value">sambhavvvvv10@gmail.com</tspan>')
    lines.append(f'<tspan x="{sx}" y="350" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ........................................ </tspan><tspan class="value">sambhav</tspan>')
    lines.append(f'<tspan x="{sx}" y="370" class="cc">. </tspan><tspan class="key">GitHub</tspan>:<tspan class="cc"> .......................................... </tspan><tspan class="value">STUCKINLOOP8</tspan>')
    lines.append(f'<tspan x="{sx}" y="390" class="cc">. </tspan><tspan class="key">Discord</tspan>:<tspan class="cc"> ......................................... </tspan><tspan class="value">stuckinloop8</tspan>')
    lines.append(f'<tspan x="{sx}" y="410" class="cc">. </tspan><tspan class="key">Status</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">while (true) {{ code(); }}</tspan>')
    lines.append(f'<tspan x="{sx}" y="450">- GitHub Stats</tspan> -————————————————————————————————————————————-—-')
    lines.append(f'<tspan x="{sx}" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> ...... </tspan><tspan class="value" id="repo_data">3</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">3</tspan>}} | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ............ </tspan><tspan class="value" id="star_data">1</tspan>')
    lines.append(f'<tspan x="{sx}" y="490" class="cc">. </tspan><tspan class="key">Commmits</tspan>:<tspan class="cc" id="commit_data_dots"> ..................... </tspan><tspan class="value" id="commit_data">54</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ........ </tspan><tspan class="value" id="follower_data">3</tspan>')
    lines.append(f'<tspan x="{sx}" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots"> .. </tspan><tspan class="value" id="loc_data">6,508</tspan> ( <tspan class="addColor" id="loc_add">6,508</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan><tspan class="delColor">--</tspan> )')
    lines.append('</text>')
    lines.append('</svg>')

    return '\n'.join(lines)

target_dir = r"C:\Users\Sambhav\.gemini\antigravity\scratch\STUCKINLOOP8"
with open(os.path.join(target_dir, "dark_mode.svg"), "w", encoding="utf-8") as f:
    f.write(create_svg(is_dark=True))

with open(os.path.join(target_dir, "light_mode.svg"), "w", encoding="utf-8") as f:
    f.write(create_svg(is_dark=False))

print("dark_mode.svg and light_mode.svg generated successfully!")
