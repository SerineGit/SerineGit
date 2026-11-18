import sys, math, html, os

STATIC = "--static" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = args[0] if args else "/home/claude/readme-game/assets"
os.makedirs(OUT, exist_ok=True)

BG, PANEL, LINE = "#080b10", "#0d121a", "#1d2733"
TEAL, ORANGE, RED, YELLOW, BLUE, PURPLE, PINK = "#2de2c4", "#ff8a3d", "#ff4d5e", "#ffd23f", "#5aa9ff", "#b98cff", "#ff7ac6"
TEXT, MUTED = "#e8eef5", "#7d8ba0"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
HEAD = "'Rajdhani','Segoe UI','Arial Narrow',Arial,sans-serif"
PS = {"triangle": "#4fd1a5", "circle": "#ff5a5f", "cross": "#6aa7ff", "square": "#f08ad0"}


def esc(s):
    return html.escape(s, quote=False)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def open_svg(w, h, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><defs>'
            f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".28"/></pattern>'
            f'<pattern id="stripes" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="3" height="14" fill="{ORANGE}" opacity=".07"/></pattern>'
            f'<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'{defs}</defs>')


def win(a, b, T):
    pts = [(0.0, 1)] if a <= 0 else [(0.0, 0), (a / T, 1)]
    if b < T:
        pts.append((b / T, 0))
    return (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(f"{k:.4f}" for k, _ in pts)}" values="{";".join(str(v) for _, v in pts)}"/>')


def glyph(kind, cx, cy, r=11, sw=2):
    c = PS[kind]
    s = f'<g fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-opacity=".55" stroke-width="1.5"/>'
    k = r * 0.48
    if kind == "triangle":
        s += f'<path d="M{cx} {cy-k} L{cx+k*1.05} {cy+k*0.8} L{cx-k*1.05} {cy+k*0.8} Z"/>'
    elif kind == "circle":
        s += f'<circle cx="{cx}" cy="{cy}" r="{k}"/>'
    elif kind == "cross":
        s += f'<path d="M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}"/>'
    else:
        s += f'<rect x="{cx-k}" y="{cy-k}" width="{2*k}" height="{2*k}"/>'
    return s + "</g>"


def corners(W, H, m=14, l=26, color=TEAL):
    d = (f"M{m} {m+l} V{m} H{m+l} M{W-m-l} {m} H{W-m} V{m+l} "
         f"M{W-m} {H-m-l} V{H-m} H{W-m-l} M{m+l} {H-m} H{m} V{H-m-l}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" opacity=".7"/>'


def bug(x, y, color=RED, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round">'
            f'<ellipse cx="0" cy="4" rx="9" ry="12" fill="{color}" fill-opacity=".25"/><circle cx="0" cy="-12" r="5" fill="{color}" fill-opacity=".35"/>'
            f'<path d="M-9 -2 L-19 -7 M-9 5 L-20 5 M-8 12 L-18 18 M9 -2 L19 -7 M9 5 L20 5 M8 12 L18 18 M-3 -16 L-7 -23 M3 -16 L7 -23"/></g>')


# ------------------------------------------------------------------------------------- HEADER
def header():
    W, H, T = 1200, 420, 9.0
    cx0, cy0 = 930, 230
    targets = [(840, 160), (1030, 270), (900, 345)]
    hits = [2.0, 4.4, 6.8]
    arrive = [1.2, 3.6, 6.0]
    p = [open_svg(W, H, f'<clipPath id="rc"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
                  f'<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
                  f'<linearGradient id="slash" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".9"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient>'
                  f'<radialGradient id="light" cx=".78" cy=".55" r=".5"><stop offset="0" stop-color="{TEAL}" stop-opacity=".22"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>')]
    p.append("<title>Serine Zargaryan - QA Operative</title>")
    p.append('<g clip-path="url(#rc)">')
    p.append(f'<rect width="{W}" height="{H}" fill="#0a0f17"/><rect width="{W}" height="{H}" fill="url(#light)"/><rect width="{W}" height="{H}" fill="url(#stripes)"/>')
    # slash accent behind title
    p.append(f'<polygon points="0,150 520,110 560,128 0,176" fill="url(#slash)" opacity=".5"/>')
    p.append(f'<polygon points="0,300 420,282 440,292 0,312" fill="{TEAL}" opacity=".18"/>')
    # top HUD
    p.append(f'<polygon points="34,30 250,30 266,46 266,100 34,100" fill="#0d141d" stroke="{LINE}"/>')
    p.append(f'<polygon points="46,42 82,42 82,88 46,88" fill="{TEAL}" opacity=".15" stroke="{TEAL}"/>')
    p.append(f'<text x="64" y="73" text-anchor="middle" font-family="{HEAD}" font-weight="800" font-size="30" fill="{TEAL}">S</text>')
    p.append(f'<text x="96" y="58" font-family="{HEAD}" font-weight="800" font-size="20" font-style="italic" letter-spacing="1" fill="{TEXT}">SERINEGIT</text>')
    p.append(f'<text x="96" y="76" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUTED}">LVL 99  /  QA OPERATIVE</text>')
    for i, (lab, col, w) in enumerate([("HP", TEAL, 150), ("AR", BLUE, 112)]):
        y = 86 + i * 0
    p.append(f'<rect x="96" y="84" width="150" height="5" fill="#16202b"/><rect x="96" y="84" width="150" height="5" fill="{TEAL}"/>')
    p.append(f'<rect x="96" y="92" width="150" height="3" fill="#16202b"/><rect x="96" y="92" width="112" height="3" fill="{BLUE}"/>')
    # title
    p.append(f'<text x="62" y="146" font-family="{MONO}" font-size="13" letter-spacing="5" fill="{ORANGE}">SEASON 2026  //  QA OPERATIVE</text>')
    p.append(f'<text x="58" y="248" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="124" letter-spacing="2" fill="{TEXT}" filter="url(#glow)">SERINE</text>')
    p.append(f'<text x="64" y="304" font-family="{HEAD}" font-weight="800" font-style="italic" font-size="58" letter-spacing="14" fill="none" stroke="{TEAL}" stroke-width="2">ZARGARYAN</text>')
    p.append(f'<text x="64" y="338" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{MUTED}">C++ DEVELOPER  /  BUG HUNTER  /  POLYGLOT</text>')
    # prompts
    x = 64
    for kind, label in [("cross", "START"), ("circle", "BACK"), ("triangle", "INVENTORY"), ("square", "SKILLS")]:
        p.append(glyph(kind, x + 11, 380, 11))
        p.append(f'<text x="{x+30}" y="385" font-family="{HEAD}" font-weight="700" font-size="15" letter-spacing="2" fill="{TEXT}">{label}</text>')
        x += 30 + len(label) * 11 + 26
    # scope area
    p.append(f'<circle cx="{cx0}" cy="{cy0}" r="150" fill="none" stroke="{TEAL}" stroke-opacity=".12"/>')
    p.append(f'<circle cx="{cx0}" cy="{cy0}" r="110" fill="none" stroke="{TEAL}" stroke-opacity=".12" stroke-dasharray="4 8"/>')
    for i, (tx, ty) in enumerate(targets):
        vis = "" if STATIC else win(0, hits[i], T)
        lab = ["BUG-4021", "BUG-1337", "BUG-0042"][i]
        p.append(f'<g>{vis}{bug(tx, ty)}<text x="{tx}" y="{ty-34}" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{RED}">{lab}</text>'
                 f'<path d="M{tx-20} {ty-28} h-6 v6 M{tx+20} {ty-28} h6 v6 M{tx-20} {ty+28} h-6 v-6 M{tx+20} {ty+28} h6 v-6" fill="none" stroke="{RED}" stroke-opacity=".7"/></g>')
        if not STATIC:
            p.append(f'<g opacity="0">{win(hits[i], hits[i]+1.1, T)}<circle cx="{tx}" cy="{ty}" r="22" fill="none" stroke="{YELLOW}" stroke-width="2"><animate attributeName="r" values="8;38" dur="1.1s" begin="0s" repeatCount="indefinite"/></circle>'
                     f'<text x="{tx}" y="{ty-4}" text-anchor="middle" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="26" fill="{YELLOW}" filter="url(#glow)">+100</text>'
                     f'<text x="{tx}" y="{ty+18}" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{TEXT}">ELIMINATED</text></g>')
    # crosshair
    cross = (f'<g transform="translate({cx0} {cy0})">'
             f'<circle r="34" fill="none" stroke="{TEAL}" stroke-width="2" filter="url(#glow)"/>'
             f'<path d="M-52 0 H-18 M18 0 H52 M0 -52 V-18 M0 18 V52" stroke="{TEAL}" stroke-width="2.5" stroke-linecap="round"/>'
             f'<circle r="2.5" fill="{TEAL}"/>')
    if not STATIC:
        for i in range(3):
            cross += f'<circle r="26" fill="none" stroke="{RED}" stroke-width="3" opacity="0">{win(arrive[i], hits[i], T)}</circle>'
        vals, kts = [(cx0, cy0)], [0.0]
        seq = [(0.5, targets[0]), (arrive[0], targets[0]), (hits[0] + .2, targets[0]), (3.0, targets[1]), (arrive[1], targets[1]), (hits[1] + .2, targets[1]),
               (5.2, targets[2]), (arrive[2], targets[2]), (hits[2] + .2, targets[2]), (7.6, (cx0, cy0))]
        for t, (x_, y_) in seq:
            kts.append(t / T)
            vals.append((x_, y_))
        kts.append(1.0)
        vals.append((cx0, cy0))
        cross += (f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" calcMode="linear" '
                  f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}" values="{";".join(f"{a} {b}" for a, b in vals)}"/>')
        cross += "</g>"
        p.append(cross)
    else:
        cross = cross.replace(f'<g transform="translate({cx0} {cy0})">', '<g>', 1)
        p.append(f'<g transform="translate({targets[0][0]} {targets[0][1]})">{cross}<circle r="26" fill="none" stroke="{RED}" stroke-width="3"/></g></g>')
    # counter
    p.append(f'<text x="{W-40}" y="62" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">BUGS ELIMINATED</text>')
    bounds = [0, hits[0], hits[1], hits[2], T]
    for i in range(4):
        w_ = "" if STATIC else win(bounds[i], bounds[i + 1], T)
        op = 1 if (STATIC and i == 0) or (not STATIC and i == 0) else (0 if STATIC else 0)
        p.append(f'<text x="{W-40}" y="100" text-anchor="end" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="40" fill="{YELLOW}" opacity="{op}">{w_}00{i}</text>')
    # ammo
    p.append(f'<text x="{W-40}" y="{H-52}" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">PRIMARY  /  C++</text>')
    p.append(f'<text x="{W-40}" y="{H-22}" text-anchor="end" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="34" fill="{TEXT}">∞ <tspan font-size="16" fill="{MUTED}">/ ∞</tspan></text>')
    p.append(corners(W, H))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/><rect width="{W}" height="{H}" fill="url(#vig)"/></g>')
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{LINE}"/></svg>')
    write("header.svg", "".join(p))


# ------------------------------------------------------------------------------------- SECTION TITLES
def section(name, label, kind, sub):
    W, H = 1100, 56
    c = PS[kind]
    p = [open_svg(W, H), f"<title>{esc(label)}</title>"]
    p.append(f'<polygon points="0,0 {W-18},0 {W},18 {W},{H} 0,{H}" fill="#0a0f17" stroke="{LINE}"/>')
    p.append(glyph(kind, 28, 28, 16, 2.4))
    p.append(f'<text x="62" y="38" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="32" letter-spacing="3" fill="{TEXT}">{esc(label)}</text>')
    tx = 62 + len(label) * 22 + 20
    p.append(f'<polygon points="{tx},14 {tx+10},14 {tx-2},42 {tx-12},42" fill="{c}" opacity=".9"/>')
    p.append(f'<text x="{tx+24}" y="35" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">{esc(sub)}</text>')
    lx = tx + 24 + len(sub) * 10 + 16
    p.append(f'<line x1="{lx}" y1="28" x2="{W-4}" y2="28" stroke="{LINE}" stroke-width="2"/><rect x="{W-34}" y="25" width="30" height="6" fill="{c}"/>')
    p.append("</svg>")
    write(f"section-{name}.svg", "".join(p))


# ------------------------------------------------------------------------------------- PROFILE
def profile():
    W, H = 1100, 300
    p = [open_svg(W, H), "<title>Player profile</title>"]
    p.append(f'<polygon points="0,0 {W-30},0 {W},30 {W},{H} 0,{H}" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#stripes)" opacity=".6"/>')
    kv = [("CLASS", "QA ENGINEER", TEAL), ("SUBCLASS", "C++ DEVELOPER", TEAL), ("TESTING", "MANUAL + AUTOMATED", TEXT), ("BASE", "LOS ANGELES, CA", TEXT),
          ("VOICE PACKS", "EN  /  日本語  /  Հայերեն", TEXT), ("COMPANIONS", "MY PETS", PINK)]
    for i, (k, v, c) in enumerate(kv):
        y = 52 + i * 40
        p.append(f'<text x="32" y="{y}" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">{k}</text>')
        p.append(f'<text x="32" y="{y+20}" font-family="{HEAD}" font-weight="800" font-style="italic" font-size="20" letter-spacing="1" fill="{c}">{esc(v)}</text>')
    p.append(f'<line x1="400" y1="24" x2="400" y2="{H-24}" stroke="{LINE}" stroke-width="2"/>')
    stats = [("BUG HUNTING", 100, RED), ("C++", 90, BLUE), ("AUTOMATION", 80, TEAL), ("DRAWING", 85, PINK), ("CHESS IQ", 75, PURPLE), ("TENNIS", 70, YELLOW), ("COFFEE", 15, ORANGE)]
    for i, (lab, val, col) in enumerate(stats):
        y = 44 + i * 36
        p.append(f'<text x="430" y="{y+13}" font-family="{HEAD}" font-weight="800" font-size="16" letter-spacing="2" fill="{TEXT}">{lab}</text>')
        n = 25
        filled = round(n * val / 100)
        for j in range(n):
            x = 590 + j * 18
            on = j < filled
            fill = col if on else "#16202b"
            op = "1" if on else "1"
            extra = ""
            if on and j == filled - 1 and not STATIC:
                extra = f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/>'
            p.append(f'<polygon points="{x+3},{y} {x+15},{y} {x+12},{y+14} {x},{y+14}" fill="{fill}" opacity="{op}">{extra}</polygon>')
        p.append(f'<text x="{590+n*18+10}" y="{y+13}" font-family="{MONO}" font-size="13" fill="{col}">{val}</text>')
    p.append("</svg>")
    write("profile.svg", "".join(p))


# ------------------------------------------------------------------------------------- LOADOUT
def loadout():
    W = 1100
    tiers = {"LEGENDARY": ORANGE, "EPIC": PURPLE, "RARE": BLUE, "UNCOMMON": TEAL}
    rows = [
        ("PRIMARY", [("C++", "heavy weapon, rock solid", "LEGENDARY"), ("PYTHON", "scripts and quick fixes", "EPIC"), ("JAVASCRIPT", "web sidearm", "EPIC")], 118),
        ("GADGETS", [("SELENIUM", "browser automation", "RARE"), ("PLAYWRIGHT", "modern e2e testing", "RARE"), ("POSTMAN", "API recon", "RARE"), ("JIRA", "mission tracker", "UNCOMMON")], 98),
        ("PERKS", [("GIT", "always save progress", "UNCOMMON"), ("MYSQL", "data vision", "UNCOMMON"), ("SNYK", "security scan", "UNCOMMON"), ("LIGHTHOUSE", "performance radar", "UNCOMMON")], 98),
    ]
    p = []
    y = 6
    body = []
    for label, items, h in rows:
        body.append(f'<text x="6" y="{y+14}" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{MUTED}">{label}</text>')
        y += 26
        n = len(items)
        gap = 14
        w = (W - 12 - gap * (n - 1)) / n
        for i, (name, desc, tier) in enumerate(items):
            x = 6 + i * (w + gap)
            c = tiers[tier]
            body.append(f'<g><polygon points="{x:.0f},{y} {x+w-18:.0f},{y} {x+w:.0f},{y+18} {x+w:.0f},{y+h} {x:.0f},{y+h}" fill="{PANEL}" stroke="{c}" stroke-opacity=".7"/>'
                        f'<polygon points="{x:.0f},{y} {x+w-18:.0f},{y} {x+w:.0f},{y+18} {x+w:.0f},{y+h} {x:.0f},{y+h}" fill="{c}" opacity=".07"/>'
                        f'<rect x="{x:.0f}" y="{y}" width="5" height="{h}" fill="{c}"/>'
                        f'<text x="{x+22:.0f}" y="{y+(46 if h>100 else 40)}" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="{34 if h>100 else 26}" letter-spacing="1" fill="{TEXT}">{name}</text>'
                        f'<text x="{x+22:.0f}" y="{y+(70 if h>100 else 62)}" font-family="{HEAD}" font-weight="600" font-size="15" fill="{MUTED}">{esc(desc)}</text>'
                        f'<text x="{x+22:.0f}" y="{y+h-14}" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{c}">{tier}</text>'
                        f'<text x="{x+w-16:.0f}" y="{y+h-14}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{TEAL}">EQUIPPED</text></g>')
        y += h + 22
    H = y
    out = [open_svg(W, H), "<title>Loadout</title>"] + body + ["</svg>"]
    write("loadout.svg", "".join(out))


# ------------------------------------------------------------------------------------- MISSIONS
def mission(fn, num, repo, obj, diff, xp, color, status, tag):
    W, H = 540, 200
    p = [open_svg(W, H, f'<clipPath id="mc"><polygon points="0,0 {W-28},0 {W},28 {W},{H} 0,{H}"/></clipPath>')]
    p.append(f"<title>{esc(repo)}</title>")
    poly = f"0,0 {W-28},0 {W},28 {W},{H} 0,{H}"
    p.append(f'<polygon points="{poly}" fill="{PANEL}" stroke="{LINE}"/><g clip-path="url(#mc)"><rect width="{W}" height="{H}" fill="url(#stripes)"/>')
    p.append(f'<rect width="6" height="{H}" fill="{color}"/>')
    if not STATIC:
        p.append(f'<rect x="0" y="{H-3}" width="90" height="3" fill="{color}"><animate attributeName="x" from="-90" to="{W}" dur="3.2s" repeatCount="indefinite"/></rect>')
    p.append("</g>")
    p.append(f'<text x="30" y="36" font-family="{MONO}" font-size="11" letter-spacing="4" fill="{color}">{esc(num)}</text>')
    stc = TEAL if status == "COMPLETE" else YELLOW
    p.append(f'<text x="{W-56}" y="36" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{stc}">{status}</text>')
    p.append(f'<circle cx="{W-44}" cy="32" r="5" fill="{stc}"/>')
    p.append(f'<text x="30" y="82" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="{30 if len(repo)<20 else 24}" letter-spacing="1" fill="{TEXT}">{esc(repo)}</text>')
    for i, l in enumerate(obj):
        p.append(f'<text x="30" y="{112+i*22}" font-family="{HEAD}" font-weight="600" font-size="16" fill="{MUTED}">{esc(l)}</text>')
    p.append(f'<line x1="30" y1="{H-52}" x2="{W-30}" y2="{H-52}" stroke="{LINE}"/>')
    p.append(f'<text x="30" y="{H-24}" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{MUTED}">DIFFICULTY</text>')
    for i in range(5):
        p.append(f'<polygon points="{128+i*16},{H-33} {138+i*16},{H-33} {135+i*16},{H-21} {125+i*16},{H-21}" fill="{color if i < diff else "#16202b"}"/>')
    p.append(f'<text x="250" y="{H-24}" font-family="{HEAD}" font-weight="800" font-size="17" fill="{YELLOW}">+{xp} XP</text>')
    p.append(f'<text x="{W-28}" y="{H-24}" text-anchor="end" font-family="{HEAD}" font-weight="800" font-style="italic" font-size="17" letter-spacing="2" fill="{color}">DEPLOY  &gt;&gt;</text>')
    p.append(f'<text x="{W-28}" y="{H-62}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{MUTED}">{esc(tag)}</text>')
    p.append("</svg>")
    write(fn, "".join(p))


def missions():
    mission("mission-1.svg", "MISSION 01", "cpp-snake-game", ["Build a classic 2D Snake in C++", "with Windows Forms."], 3, 500, TEAL, "COMPLETE", "C++")
    mission("mission-2.svg", "MISSION 02", "Apple-and-X-AI-testing", ["FE, API, performance and security tests,", "cloud automation, QA documentation."], 4, 800, PINK, "COMPLETE", "QA  /  HTML")
    mission("mission-3.svg", "MISSION 03", "Blue-Origin-and-X-AI-testing", ["Same boss fight, now fully", "equipped with Playwright."], 5, 1000, PURPLE, "COMPLETE", "QA  /  PLAYWRIGHT")
    mission("mission-4.svg", "SIDE MISSION", "Demo-Menu", ["A demo menu page in plain", "JavaScript."], 2, 250, ORANGE, "IN PROGRESS", "JAVASCRIPT")


# ------------------------------------------------------------------------------------- TROPHIES
def cup(cx, cy, color, s=1.0, glow=False):
    f = ' filter="url(#glow)"' if glow else ""
    return (f'<g transform="translate({cx} {cy}) scale({s})"{f} fill="{color}" stroke="none">'
            f'<path d="M-11 -14 H11 V-4 A11 11 0 0 1 -11 -4 Z"/><path d="M-11 -11 H-17 V-8 A7 7 0 0 0 -11 -2 Z M11 -11 H17 V-8 A7 7 0 0 1 11 -2 Z" opacity=".8"/>'
            f'<rect x="-3" y="6" width="6" height="7"/><rect x="-9" y="13" width="18" height="4" rx="1"/></g>')


def trophies():
    W = 1100
    rows = [
        ("PLATINUM", "#bfe3ff", "Bug Hunter", "Found a bug before the users did.", "ULTRA RARE"),
        ("GOLD", "#ffd23f", "Polyglot", "Speak English, Japanese and Armenian.", "RARE"),
        ("SILVER", "#c6d0dc", "Three Moves Ahead", "Plan like a chess player, test like a QA.", "RARE"),
        ("SILVER", "#c6d0dc", "Ace", "Win a point with a clean tennis serve.", "UNCOMMON"),
        ("BRONZE", "#d9894b", "Best Friend", "Cuddle the pets. Every single day.", "COMMON"),
        ("BRONZE", "#d9894b", "Edge Case", "Order -1 beers and one lizard.", "COMMON"),
    ]
    rh = 68
    H = len(rows) * rh + 8
    p = [open_svg(W, H), "<title>Trophies</title>"]
    for i, (tier, col, name, desc, rar) in enumerate(rows):
        y = 4 + i * rh
        plat = tier == "PLATINUM"
        p.append(f'<polygon points="0,{y} {W-20},{y} {W},{y+20} {W},{y+rh-6} 0,{y+rh-6}" fill="{PANEL}" stroke="{col if plat else LINE}" stroke-opacity="{.8 if plat else 1}"/>')
        if plat:
            p.append(f'<polygon points="0,{y} {W-20},{y} {W},{y+20} {W},{y+rh-6} 0,{y+rh-6}" fill="{col}" opacity=".07"/>')
            if not STATIC:
                p.append(f'<rect x="-120" y="{y+1}" width="120" height="{rh-8}" fill="#ffffff" opacity=".07"><animate attributeName="x" from="-120" to="{W}" dur="4s" repeatCount="indefinite"/></rect>')
        p.append(f'<circle cx="46" cy="{y+31}" r="24" fill="{col}" opacity=".1"/>')
        p.append(cup(46, y + 30, col, 1.25, plat))
        p.append(f'<text x="92" y="{y+30}" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="25" letter-spacing="1" fill="{TEXT}">{esc(name)}</text>')
        p.append(f'<text x="92" y="{y+50}" font-family="{HEAD}" font-weight="600" font-size="15" fill="{MUTED}">{esc(desc)}</text>')
        p.append(f'<text x="{W-34}" y="{y+28}" text-anchor="end" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="20" letter-spacing="3" fill="{col}">{tier}</text>')
        p.append(f'<text x="{W-34}" y="{y+48}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{MUTED}">{rar}</text>')
    p.append("</svg>")
    write("trophies.svg", "".join(p))


# ------------------------------------------------------------------------------------- SIDE QUESTS
def side():
    W = 1100
    groups = [("SIDE QUESTS", YELLOW, ["Tennis", "Chess", "Drawing", "Reading comics", "PlayStation", "Marvel"]),
              ("COMPANIONS", PINK, ["My pets"]),
              ("VOICE PACKS", TEAL, ["English", "日本語", "Հայերեն"])]
    body, y = [], 8
    for gname, col, items in groups:
        body.append(f'<text x="6" y="{y+14}" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{col}">{gname}</text>')
        y += 28
        x = 6
        for it in items:
            wide = sum(1.0 if ord(ch) < 0x2E80 else 1.9 for ch in it)
            w = wide * 13.2 + 62
            body.append(f'<g><polygon points="{x:.0f},{y} {x+w-12:.0f},{y} {x+w:.0f},{y+12} {x+w:.0f},{y+38} {x:.0f},{y+38}" fill="{PANEL}" stroke="{LINE}"/>'
                        f'<rect x="{x:.0f}" y="{y}" width="4" height="38" fill="{col}"/>'
                        f'<polygon points="{x+18:.0f},{y+13} {x+30:.0f},{y+19} {x+18:.0f},{y+25}" fill="{col}"/>'
                        f'<text x="{x+40:.0f}" y="{y+26}" font-family="{HEAD}" font-weight="800" font-size="18" letter-spacing="1" fill="{TEXT}">{esc(it).upper()}</text></g>')
            x += w + 12
        y += 38 + 22
    out = [open_svg(W, y), "<title>Side quests</title>"] + body + ["</svg>"]
    write("side.svg", "".join(out))


# ------------------------------------------------------------------------------------- CONTACT / FOOTER
def contact():
    W, H = 440, 76
    p = [open_svg(W, H)]
    p.append("<title>Continue: LinkedIn</title>")
    poly = f"0,0 {W-20},0 {W},20 {W},{H} 0,{H}"
    p.append(f'<polygon points="{poly}" fill="{PANEL}" stroke="{TEAL}" stroke-width="1.6">'
             + ("" if STATIC else '<animate attributeName="stroke-opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/>') + "</polygon>")
    p.append(glyph("cross", 40, 38, 17, 2.6))
    p.append(f'<text x="78" y="36" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="26" letter-spacing="3" fill="{TEXT}">CONTINUE</text>')
    p.append(f'<text x="78" y="56" font-family="{MONO}" font-size="12" fill="{MUTED}">linkedin.com/in/serinezargaryan</text>')
    p.append(f'<text x="{W-30}" y="46" text-anchor="end" font-family="{HEAD}" font-weight="900" font-size="28" fill="{TEAL}">&gt;&gt;</text>')
    p.append("</svg>")
    write("contact.svg", "".join(p))


def footer():
    W, H = 1100, 100
    p = [open_svg(W, H)]
    p.append("<title>Autosaving</title>")
    p.append(f'<polygon points="0,0 {W-24},0 {W},24 {W},{H} 0,{H}" fill="{PANEL}" stroke="{LINE}"/>')
    # spinner
    spin = f'<g transform="translate(56 50)"><circle r="16" fill="none" stroke="{LINE}" stroke-width="4"/><path d="M0 -16 A16 16 0 0 1 16 0" fill="none" stroke="{TEAL}" stroke-width="4" stroke-linecap="round">'
    if not STATIC:
        spin += '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="1.2s" repeatCount="indefinite"/>'
    spin += "</path></g>"
    p.append(spin)
    p.append(f'<text x="94" y="46" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="26" letter-spacing="3" fill="{TEXT}">AUTOSAVING...<tspan fill="{TEAL}"> </tspan></text>')
    p.append(f'<text x="94" y="68" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">DO NOT CLOSE THIS TAB.  BUGS WILL BE FOUND.</text>')
    p.append(f'<text x="{W-40}" y="46" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">BUGS ELIMINATED</text>')
    p.append(f'<text x="{W-40}" y="76" text-anchor="end" font-family="{HEAD}" font-weight="900" font-style="italic" font-size="34" fill="{YELLOW}">∞</text>')
    p.append("</svg>")
    write("footer.svg", "".join(p))


section("loadout", "LOADOUT", "triangle", "TECH STACK")
section("profile", "PLAYER PROFILE", "circle", "STATS")
section("missions", "MISSIONS", "cross", "PROJECTS")
section("trophies", "TROPHIES", "square", "ACHIEVEMENTS")
section("side", "SIDE QUESTS", "triangle", "OFF DUTY")
section("contact", "CONTINUE", "cross", "CONTACT")
for fn in (header, profile, loadout, missions, trophies, side, contact, footer):
    fn()
print("built ->", OUT, "static" if STATIC else "animated")
