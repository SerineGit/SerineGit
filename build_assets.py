import sys, math, html, os

STATIC = "--static" in sys.argv
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "/home/claude/readme-v3/assets"
os.makedirs(OUT, exist_ok=True)

BG, PANEL, LINE = "#0b1020", "#0f1629", "#1f2a44"
CYAN, VIOLET, GREEN, PINK, AMBER = "#22d3ee", "#a78bfa", "#34d399", "#f472b6", "#fbbf24"
TEXT, MUTED = "#e5e9f5", "#7a86a8"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "Inter,'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"


def esc(s):
    return html.escape(s, quote=False)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def svg_open(w, h, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
        f"<defs>"
        f'<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
        f'<linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#101a38"/></linearGradient>'
        f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#16203a" stroke-width="1"/></pattern>'
        f'<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f"{extra_defs}</defs>"
    )


def stepped(attr, values, start, dt, T, id_=None):
    """discrete stepped animation: values[0] before start, then one value per dt"""
    n = len(values) - 1
    kt = [0.0] + [(start + j * dt) / T for j in range(n)]
    vs = values
    return (
        f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(str(v) for v in vs)}"/>'
    )


def window(a, b, T):
    """opacity animation: visible between a and b seconds of the cycle"""
    pts = [(0.0, 0)]
    if a <= 0:
        pts = [(0.0, 1)]
    else:
        pts.append((a / T, 1))
    if b < T:
        pts.append((b / T, 0))
    return (
        f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{";".join(f"{k:.4f}" for k, _ in pts)}" values="{";".join(str(v) for _, v in pts)}"/>'
    )


def blink(dur=1):
    return f'<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" dur="{dur}s" calcMode="discrete" repeatCount="indefinite"/>'


# ----------------------------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------------------------
def header():
    W, H, T = 1200, 380, 15.0
    cx, cy, R = 1000, 190, 125
    p = [svg_open(W, H, '<clipPath id="r"><rect width="1200" height="380" rx="20"/></clipPath>'
                  f'<radialGradient id="sweep" cx="0" cy="0" r="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/></radialGradient>'
                  f'<radialGradient id="aura" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".35"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>')]
    p.append('<title>Serine Zargaryan - QA Engineer / C++ Developer</title>')
    p.append('<g clip-path="url(#r)">')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#bgg)"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity=".7"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="260" fill="url(#aura)"/>')
    p.append(f'<circle cx="120" cy="40" r="180" fill="{CYAN}" opacity=".05"/>')
    # radar
    for r in (R, R * 2 / 3, R / 3):
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-width="1"/>')
    p.append(f'<line x1="{cx-R}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{CYAN}" stroke-opacity=".2"/>')
    p.append(f'<line x1="{cx}" y1="{cy-R}" x2="{cx}" y2="{cy+R}" stroke="{CYAN}" stroke-opacity=".2"/>')
    a = math.radians(55)
    x2, y2 = cx + R * math.cos(-a), cy + R * math.sin(-a)
    sweep = (f'<g><path d="M{cx} {cy} L{cx+R} {cy} A{R} {R} 0 0 0 {x2:.1f} {y2:.1f} Z" fill="{CYAN}" opacity=".22"/>'
             f'<line x1="{cx}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{CYAN}" stroke-width="2" filter="url(#glow)"/>')
    if not STATIC:
        sweep += f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="5s" repeatCount="indefinite"/>'
    sweep += "</g>"
    p.append(sweep)
    blips = [(cx + 55, cy - 40, 0.4), (cx - 70, cy - 20, 1.8), (cx - 25, cy + 75, 3.0), (cx + 85, cy + 50, 4.2)]
    for bx, by, delay in blips:
        pulse = "" if STATIC else (f'<animate attributeName="r" values="3;9;3" dur="5s" begin="{delay}s" repeatCount="indefinite"/>'
                                   f'<animate attributeName="opacity" values="1;.2;1" dur="5s" begin="{delay}s" repeatCount="indefinite"/>')
        p.append(f'<circle cx="{bx}" cy="{by}" r="4" fill="{PINK}" filter="url(#glow)">{pulse}</circle>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{CYAN}"/>')
    p.append(f'<text x="{cx}" y="{cy+R+28}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">BUG RADAR</text>')

    # text
    p.append(f'<text x="64" y="66" font-family="{MONO}" font-size="15" fill="{MUTED}">// Hello, World.</text>')
    p.append(f'<text x="62" y="146" font-family="{SANS}" font-size="64" font-weight="800" fill="url(#brand)" filter="url(#glow)">Serine Zargaryan</text>')
    p.append(f'<text x="64" y="190" font-family="{MONO}" font-size="16" letter-spacing="4" fill="{CYAN}">QA ENGINEER  /  C++ DEVELOPER</text>')

    phrases = ["> Code. Break. Fix. Repeat.", "> I find bugs before users do.", "> Coding my way out of the matrix..."]
    slice_ = T / len(phrases)
    cw, fs, x0, y0 = 14.4, 24, 64, 252
    for i, ph in enumerate(phrases):
        s = i * slice_ + 0.4
        n = len(ph)
        dt = 0.07
        vals = [0] + [round((j + 1) * cw, 1) for j in range(n)]
        full = round((n + 1) * cw, 1)
        cid = f"hp{i}"
        if STATIC and i != 0:
            continue
        anim_w = "" if STATIC else stepped("width", vals, s, dt, T)
        w0 = full
        p.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{y0-fs}" width="{w0}" height="{fs+10}">{anim_w}</rect></clipPath>')
        grp = f'<g opacity="{1 if (STATIC or i==0) else 0}">' if True else ""
        p.append(grp + ("" if STATIC else window(i * slice_, (i + 1) * slice_, T)))
        p.append(f'<text x="{x0}" y="{y0}" font-family="{MONO}" font-size="{fs}" fill="{TEXT}" clip-path="url(#{cid})">{esc(ph)}</text>')
        cur_vals = [x0] + [round(x0 + (j + 1) * cw, 1) for j in range(n)]
        cur_anim = "" if STATIC else stepped("x", cur_vals, s, dt, T)
        cur_x = x0 + n * cw
        p.append(f'<rect x="{cur_x}" y="{y0-fs+3}" width="11" height="{fs}" fill="{GREEN}">{cur_anim}</rect>')
        p.append("</g>")

    p.append(f'<text x="64" y="300" font-family="{MONO}" font-size="15" fill="{GREEN}" opacity=".85">while (true) {{ code(); breakIt(); fix(); }}</text>')
    # pills
    px = 64
    for label in ["Manual + Automated", "Los Angeles, CA", "English / 日本語 / Հայերեն"]:
        w = len(label) * 7.9 + 36
        p.append(f'<rect x="{px}" y="320" width="{w:.0f}" height="30" rx="15" fill="{PANEL}" stroke="{LINE}"/>')
        p.append(f'<circle cx="{px+16}" cy="335" r="3" fill="{CYAN}"/>')
        p.append(f'<text x="{px+28}" y="340" font-family="{MONO}" font-size="12.5" fill="{TEXT}">{esc(label)}</text>')
        px += w + 12
    p.append("</g>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{LINE}"/>')
    p.append("</svg>")
    write("header.svg", "".join(p))


# ----------------------------------------------------------------------------------------------
# TERMINAL
# ----------------------------------------------------------------------------------------------
def terminal():
    W, H, T = 1100, 430, 20.0
    fs, cw, lh, x0 = 15, 9.0, 26, 34
    P = "serine@qa-lab"
    lines = [
        ([(P, GREEN), (":~$ ", MUTED), ("whoami", TEXT)], 0.07),
        ([("serine zargaryan  //  QA engineer by day, C++ developer by heart", CYAN)], 0.012),
        ([], 0),
        ([(P, GREEN), (":~$ ", MUTED), ("./run_tests --suite=life", TEXT)], 0.07),
        ([("  [ PASS ] ", GREEN), ("tennis.serve()", TEXT)], 0.02),
        ([("  [ PASS ] ", GREEN), ("chess.think_three_moves_ahead()", TEXT)], 0.02),
        ([("  [ PASS ] ", GREEN), ("pets.cuddle()", TEXT)], 0.02),
        ([("  [ PASS ] ", GREEN), ("languages == {en, ja, hy}", TEXT)], 0.02),
        ([("  [ PASS ] ", GREEN), ("bugs.find()  ", TEXT), ("// always", MUTED)], 0.02),
        ([("  [ WARN ] ", AMBER), ("coffee.level == 0", TEXT)], 0.02),
        ([], 0),
        ([("  5 passed, ", TEXT), ("1 warning", AMBER), (", 0 failed", TEXT)], 0.02),
        ([], 0),
        ([(P, GREEN), (":~$ ", MUTED)], 0.07),
    ]
    p = [svg_open(W, H, '<clipPath id="tw"><rect width="1100" height="430" rx="14"/></clipPath>')]
    p.append('<title>Terminal: whoami and run_tests --suite=life</title>')
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="#080c18" stroke="{LINE}"/>')
    p.append(f'<g clip-path="url(#tw)"><rect width="{W}" height="42" fill="#0d1426"/><line x1="0" y1="42" x2="{W}" y2="42" stroke="{LINE}"/></g>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        p.append(f'<circle cx="{26+i*22}" cy="21" r="6.5" fill="{c}"/>')
    p.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">serine@qa-lab: ~/life</text>')
    t = 0.6
    y = 82
    last_end = 0
    cursor_info = None
    for idx, (segs, dt) in enumerate(lines):
        if not segs:
            t += 0.25
            y += lh
            continue
        total = sum(len(s) for s, _ in segs)
        start = t
        vals = [0] + [round((j + 1) * cw, 1) for j in range(total)]
        full = round((total + 1) * cw, 1)
        cid = f"tl{idx}"
        anim = "" if STATIC else stepped("width", vals, start, dt, T)
        p.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{y-fs-2}" width="{full}" height="{fs+9}">{anim}</rect></clipPath>')
        tsp = "".join(f'<tspan fill="{c}">{esc(s).replace(" ", chr(160))}</tspan>' for s, c in segs)
        p.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" clip-path="url(#{cid})" xml:space="preserve">{tsp}</text>')
        t = start + total * dt + (0.7 if dt >= 0.07 else 0.25)
        cursor_info = (x0 + total * cw, y, start + total * dt)
        y += lh
    if cursor_info:
        cx_, cy_, appear = cursor_info
        if STATIC:
            p.append(f'<rect x="{cx_}" y="{cy_-fs}" width="9" height="{fs+3}" fill="{GREEN}"/>')
        else:
            kt = f"0;{appear/T:.4f};{(appear+0.5)/T:.4f}"
            p.append(f'<rect x="{cx_}" y="{cy_-fs}" width="9" height="{fs+3}" fill="{GREEN}" opacity="0">'
                     f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{appear/T:.4f}" values="0;1"/></rect>')
    p.append("</svg>")
    write("terminal.svg", "".join(p))


# ----------------------------------------------------------------------------------------------
# CHIP SECTIONS (stack, about)
# ----------------------------------------------------------------------------------------------
def chip_width(label, fs=14):
    wide = sum(1.0 if ord(ch) < 0x2E80 else 1.9 for ch in label)
    return wide * fs * 0.58 + 44


def chips_svg(name, title, groups, W=1100, fs=14):
    pad, row_h, gap = 28, 40, 10
    p_body = []
    y = 26
    delay = 0.0
    for gi, (gname, color, items) in enumerate(groups):
        p_body.append(f'<text x="{pad}" y="{y+14}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{color}">{esc(gname)}</text>')
        p_body.append(f'<line x1="{pad+len(gname)*10+14}" y1="{y+10}" x2="{W-pad}" y2="{y+10}" stroke="{LINE}"/>')
        y += 30
        x = pad
        for it in items:
            w = chip_width(it, fs)
            if x + w > W - pad:
                x = pad
                y += row_h
            anim = ""
            op = 1
            p_body.append(
                f'<g opacity="{op}">{anim}<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="32" rx="9" fill="{PANEL}" stroke="{LINE}"/>'
                f'<circle cx="{x+18:.0f}" cy="{y+16}" r="4" fill="{color}"/>'
                f'<text x="{x+30:.0f}" y="{y+21}" font-family="{SANS}" font-size="{fs}" fill="{TEXT}">{esc(it)}</text></g>')
            x += w + gap
            delay += 0.04
        y += row_h + 14
    H = y + 6
    bgr = f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{BG}" stroke="{LINE}"/>'
    out = [svg_open(W, H), f"<title>{esc(title)}</title>", bgr] + p_body + ["</svg>"]
    write(name, "".join(out))


def stack():
    chips_svg("stack.svg", "Tech stack", [
        ("LANGUAGES", CYAN, ["C++", "Python", "JavaScript", "HTML5", "CSS3", "SQL / MySQL"]),
        ("QA AND AUTOMATION", PINK, ["Manual testing", "Test automation", "Selenium", "Playwright", "Postman", "API testing", "Performance", "Security testing", "Jira", "Confluence"]),
        ("TOOLS", VIOLET, ["Git", "GitHub", "VS Code", "PyCharm", "WebStorm", "Node.js", "Snyk", "Lighthouse", "VirtualBox", "Slack", "Zoom"]),
        ("PLATFORMS", GREEN, ["Chrome", "Firefox", "Edge", "Safari", "Opera", "Android", "iOS", "Windows", "macOS"]),
    ])


def about():
    chips_svg("about.svg", "About Serine", [
        ("LOVES", PINK, ["My pets", "PlayStation", "Marvel"]),
        ("HOBBIES", AMBER, ["Tennis", "Chess", "Drawing", "Reading comics"]),
        ("SPEAKS", CYAN, ["English", "日本語", "Հայերեն"]),
    ])


# ----------------------------------------------------------------------------------------------
# PROJECT CARDS
# ----------------------------------------------------------------------------------------------
def card(name, repo, desc_lines, lang, color, tag):
    W, H = 540, 176
    p = [svg_open(W, H, f'<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
                   '<clipPath id="cc"><rect width="540" height="176" rx="14"/></clipPath>')]
    p.append(f"<title>{esc(repo)}</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
    p.append('<g clip-path="url(#cc)">')
    p.append(f'<rect width="{W}" height="3" fill="url(#bar)"/>')
    if not STATIC:
        p.append(f'<rect width="120" height="3" fill="#ffffff" opacity=".55"><animate attributeName="x" from="-120" to="{W}" dur="3.5s" repeatCount="indefinite"/></rect>')
    p.append("</g>")
    # repo icon
    p.append(f'<g transform="translate(26 30)" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h9l3 3h8v16H2z"/></g>')
    p.append(f'<text x="64" y="48" font-family="{MONO}" font-size="19" font-weight="700" fill="{TEXT}">{esc(repo)}</text>')
    tw = len(tag) * 7.2 + 20
    p.append(f'<rect x="{W-26-tw:.0f}" y="30" width="{tw:.0f}" height="22" rx="11" fill="none" stroke="{color}" stroke-opacity=".6"/>')
    p.append(f'<text x="{W-26-tw/2:.0f}" y="45" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{color}">{esc(tag)}</text>')
    for i, l in enumerate(desc_lines):
        p.append(f'<text x="28" y="{86+i*24}" font-family="{SANS}" font-size="15" fill="{MUTED}">{esc(l)}</text>')
    p.append(f'<circle cx="34" cy="{H-26}" r="5" fill="{color}"/>')
    p.append(f'<text x="48" y="{H-21}" font-family="{MONO}" font-size="12.5" fill="{TEXT}">{esc(lang)}</text>')
    p.append(f'<text x="{W-26}" y="{H-21}" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{CYAN}">open repo  →</text>')
    p.append("</svg>")
    write(name, "".join(p))


def cards():
    card("card-snake.svg", "cpp-snake-game", ["Classic 2D Snake game built with", "C++ and Windows Forms."], "C++", CYAN, "game")
    card("card-apple.svg", "Apple-and-X-AI-testing", ["Front-end, API, performance and security", "testing, cloud automation, QA docs."], "HTML  /  QA", PINK, "qa project")
    card("card-blue.svg", "Blue-Origin-and-X-AI-testing", ["The full QA cycle again, now with", "Playwright and cloud automation."], "HTML  /  Playwright", VIOLET, "qa project")
    card("card-menu.svg", "Demo-Menu", ["A demo menu page: layout and", "interaction in plain JavaScript."], "JavaScript", AMBER, "web")


# ----------------------------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------------------------
def footer():
    W, H = 1200, 150
    p = [svg_open(W, H, f'<linearGradient id="flow" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></linearGradient>')]
    p.append("<title>Footer</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{BG}" stroke="{LINE}"/>')
    p.append(f'<line x1="40" y1="40" x2="{W-40}" y2="40" stroke="{LINE}"/>')
    if not STATIC:
        p.append(f'<rect x="-300" y="38" width="300" height="4" rx="2" fill="url(#flow)" filter="url(#glow)"><animate attributeName="x" from="-300" to="{W}" dur="4s" repeatCount="indefinite"/></rect>')
    else:
        p.append(f'<rect x="450" y="38" width="300" height="4" rx="2" fill="url(#flow)"/>')
    p.append(f'<text x="{W/2}" y="86" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{TEXT}">assert(bugs == 0);  <tspan fill="{MUTED}">// never happened. keep testing.</tspan></text>')
    p.append(f'<text x="{W/2}" y="116" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">CODE.  BREAK.  FIX.  REPEAT.</text>')
    p.append("</svg>")
    write("footer.svg", "".join(p))


def section(name, label, color):
    W, H = 1100, 46
    p = [svg_open(W, H), f"<title>{esc(label)}</title>"]
    p.append(f'<text x="4" y="30" font-family="{MONO}" font-size="22" font-weight="700" fill="{color}">~/{esc(label)}</text>')
    x = 4 + (len(label) + 2) * 13.4 + 12
    p.append(f'<line x1="{x:.0f}" y1="23" x2="{W-4}" y2="23" stroke="{LINE}" stroke-width="2"/>')
    p.append(f'<circle cx="{W-8}" cy="23" r="4" fill="{color}"/>')
    p.append("</svg>")
    write(f"section-{name}.svg", "".join(p))


def contact():
    W, H = 360, 64
    p = [svg_open(W, H, f'<linearGradient id="cb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')]
    p.append("<title>LinkedIn: Serine Zargaryan</title>")
    p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{PANEL}" stroke="url(#cb)" stroke-width="1.5"/>')
    p.append(f'<rect x="16" y="14" width="36" height="36" rx="9" fill="url(#cb)"/>')
    p.append(f'<text x="34" y="39" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="800" fill="{BG}">in</text>')
    p.append(f'<text x="68" y="30" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">Let\'s connect</text>')
    p.append(f'<text x="68" y="48" font-family="{MONO}" font-size="12" fill="{MUTED}">linkedin.com/in/serinezargaryan</text>')
    p.append(f'<text x="{W-22}" y="39" text-anchor="end" font-family="{MONO}" font-size="20" fill="{CYAN}">→</text>')
    p.append("</svg>")
    write("contact.svg", "".join(p))


section("about", "about", PINK)
section("stack", "stack", CYAN)
section("projects", "projects", VIOLET)
section("contact", "contact", GREEN)
contact()
for fn in (header, terminal, stack, about, cards, footer):
    fn()
print("built ->", OUT, "static" if STATIC else "animated")
