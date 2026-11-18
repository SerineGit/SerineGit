import sys, math, html, os, random

STATIC = "--static" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = args[0] if args else "/home/claude/readme-matrix-v3/assets"
os.makedirs(OUT, exist_ok=True)

BG, PANEL, LINE = "#020805", "#04130a", "#0f3a1c"
G, G2, G3, GD = "#00ff41", "#8dffb0", "#19b84a", "#0a5c1f"
WHITE, MUTED, RED, BLUE, AMBER = "#d7ffe3", "#4f9c68", "#ff2a2a", "#2a7bff", "#ffd23f"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "Inter,'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
random.seed(7)


def esc(s):
    return html.escape(s, quote=False)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def open_svg(w, h, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><defs>'
            f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>'
            f'<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'{defs}</defs>')


def stepped(attr, values, start, dt, T):
    n = len(values) - 1
    kt = [0.0] + [(start + j * dt) / T for j in range(n)]
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(str(v) for v in values)}"/>')


def win(a, b, T):
    pts = [(0.0, 1)] if a <= 0 else [(0.0, 0), (a / T, 1)]
    if b < T:
        pts.append((b / T, 0))
    return (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(f"{k:.4f}" for k, _ in pts)}" values="{";".join(str(v) for _, v in pts)}"/>')


def flash(times, T, dur=0.07):
    kt, vs = [0.0], [0]
    for t in times:
        for j, v in enumerate((1, 0, 1, 0)):
            kt.append((t + j * dur) / T)
            vs.append(v)
    return (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(str(v) for v in vs)}"/>')


def corners(W, H, m=14, l=26, color=G):
    d = (f"M{m} {m+l} V{m} H{m+l} M{W-m-l} {m} H{W-m} V{m+l} M{W-m} {H-m-l} V{H-m} H{W-m-l} M{m+l} {H-m} H{m} V{H-m-l}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" opacity=".6"/>'


KANA = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789:.=*+-"


def rain(x0, x1, H, step, n, T_lo=6, T_hi=12, op=1.0):
    out = []
    cols = int((x1 - x0) / step)
    ch_h = 18
    colh = n * ch_h
    for i in range(cols):
        x = x0 + i * step + step / 2
        d = random.uniform(T_lo, T_hi)
        off = -random.uniform(0, d)
        s = f'<g opacity="{op}">'
        for k in range(n):
            a = ((k + 1) / n) ** 2.2
            c = WHITE if k == n - 1 else G
            s += f'<text x="{x:.0f}" y="{k*ch_h+14}" fill="{c}" fill-opacity="{a*0.95:.2f}">{esc(random.choice(KANA))}</text>'
        base_y = random.uniform(-colh, H)
        anim = "" if STATIC else (f'<animateTransform attributeName="transform" type="translate" values="0 {-colh};0 {H+20}" dur="{d:.1f}s" begin="{off:.1f}s" repeatCount="indefinite"/>')
        out.append(f'<g transform="translate(0 {base_y:.0f})">{s}{anim}</g></g>')
    return f'<g font-family="{MONO}" font-size="15" text-anchor="middle">' + "".join(out) + "</g>"


# ------------------------------------------------------------------------------------- HEADER
def header():
    W, H, T = 1200, 420, 15.0
    p = [open_svg(W, H, '<clipPath id="rc"><rect width="1200" height="420" rx="16"/></clipPath>'
                  f'<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG}" stop-opacity=".72"/><stop offset=".55" stop-color="{BG}" stop-opacity=".5"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
                  f'<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".8"/></radialGradient>'
                  f'<linearGradient id="redp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a7a"/><stop offset="1" stop-color="{RED}"/></linearGradient>'
                  f'<linearGradient id="bluep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb0ff"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>')]
    p.append("<title>Serine Zargaryan - Wake up, Serine</title>")
    p.append('<g clip-path="url(#rc)">')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(rain(8, 1192, H, 20, 22, 5, 11))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#fadeL)" x="0"/>')
    # left text
    p.append(f'<text x="64" y="64" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{MUTED}">SYSTEM://MATRIX   USER: SERINEGIT   STATUS: AWAKE</text>')
    name = "SERINE ZARGARYAN"
    nm = f'font-family="{MONO}" font-size="58" font-weight="800" letter-spacing="1"'
    p.append(f'<text x="62" y="146" {nm} fill="{RED}" opacity="0">{"" if STATIC else flash([3.2, 9.4], T)}{name}</text>')
    p.append(f'<text x="66" y="146" {nm} fill="{BLUE}" opacity="0">{"" if STATIC else flash([3.2, 9.4], T)}{name}</text>')
    p.append(f'<text x="64" y="146" {nm} fill="{G}" filter="url(#glow)">{name}</text>')
    p.append(f'<text x="66" y="188" font-family="{MONO}" font-size="16" letter-spacing="5" fill="{G2}">QA ENGINEER  /  C++ DEVELOPER</text>')
    phrases = ["> Wake up, Serine...", "> The Matrix has you...", "> Follow the white rabbit."]
    sl = T / len(phrases)
    cw, fs, x0, y0 = 14.4, 24, 66, 252
    for i, ph in enumerate(phrases):
        if STATIC and i != 1:
            continue
        s = i * sl + 0.4
        n = len(ph)
        dt = 0.08
        vals = [0] + [round((j + 1) * cw, 1) for j in range(n)]
        full = round((n + 1) * cw, 1)
        cid = f"hp{i}"
        anim_w = "" if STATIC else stepped("width", vals, s, dt, T)
        p.append(f'<clipPath id="{cid}"><rect x="{x0}" y="{y0-fs}" width="{full}" height="{fs+10}">{anim_w}</rect></clipPath>')
        p.append(f'<g opacity="{1 if (STATIC or i==0) else 0}">' + ("" if STATIC else win(i * sl, (i + 1) * sl, T)))
        p.append(f'<text x="{x0}" y="{y0}" font-family="{MONO}" font-size="{fs}" fill="{WHITE}" clip-path="url(#{cid})">{esc(ph)}</text>')
        cur_vals = [x0] + [round(x0 + (j + 1) * cw, 1) for j in range(n)]
        cur_anim = "" if STATIC else stepped("x", cur_vals, s, dt, T)
        p.append(f'<rect x="{x0 + n*cw}" y="{y0-fs+3}" width="11" height="{fs}" fill="{G}">{cur_anim}</rect></g>')
    p.append(f'<text x="66" y="298" font-family="{MONO}" font-size="15" fill="{G3}">while (true) {{ code(); breakIt(); fix(); }}</text>')
    px = 66
    for label in ["Manual + Automated", "Los Angeles, CA", "English / 日本語 / Հայերեն"]:
        w = len(label) * 7.9 + 36
        p.append(f'<rect x="{px}" y="322" width="{w:.0f}" height="30" rx="4" fill="{BG}" fill-opacity=".85" stroke="{GD}"/>')
        p.append(f'<rect x="{px+12}" y="334" width="6" height="6" fill="{G}"/>')
        p.append(f'<text x="{px+28}" y="342" font-family="{MONO}" font-size="12.5" fill="{WHITE}">{esc(label)}</text>')
        px += w + 12
    # pills
    def pill(cx, cy, rot, grad, glowc, d, ph):
        fl = "" if STATIC else f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -9;0 0" dur="{d}s" begin="{ph}s" repeatCount="indefinite"/>'
        return (f'<g transform="translate({cx} {cy})"><g>{fl}<g transform="rotate({rot})" filter="url(#glow)">'
                f'<rect x="-52" y="-22" width="104" height="44" rx="22" fill="url(#{grad})"/>'
                f'<path d="M0 -22 H30 A22 22 0 0 1 30 22 H0 Z" fill="#000" opacity=".28"/>'
                f'<rect x="-44" y="-15" width="70" height="7" rx="3.5" fill="#fff" opacity=".35"/></g></g></g>')
    p.append(pill(985, 150, -28, "redp", RED, 3.4, 0))
    p.append(pill(1075, 255, 24, "bluep", BLUE, 4.1, -1.3))
    p.append(f'<text x="985" y="206" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{RED}">RED</text>')
    p.append(f'<text x="1075" y="310" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{BLUE}">BLUE</text>')
    p.append(f'<text x="{W-44}" y="{H-30}" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{G2}">CHOOSE.</text>')
    p.append(corners(W, H))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/><rect width="{W}" height="{H}" fill="url(#vig)"/></g>')
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{LINE}"/></svg>')
    write("header.svg", "".join(p))


# ------------------------------------------------------------------------------------- TERMINAL
def terminal():
    W, H, T = 1100, 430, 20.0
    fs, cw, lh, x0 = 15, 9.0, 26, 34
    P = "serine@zion"
    lines = [
        ([(P, G), (":~$ ", MUTED), ("whoami", WHITE)], 0.07),
        ([("serine zargaryan  //  QA engineer by day, C++ developer by heart", G2)], 0.012),
        ([], 0),
        ([(P, G), (":~$ ", MUTED), ("./run_tests --suite=matrix", WHITE)], 0.07),
        ([("  [ PASS ] ", G), ("reality.check()", WHITE)], 0.02),
        ([("  [ PASS ] ", G), ("spoon.exists() == false  ", WHITE), ("// there is no spoon", MUTED)], 0.02),
        ([("  [ PASS ] ", G), ("bugs.find()  ", WHITE), ("// always", MUTED)], 0.02),
        ([("  [ PASS ] ", G), ("languages == {en, ja, hy}", WHITE)], 0.02),
        ([("  [ PASS ] ", G), ("pets.cuddle()", WHITE)], 0.02),
        ([("  [ WARN ] ", AMBER), ("coffee.level == 0", WHITE)], 0.02),
        ([], 0),
        ([("  5 passed, ", WHITE), ("1 warning", AMBER), (", 0 failed", WHITE)], 0.02),
        ([], 0),
        ([(P, G), (":~$ ", MUTED)], 0.07),
    ]
    p = [open_svg(W, H, '<clipPath id="tw"><rect width="1100" height="430" rx="14"/></clipPath>')]
    p.append("<title>Terminal: whoami and run_tests</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{GD}"/>')
    p.append(f'<g clip-path="url(#tw)"><rect width="{W}" height="42" fill="{PANEL}"/><line x1="0" y1="42" x2="{W}" y2="42" stroke="{LINE}"/></g>')
    for i, c in enumerate([RED, AMBER, G]):
        p.append(f'<circle cx="{26+i*22}" cy="21" r="6.5" fill="{c}" opacity=".85"/>')
    p.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">serine@zion: ~/matrix</text>')
    t, y, cur = 0.6, 82, None
    for idx, (segs, dt) in enumerate(lines):
        if not segs:
            t += 0.25
            y += lh
            continue
        total = sum(len(s) for s, _ in segs)
        vals = [0] + [round((j + 1) * cw, 1) for j in range(total)]
        full = round((total + 1) * cw, 1)
        anim = "" if STATIC else stepped("width", vals, t, dt, T)
        p.append(f'<clipPath id="tl{idx}"><rect x="{x0}" y="{y-fs-2}" width="{full}" height="{fs+9}">{anim}</rect></clipPath>')
        tsp = "".join(f'<tspan fill="{c}">{esc(s).replace(" ", chr(160))}</tspan>' for s, c in segs)
        p.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" clip-path="url(#tl{idx})" xml:space="preserve">{tsp}</text>')
        cur = (x0 + total * cw, y, t + total * dt)
        t += total * dt + (0.7 if dt >= 0.07 else 0.25)
        y += lh
    cx_, cy_, ap = cur
    op = "" if STATIC else ' opacity="0"'
    an = "" if STATIC else f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{ap/T:.4f}" values="0;1"/>'
    p.append(f'<rect x="{cx_}" y="{cy_-fs}" width="9" height="{fs+3}" fill="{G}"{op}>{an}</rect>')
    p.append("</svg>")
    write("terminal.svg", "".join(p))


# ------------------------------------------------------------------------------------- SECTION TITLES
def section(name, label, sub):
    W, H = 1100, 56
    p = [open_svg(W, H), f"<title>{esc(label)}</title>"]
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="{BG}" stroke="{LINE}"/>')
    p.append(f'<text x="22" y="36" font-family="{MONO}" font-size="22" font-weight="800" fill="{G}" filter="url(#glow)">//</text>')
    p.append(f'<text x="58" y="36" font-family="{MONO}" font-size="22" font-weight="800" letter-spacing="3" fill="{WHITE}">{esc(label)}</text>')
    tx = 58 + len(label) * 16 + 20
    p.append(f'<text x="{tx}" y="35" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">{esc(sub)}</text>')
    lx = tx + len(sub) * 10 + 16
    p.append(f'<line x1="{lx}" y1="28" x2="{W-50}" y2="28" stroke="{GD}" stroke-width="1.5"/>')
    p.append(f'<rect x="{W-40}" y="24" width="10" height="8" fill="{G}">' + ("" if STATIC else '<animate attributeName="opacity" values="1;0" keyTimes="0;.5" dur="1s" calcMode="discrete" repeatCount="indefinite"/>') + "</rect>")
    p.append("</svg>")
    write(f"section-{name}.svg", "".join(p))


# ------------------------------------------------------------------------------------- PROFILE
def profile():
    W, H = 1100, 300
    p = [open_svg(W, H), "<title>Operator file</title>"]
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{PANEL}" stroke="{LINE}"/>')
    kv = [("CLASS", "QA ENGINEER", G), ("SUBCLASS", "C++ DEVELOPER", G), ("TESTING", "MANUAL + AUTOMATED", WHITE), ("BASE", "LOS ANGELES, CA", WHITE),
          ("VOICE", "EN  /  日本語  /  Հայերեն", WHITE), ("COMPANIONS", "MY PETS", G2)]
    for i, (k, v, c) in enumerate(kv):
        y = 50 + i * 40
        p.append(f'<text x="32" y="{y}" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">{k}</text>')
        p.append(f'<text x="32" y="{y+20}" font-family="{MONO}" font-weight="700" font-size="18" fill="{c}">{esc(v)}</text>')
    p.append(f'<line x1="400" y1="24" x2="400" y2="{H-24}" stroke="{LINE}" stroke-width="2"/>')
    stats = [("BUG HUNTING", 100, G), ("C++", 90, G), ("AUTOMATION", 80, G), ("DRAWING", 85, G), ("CHESS IQ", 75, G), ("TENNIS", 70, G), ("COFFEE", 15, AMBER)]
    for i, (lab, val, col) in enumerate(stats):
        y = 44 + i * 36
        p.append(f'<text x="430" y="{y+13}" font-family="{MONO}" font-weight="700" font-size="14" letter-spacing="2" fill="{WHITE}">{lab}</text>')
        n, filled = 25, round(25 * val / 100)
        for j in range(n):
            x = 590 + j * 18
            on = j < filled
            extra = '<animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/>' if (on and j == filled - 1 and not STATIC) else ""
            p.append(f'<rect x="{x}" y="{y}" width="13" height="14" fill="{col if on else "#0a1f10"}">{extra}</rect>')
        p.append(f'<text x="{590+n*18+10}" y="{y+13}" font-family="{MONO}" font-size="13" fill="{col}">{val}</text>')
    p.append("</svg>")
    write("profile.svg", "".join(p))


# ------------------------------------------------------------------------------------- CHIPS
def chips(name, title, groups, W=1100, fs=14):
    pad, rh, gap = 28, 40, 10
    body, y = [], 26
    for gname, color, items in groups:
        body.append(f'<text x="{pad}" y="{y+14}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{color}">{esc(gname)}</text>')
        body.append(f'<line x1="{pad+len(gname)*10+14}" y1="{y+10}" x2="{W-pad}" y2="{y+10}" stroke="{LINE}"/>')
        y += 30
        x = pad
        for it in items:
            wide = sum(1.0 if ord(ch) < 0x2E80 else 1.9 for ch in it)
            w = wide * fs * 0.62 + 44
            if x + w > W - pad:
                x, y = pad, y + rh
            body.append(f'<g><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="32" rx="4" fill="{PANEL}" stroke="{GD}"/>'
                        f'<rect x="{x+12:.0f}" y="{y+13}" width="6" height="6" fill="{color}"/>'
                        f'<text x="{x+28:.0f}" y="{y+21}" font-family="{MONO}" font-size="{fs-1}" fill="{WHITE}">{esc(it)}</text></g>')
            x += w + gap
        y += rh + 14
    H = y + 6
    out = [open_svg(W, H), f"<title>{esc(title)}</title>", f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{LINE}"/>'] + body + ["</svg>"]
    write(name, "".join(out))


def about():
    chips("about.svg", "About Serine", [("LOVES", G, ["My pets", "PlayStation", "Marvel"]),
                                         ("HOBBIES", G2, ["Tennis", "Chess", "Drawing", "Reading comics"]),
                                         ("SPEAKS", G3, ["English", "日本語", "Հայերեն"])])


def tools():
    chips("tools.svg", "Tools and environments", [
        ("QA", G, ["Manual testing", "Test automation", "API testing", "Performance", "Security testing"]),
        ("TOOLS", G2, ["Jira", "Confluence", "GitHub", "VS Code", "PyCharm", "WebStorm", "Node.js", "Snyk", "Lighthouse", "VirtualBox", "Slack", "Zoom"]),
        ("ENVIRONMENTS", G3, ["Chrome", "Firefox", "Edge", "Safari", "Opera", "Android", "iOS", "Windows", "macOS"])])


# ------------------------------------------------------------------------------------- TRAINING (upload)
def upload():
    W, T = 1100, 16.0
    rows = ["C++", "Python", "JavaScript", "SQL", "HTML + CSS", "Selenium", "Playwright", "Postman", "Git"]
    H = 84 + len(rows) * 40 + 16
    p = [open_svg(W, H), "<title>Training program: skills loaded</title>"]
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="8" fill="{BG}" stroke="{LINE}"/>')
    p.append(f'<text x="30" y="42" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{G}">TRAINING PROGRAM  //  UPLOAD</text>')
    p.append(f'<text x="{W-30}" y="42" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">9 / 9 PROGRAMS LOADED</text>')
    p.append(f'<line x1="30" y1="58" x2="{W-30}" y2="58" stroke="{LINE}"/>')
    bw = 520
    for i, name in enumerate(rows):
        y = 84 + i * 40
        st = i * 0.7 + 0.5
        en = st + 2.0
        p.append(f'<text x="30" y="{y+14}" font-family="{MONO}" font-size="15" font-weight="700" fill="{WHITE}">{esc(name)}</text>')
        p.append(f'<rect x="240" y="{y+2}" width="{bw}" height="14" rx="2" fill="#071a0d" stroke="{GD}"/>')
        if STATIC:
            anim = ""
        else:
            anim = (f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="linear" keyTimes="0;{st/T:.4f};{en/T:.4f};1" values="0;0;{bw-4};{bw-4}"/>')
        p.append(f'<rect x="242" y="{y+4}" width="{bw-4}" height="10" fill="{G}" filter="url(#glow)">{anim}</rect>')
        p.append(f'<text x="{240+bw+16}" y="{y+14}" font-family="{MONO}" font-size="13" fill="{G}">100%</text>')
        op = "" if STATIC else ' opacity="0"'
        sa = "" if STATIC else f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{en/T:.4f}" values="0;1"/>'
        p.append(f'<text x="{W-30}" y="{y+14}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{G2}"{op}>{sa}I know {esc(name)}.</text>')
    p.append("</svg>")
    write("upload.svg", "".join(p))


# ------------------------------------------------------------------------------------- PROGRAM CARDS
def card(fn, repo, desc, tag, num):
    W, H = 540, 176
    p = [open_svg(W, H, '<clipPath id="cc"><rect width="540" height="176" rx="10"/></clipPath>')]
    p.append(f"<title>{esc(repo)}</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{PANEL}" stroke="{GD}"/>')
    p.append(f'<g clip-path="url(#cc)"><rect width="{W}" height="3" fill="{G}" opacity=".5"/>')
    if not STATIC:
        p.append(f'<rect width="120" height="3" fill="{WHITE}"><animate attributeName="x" from="-120" to="{W}" dur="3.5s" repeatCount="indefinite"/></rect>')
    p.append("</g>")
    p.append(f'<text x="26" y="40" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">PROGRAM {num}</text>')
    p.append(f'<text x="{W-26}" y="40" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{G}">EXIT CODE 0</text>')
    p.append(f'<text x="26" y="76" font-family="{MONO}" font-size="{19 if len(repo)<22 else 16}" font-weight="800" fill="{WHITE}"><tspan fill="{G}">&gt;_ </tspan>{esc(repo)}</text>')
    for i, l in enumerate(desc):
        p.append(f'<text x="26" y="{104+i*22}" font-family="{SANS}" font-size="14.5" fill="{G2}" fill-opacity=".75">{esc(l)}</text>')
    p.append(f'<line x1="26" y1="{H-46}" x2="{W-26}" y2="{H-46}" stroke="{LINE}"/>')
    p.append(f'<rect x="26" y="{H-31}" width="7" height="7" fill="{G}"/>')
    p.append(f'<text x="42" y="{H-24}" font-family="{MONO}" font-size="12" fill="{WHITE}">{esc(tag)}</text>')
    p.append(f'<text x="{W-26}" y="{H-24}" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{G}">RUN  &gt;&gt;</text>')
    p.append("</svg>")
    write(fn, "".join(p))


def cards():
    card("card-1.svg", "cpp-snake-game", ["Classic 2D Snake game built with", "C++ and Windows Forms."], "C++", "01")
    card("card-2.svg", "Apple-and-X-AI-testing", ["Front-end, API, performance and security", "testing, cloud automation, QA docs."], "QA  /  HTML", "02")
    card("card-3.svg", "Blue-Origin-and-X-AI-testing", ["The full QA cycle again, now with", "Playwright and cloud automation."], "QA  /  Playwright", "03")
    card("card-4.svg", "Demo-Menu", ["A demo menu page: layout and", "interaction in plain JavaScript."], "JavaScript", "04")


# ------------------------------------------------------------------------------------- ACHIEVEMENTS
def cup(cx, cy, color, s=1.0, glow=False):
    f = ' filter="url(#glow)"' if glow else ""
    return (f'<g transform="translate({cx} {cy}) scale({s})"{f} fill="{color}">'
            f'<path d="M-11 -14 H11 V-4 A11 11 0 0 1 -11 -4 Z"/><path d="M-11 -11 H-17 V-8 A7 7 0 0 0 -11 -2 Z M11 -11 H17 V-8 A7 7 0 0 1 11 -2 Z" opacity=".8"/>'
            f'<rect x="-3" y="6" width="6" height="7"/><rect x="-9" y="13" width="18" height="4" rx="1"/></g>')


def trophies():
    W = 1100
    rows = [("THE ONE", WHITE, "Bug Hunter", "Found a bug before the users did.", "ULTRA RARE"),
            ("ARCHITECT", G, "Polyglot", "Speak English, Japanese and Armenian.", "RARE"),
            ("OPERATOR", G3, "Three Moves Ahead", "Plan like a chess player, test like a QA.", "RARE"),
            ("OPERATOR", G3, "Ace", "Win a point with a clean tennis serve.", "UNCOMMON"),
            ("REBEL", GD, "Best Friend", "Cuddle the pets. Every single day.", "COMMON"),
            ("REBEL", GD, "Edge Case", "Order -1 beers and one lizard.", "COMMON")]
    rh = 68
    H = len(rows) * rh + 8
    p = [open_svg(W, H), "<title>Achievements</title>"]
    for i, (tier, col, name, desc, rar) in enumerate(rows):
        y = 4 + i * rh
        top = i == 0
        p.append(f'<rect x=".5" y="{y}" width="{W-1}" height="{rh-6}" rx="6" fill="{PANEL}" stroke="{col if top else LINE}"/>')
        if top and not STATIC:
            p.append(f'<rect x="-120" y="{y+1}" width="120" height="{rh-8}" fill="{G}" opacity=".08"><animate attributeName="x" from="-120" to="{W}" dur="4s" repeatCount="indefinite"/></rect>')
        p.append(f'<circle cx="46" cy="{y+31}" r="24" fill="{col}" opacity=".1"/>')
        p.append(cup(46, y + 30, col if col != GD else G3, 1.25, top))
        p.append(f'<text x="92" y="{y+30}" font-family="{MONO}" font-weight="800" font-size="21" fill="{WHITE}">{esc(name)}</text>')
        p.append(f'<text x="92" y="{y+50}" font-family="{SANS}" font-size="14" fill="{G2}" fill-opacity=".7">{esc(desc)}</text>')
        p.append(f'<text x="{W-34}" y="{y+28}" text-anchor="end" font-family="{MONO}" font-weight="800" font-size="16" letter-spacing="3" fill="{col if col != GD else G3}">{tier}</text>')
        p.append(f'<text x="{W-34}" y="{y+48}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{MUTED}">{rar}</text>')
    p.append("</svg>")
    write("trophies.svg", "".join(p))


# ------------------------------------------------------------------------------------- PILLS + FOOTER
def pill_btn(fn, kind, title, sub, link_text):
    W, H = 440, 88
    c, grad = (RED, "redp") if kind == "red" else (BLUE, "bluep")
    p = [open_svg(W, H, f'<linearGradient id="redp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a7a"/><stop offset="1" stop-color="{RED}"/></linearGradient>'
                       f'<linearGradient id="bluep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb0ff"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>')]
    p.append(f"<title>{esc(title)}</title>")
    pulse = "" if STATIC else f'<animate attributeName="stroke-opacity" values="1;.3;1" dur="2.2s" repeatCount="indefinite"/>'
    p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{PANEL}" stroke="{c}" stroke-width="1.6">{pulse}</rect>')
    p.append(f'<g transform="translate(56 44) rotate(-28)" filter="url(#glow)"><rect x="-32" y="-14" width="64" height="28" rx="14" fill="url(#{grad})"/>'
             f'<path d="M0 -14 H18 A14 14 0 0 1 18 14 H0 Z" fill="#000" opacity=".28"/><rect x="-26" y="-9" width="42" height="5" rx="2.5" fill="#fff" opacity=".35"/></g>')
    p.append(f'<text x="108" y="40" font-family="{MONO}" font-weight="800" font-size="22" letter-spacing="2" fill="{c}">{esc(title)}</text>')
    p.append(f'<text x="108" y="62" font-family="{MONO}" font-size="11.5" fill="{G2}" fill-opacity=".8">{esc(sub)}</text>')
    p.append(f'<text x="{W-26}" y="52" text-anchor="end" font-family="{MONO}" font-weight="800" font-size="26" fill="{c}">&gt;&gt;</text>')
    p.append("</svg>")
    write(fn, "".join(p))


def pills():
    pill_btn("pill-red.svg", "red", "RED PILL", "Stay in Wonderland. Connect on LinkedIn.", "")
    pill_btn("pill-blue.svg", "blue", "BLUE PILL", "The story ends. Close the tab.", "")


def footer():
    W, H, T = 1100, 120, 12.0
    p = [open_svg(W, H, f'<linearGradient id="flow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".5" stop-color="{G}"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></linearGradient>')]
    p.append("<title>There is no spoon</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{LINE}"/>')
    p.append(rain(10, W - 10, H, 20, 7, 4, 8, 1.0))
    p.append(f'<rect x="230" y="14" width="{W-460}" height="{H-28}" rx="8" fill="{BG}" opacity=".82"/>')
    p.append(f'<text x="{W/2}" y="56" text-anchor="middle" font-family="{MONO}" font-size="20" fill="{WHITE}">There is no spoon. <tspan fill="{G}">Only test cases.</tspan></text>')
    p.append(f'<text x="{W/2}" y="86" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{MUTED}">WAKE UP, SERINE. THE MATRIX HAS YOU.</text>')
    if not STATIC:
        p.append(f'<rect x="200" y="{H-4}" width="240" height="2" fill="url(#flow)" filter="url(#glow)"><animate attributeName="x" from="200" to="{W-440}" dur="3.5s" repeatCount="indefinite"/></rect>')
    p.append("</svg>")
    write("footer.svg", "".join(p))



# ======================================================================= v2: everything as terminals
def term(fn, title, lines, W=1100, fs=15, cw=9.0, lh=26, x0=34, bar=42, top=None, hold=6.0, title_fs=13, tail=30, r=14):
    top = top if top is not None else bar + 40
    # timing pass
    t, plan = 0.6, []
    for segs, dt in lines:
        if not segs:
            t += 0.25
            plan.append(None)
            continue
        total = sum(len(s) for s, _ in segs)
        plan.append((t, total, dt))
        t += total * dt + (0.6 if dt >= 0.05 else 0.18)
    T = round(t + hold, 1)
    H = top + len(lines) * lh + tail
    p = [open_svg(W, H, f'<clipPath id="tw"><rect width="{W}" height="{H}" rx="{r}"/></clipPath>')]
    p.append(f"<title>{esc(title)}</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{r}" fill="{BG}" stroke="{GD}"/>')
    p.append(f'<g clip-path="url(#tw)"><rect width="{W}" height="{bar}" fill="{PANEL}"/><line x1="0" y1="{bar}" x2="{W}" y2="{bar}" stroke="{LINE}"/></g>')
    dr = 6.5 if bar >= 40 else 5
    for i, c in enumerate([RED, AMBER, G]):
        p.append(f'<circle cx="{24+i*(dr*3.2):.0f}" cy="{bar/2}" r="{dr}" fill="{c}" opacity=".85"/>')
    p.append(f'<text x="{W/2}" y="{bar/2+4.5}" text-anchor="middle" font-family="{MONO}" font-size="{title_fs}" fill="{MUTED}">{esc(title)}</text>')
    y, cur = top, None
    for idx, ((segs, dt), pl) in enumerate(zip(lines, plan)):
        if pl is None:
            y += lh
            continue
        st, total, dt = pl
        flat = "".join(sg for sg, _ in segs)
        def cells(ch):
            o = ord(ch)
            return 1.75 if o >= 0x2E80 else (1.25 if 0x0530 <= o < 0x0590 else 1.0)
        cum, acc = [], 0.0
        for ch in flat:
            acc += cells(ch) * cw
            cum.append(round(acc, 1))
        wide_line = any(ord(ch) >= 0x0530 for ch in flat)
        vals = [0] + cum
        full = round(acc + cw * (3 if wide_line else 1), 1)
        anim = "" if STATIC else stepped("width", vals, st, dt, T)
        p.append(f'<clipPath id="tl{idx}"><rect x="{x0}" y="{y-fs-2}" width="{full}" height="{fs+9}">{anim}</rect></clipPath>')
        tsp = "".join(f'<tspan fill="{c}">{esc(s).replace(" ", chr(160))}</tspan>' for s, c in segs)
        p.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" clip-path="url(#tl{idx})" xml:space="preserve">{tsp}</text>')
        cur = (x0 + acc, y, st + total * dt)
        y += lh
    cx_, cy_, ap = cur
    op = "" if STATIC else ' opacity="0"'
    an = "" if STATIC else f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{ap/T:.4f}" values="0;1"/>'
    p.append(f'<rect x="{cx_}" y="{cy_-fs}" width="{cw}" height="{fs+3}" fill="{G}"{op}>{an}</rect>')
    p.append("</svg>")
    write(fn, "".join(p))


P = "serine@zion"
PR = [(P, G), (":~$ ", MUTED)]


def js(indent, key, vals, last=False):
    segs = [(" " * indent, WHITE), ('"' + key + '"', G), (": ", MUTED)]
    if isinstance(vals, list):
        segs.append(("[", MUTED))
        for i, v in enumerate(vals):
            segs.append(('"' + v + '"', WHITE))
            if i < len(vals) - 1:
                segs.append((", ", MUTED))
        segs.append(("]", MUTED))
    else:
        segs.append(('"' + vals + '"', WHITE))
    if not last:
        segs.append((",", MUTED))
    return (segs, 0.012)


def operator():
    lines = [
        (PR + [("cat operator.json", WHITE)], 0.07),
        ([("{", MUTED)], 0.02),
        js(2, "name", "Serine Zargaryan"),
        js(2, "role", ["QA Engineer", "C++ Developer"]),
        js(2, "testing", "manual + automated"),
        js(2, "base", "Los Angeles, CA"),
        js(2, "voice", ["English", "日本語", "Հայերեն"]),
        js(2, "loves", ["my pets", "PlayStation", "Marvel"]),
        js(2, "hobbies", ["tennis", "chess", "drawing", "reading comics"], last=True),
        ([("}", MUTED)], 0.02),
        ([], 0),
        (PR, 0.07),
    ]
    term("operator.svg", "serine@zion: ~/operator", lines)


def skills():
    names = ["C++", "Python", "JavaScript", "SQL", "HTML + CSS", "Selenium", "Playwright", "Postman", "Git"]
    lines = [(PR + [("./load_skills --all", WHITE)], 0.07)]
    for n in names:
        lines.append(([("  loading ", MUTED), (n.ljust(11) + " ", WHITE), ("[##########] 100%", G), ("   I know " + n + ".", G2)], 0.014))
    lines += [([], 0), (PR + [("ls tools/", WHITE)], 0.07)]
    cols = [("qa/", "manual-testing  test-automation  api-testing  performance  security-testing"),
            ("tools/", "Jira  Confluence  GitHub  VS-Code  PyCharm  WebStorm  Node.js  Snyk  Lighthouse"),
            ("", "VirtualBox  Slack  Zoom"),
            ("browsers/", "Chrome  Firefox  Edge  Safari  Opera"),
            ("platforms/", "Android  iOS  Windows  macOS")]
    for d, items in cols:
        lines.append(([(d.ljust(12), G), (items, WHITE)], 0.012))
    lines += [([], 0), (PR, 0.07)]
    term("skills.svg", "serine@zion: ~/training", lines)


def log():
    def row(name, desc, warn=False):
        tag = ("[ WARN ] ", AMBER) if warn else ("[  OK  ] ", G)
        dots = " " + "." * (16 - len(name)) + " "
        return ([tag, (name, WHITE), (dots, MUTED), (desc, AMBER if warn else G2)], 0.016)
    lines = [
        (PR + [("cat capabilities.log", WHITE)], 0.07),
        row("bug-hunter", "found a bug before the users did"),
        row("polyglot", "English, 日本語, Հայերեն"),
        row("strategist", "plans three moves ahead (chess)"),
        row("ace", "clean tennis serve"),
        row("best-friend", "cuddles the pets, every single day"),
        row("edge-case", "orders -1 beers and one lizard"),
        row("coffee", "level == 0", warn=True),
        ([], 0),
        ([("6 services running, ", WHITE), ("1 warning", AMBER), (", 0 failed", WHITE)], 0.02),
        ([], 0),
        (PR, 0.07),
    ]
    term("log.svg", "serine@zion: ~/capabilities", lines)


def mini(fn, repo, desc, tag):
    lines = [
        ([("$ ", G), ("git clone SerineGit/" + repo, WHITE)], 0.045),
        ([("Cloning... done.", MUTED)], 0.012),
    ]
    for i, d in enumerate(desc):
        lines.append(([(("> " if i == 0 else "  ") + d, G2)], 0.018))
    lines.append(([("[ exit 0 ]  ", G), (tag, WHITE)], 0.03))
    lines.append(([("$ ", G)], 0.05))
    term(fn, "program://" + repo, lines, W=540, fs=13, cw=7.8, lh=24, x0=24, bar=34, top=64, title_fs=12, tail=22, r=10, hold=7.0)


def minis():
    mini("card-1.svg", "cpp-snake-game", ["Classic 2D Snake game built with", "C++ and Windows Forms."], "C++")
    mini("card-2.svg", "Apple-and-X-AI-testing-project", ["Front-end, API, performance and security", "testing, cloud automation, QA docs."], "QA  /  HTML")
    mini("card-3.svg", "Blue-Origin-and-X-AI-testing-project", ["The full QA cycle again, now with", "Playwright and cloud automation."], "QA  /  Playwright")
    mini("card-4.svg", "Demo-Menu", ["A demo menu page: layout and", "interaction in plain JavaScript."], "JavaScript")


def strip(fn, label):
    W, H = 1100, 120
    p = [open_svg(W, H, f'<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".28" stop-color="{BG}" stop-opacity="0"/><stop offset=".72" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
                  '<clipPath id="sc"><rect width="1100" height="120" rx="10"/></clipPath>')]
    p.append(f"<title>{esc(label)}</title>")
    p.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/><g clip-path="url(#sc)">')
    p.append(rain(8, W - 8, H, 18, 9, 3, 7))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#tb)"/></g>')
    p.append("</svg>")
    write(fn, "".join(p))



# ======================================================================= v3: varied matrix panels
def brackets(x, y, w, h, l=16, color=G, op=".8"):
    return (f'<path d="M{x} {y+l} V{y} H{x+l} M{x+w-l} {y} H{x+w} V{y+l} M{x+w} {y+h-l} V{y+h} H{x+w-l} M{x+l} {y+h} H{x} V{y+h-l}" '
            f'fill="none" stroke="{color}" stroke-width="2" opacity="{op}"/>')


def subject():
    W, H, T = 1100, 340, 9.0
    p = [open_svg(W, H, f'<clipPath id="sp"><rect width="{W}" height="{H}" rx="10"/></clipPath>'
                  f'<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".85" stop-color="{G}" stop-opacity=".22"/><stop offset="1" stop-color="{G}" stop-opacity=".6"/></linearGradient>')]
    p.append("<title>Subject file: Serine Zargaryan</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{GD}"/><g clip-path="url(#sp)">')
    for gx in range(0, W, 40):
        p.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#08210f" stroke-width="1"/>')
    for gy in range(0, H, 40):
        p.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="#08210f" stroke-width="1"/>')
    p.append(f'<text x="30" y="38" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{MUTED}">SUBJECT FILE  //  SERINEGIT</text>')
    p.append(f'<line x1="30" y1="52" x2="{W-30}" y2="52" stroke="{LINE}"/>')
    # globe
    cx, cy, R = 150, 196, 98
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#041a0a" stroke="{G}" stroke-opacity=".55" stroke-width="1.5"/>')
    for dy in (-62, -30, 0, 30, 62):
        hw = math.sqrt(R * R - dy * dy)
        p.append(f'<line x1="{cx-hw:.0f}" y1="{cy+dy}" x2="{cx+hw:.0f}" y2="{cy+dy}" stroke="{G}" stroke-opacity=".25"/>')
    for k, ph in enumerate((0, 45, 90, 135)):
        rx0 = R * abs(math.cos(math.radians(ph)))
        vals = ";".join(f"{R*abs(math.cos(math.radians(ph+i*15))):.1f}" for i in range(25))
        an = "" if STATIC else f'<animate attributeName="rx" values="{vals}" dur="12s" repeatCount="indefinite"/>'
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx0:.1f}" ry="{R}" fill="none" stroke="{G}" stroke-opacity=".4">{an}</ellipse>')
    px, py = cx - 42, cy - 22
    p.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{WHITE}" filter="url(#glow)"/>')
    p.append(f'<circle cx="{px}" cy="{py}" r="6" fill="none" stroke="{G}" stroke-width="2">' + ("" if STATIC else '<animate attributeName="r" values="5;24" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/>') + "</circle>")
    p.append(f'<text x="{cx}" y="{cy+R+26}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{G2}">LOS ANGELES, CA</text>')
    # fields
    def field(x, y, k, v, c=WHITE, big=False):
        p.append(f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">{k}</text>')
        p.append(f'<text x="{x}" y="{y+26}" font-family="{MONO}" font-size="{22 if big else 17}" font-weight="800" fill="{c}"{" filter=\"url(#glow)\"" if big else ""}>{esc(v)}</text>')
    field(330, 100, "SUBJECT", "SERINE ZARGARYAN", G, True)
    if not STATIC:
        for off, col in ((-2, RED), (2, BLUE)):
            p.append(f'<text x="{330+off}" y="126" font-family="{MONO}" font-size="22" font-weight="800" fill="{col}" opacity="0">{flash([2.4, 6.6], T)}SERINE ZARGARYAN</text>')
    field(330, 170, "CLASS", "QA ENGINEER  /  C++ DEVELOPER")
    field(330, 240, "VOICE", "ENGLISH  /  日本語  /  Հայերեն")
    field(700, 170, "TESTING", "MANUAL + AUTOMATED")
    field(700, 240, "COMPANIONS", "MY PETS", G2)
    p.append(f'<text x="330" y="304" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">OFF DUTY</text>')
    p.append(f'<text x="420" y="304" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{G2}">TENNIS / CHESS / DRAWING / COMICS / PLAYSTATION / MARVEL</text>')
    # right status + binary
    p.append(f'<text x="{W-30}" y="38" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{G}">SIGNAL TRACED</text>')
    p.append(f'<circle cx="{W-176}" cy="34" r="4" fill="{G}">' + ("" if STATIC else '<animate attributeName="opacity" values="1;0" keyTimes="0;.5" dur="1s" calcMode="discrete" repeatCount="indefinite"/>') + "</circle>")
    for i in range(11):
        bits = "".join(random.choice("01") for _ in range(7))
        p.append(f'<text x="{W-30}" y="{84+i*22}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{G}" fill-opacity=".35">{bits}</text>')
    hl = f'<rect x="{W-122}" y="68" width="94" height="20" fill="{G}" opacity=".18">' + ("" if STATIC else f'<animate attributeName="y" values="68;288;68" dur="{T}s" repeatCount="indefinite"/>') + "</rect>"
    p.append(hl)
    # scan band
    if not STATIC:
        p.append(f'<rect x="0" y="-60" width="{W}" height="60" fill="url(#band)"><animate attributeName="y" from="-60" to="{H}" dur="5s" repeatCount="indefinite"/></rect>')
    p.append("</g>")
    p.append(brackets(8, 8, W - 16, H - 16))
    p.append("</svg>")
    write("subject.svg", "".join(p))


def monitors():
    W = 1100
    names = ["C++", "Python", "JavaScript", "SQL", "HTML + CSS", "Selenium", "Playwright", "Postman", "Git", "Jira", "Node.js", "Lighthouse"]
    cols, gap, tw, th = 4, 12, 263, 128
    top = 56
    H = top + 3 * (th + gap) + 58
    defs = "".join(f'<clipPath id="mt{i}"><rect x="0" y="0" width="{tw}" height="{th}" rx="6"/></clipPath>' for i in range(12))
    p = [open_svg(W, H, defs)]
    p.append("<title>Operator console: skills online</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{GD}"/>')
    p.append(f'<text x="30" y="36" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{MUTED}">OPERATOR CONSOLE  //  SKILLS ONLINE</text>')
    p.append(f'<text x="{W-30}" y="36" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{G}">12 / 12</text>')
    for i, nm in enumerate(names):
        c, r = i % cols, i // cols
        x = 6 + c * (tw + gap) + 0
        x = 12 + c * (tw + gap)
        y = top + r * (th + gap)
        p.append(f'<g transform="translate({x} {y})"><g clip-path="url(#mt{i})"><rect width="{tw}" height="{th}" fill="#020d06"/>')
        p.append(rain(6, tw - 6, th, 16, 7, 3, 7, .75))
        p.append(f'<rect x="0" y="{th/2-30}" width="{tw}" height="60" fill="{BG}" opacity=".72"/><rect x="0" y="0" width="{tw}" height="28" fill="{BG}" opacity=".88"/></g>')
        p.append(f'<rect x=".5" y=".5" width="{tw-1}" height="{th-1}" rx="6" fill="none" stroke="{GD}"/>')
        p.append(f'<text x="12" y="20" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">CAM {i+1:02d}</text>')
        p.append(f'<circle cx="{tw-62}" cy="16" r="3.5" fill="{G}">' + ("" if STATIC else f'<animate attributeName="opacity" values="1;.2;1" dur="{1.4+ (i%4)*.3:.1f}s" repeatCount="indefinite"/>') + "</circle>")
        p.append(f'<text x="{tw-12}" y="20" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{G}">ONLINE</text>')
        fs = 26 if len(nm) < 9 else 21
        p.append(f'<text x="{tw/2}" y="{th/2+9}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" font-weight="800" fill="{WHITE}" filter="url(#glow)">{esc(nm)}</text>')
        p.append(f'<text x="{tw/2}" y="{th/2+30}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{G2}">I know {esc(nm)}.</text>')
        p.append(brackets(0, 0, tw, th, 10, G, ".55"))
        p.append("</g>")
    also1 = "ALSO ONLINE:  Confluence  /  GitHub  /  VS Code  /  PyCharm  /  WebStorm  /  Snyk  /  VirtualBox  /  Slack  /  Zoom"
    also2 = "ENVIRONMENTS:  Chrome  /  Firefox  /  Edge  /  Safari  /  Opera  /  Android  /  iOS  /  Windows  /  macOS"
    p.append(f'<text x="30" y="{H-34}" font-family="{MONO}" font-size="12" fill="{G2}" fill-opacity=".85">{esc(also1)}</text>')
    p.append(f'<text x="30" y="{H-14}" font-family="{MONO}" font-size="12" fill="{MUTED}">{esc(also2)}</text>')
    p.append("</svg>")
    write("monitors.svg", "".join(p))


def messages():
    W, T = 1100, 16.0
    lines = [("FOUND A BUG BEFORE THE USERS DID.", WHITE), ("SPEAKS ENGLISH, 日本語, Հայերեն.", G), ("THINKS THREE MOVES AHEAD.", WHITE),
             ("ONE CLEAN TENNIS SERVE.", G), ("CUDDLES THE PETS. EVERY SINGLE DAY.", WHITE), ("ORDERED -1 BEERS AND ONE LIZARD.", G), ("COFFEE LEVEL: 0", AMBER)]
    step, top = 58, 112
    H = top + len(lines) * step + 20
    p = [open_svg(W, H, f'<clipPath id="mp"><rect width="{W}" height="{H}" rx="10"/></clipPath>')]
    p.append("<title>System messages</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{GD}"/><g clip-path="url(#mp)">')
    p.append(rain(10, 150, H, 20, 10, 5, 10, .55))
    p.append(rain(W - 150, W - 10, H, 20, 10, 5, 10, .55))
    p.append(f'<text x="{W/2}" y="46" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="6" fill="{MUTED}">INCOMING TRANSMISSION</text>')
    p.append(f'<text x="{W/2}" y="76" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{G}">WAKE UP. THE SYSTEM HAS SOMETHING TO SAY.</text>')
    p.append(f'<line x1="260" y1="92" x2="{W-260}" y2="92" stroke="{GD}"/>')
    for i, (t, c) in enumerate(lines):
        y = top + i * step + 24
        p.append(f'<text x="200" y="{y}" font-family="{MONO}" font-size="13" fill="{MUTED}">{i+1:02d}</text>')
        fs = 27
        p.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" font-weight="800" fill="{c}" filter="url(#glow)">{esc(t)}</text>')
        if not STATIC:
            ft = 1.5 + i * 2.1
            for off, col in ((-3, RED), (3, BLUE)):
                p.append(f'<text x="{W/2+off}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" font-weight="800" fill="{col}" opacity="0">{flash([ft], T, 0.06)}{esc(t)}</text>')
    p.append("</g>")
    p.append(brackets(8, 8, W - 16, H - 16))
    p.append("</svg>")
    write("messages.svg", "".join(p))


def vcard(fn, num, repo, desc, tag):
    W, H = 540, 200
    p = [open_svg(W, H, f'<clipPath id="vc"><rect width="{W}" height="{H}" rx="10"/></clipPath>'
                  f'<linearGradient id="vb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".8" stop-color="{G}" stop-opacity=".2"/><stop offset="1" stop-color="{G}" stop-opacity=".55"/></linearGradient>'
                  f'<linearGradient id="vl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG}" stop-opacity=".95"/><stop offset=".65" stop-color="{BG}" stop-opacity=".7"/><stop offset="1" stop-color="{BG}" stop-opacity=".3"/></linearGradient>')]
    p.append(f"<title>{esc(repo)}</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="#020d06" stroke="{GD}"/><g clip-path="url(#vc)">')
    p.append(rain(8, W - 8, H, 20, 8, 4, 9, .6))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vl)"/>')
    if not STATIC:
        p.append(f'<rect x="0" y="-50" width="{W}" height="50" fill="url(#vb)"><animate attributeName="y" from="-50" to="{H}" dur="3.6s" repeatCount="indefinite"/></rect>')
    p.append("</g>")
    p.append(f'<text x="28" y="38" font-family="{MONO}" font-size="11" letter-spacing="4" fill="{MUTED}">TARGET {num}</text>')
    p.append(f'<circle cx="{W-86}" cy="34" r="3.5" fill="{G}">' + ("" if STATIC else '<animate attributeName="opacity" values="1;0" keyTimes="0;.5" dur="1s" calcMode="discrete" repeatCount="indefinite"/>') + "</circle>")
    p.append(f'<text x="{W-28}" y="38" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{G}">LOCKED</text>')
    fs = 26 if len(repo) < 16 else (20 if len(repo) < 24 else 17)
    p.append(f'<text x="28" y="84" font-family="{MONO}" font-size="{fs}" font-weight="800" fill="{G}" filter="url(#glow)">{esc(repo)}</text>')
    for i, l in enumerate(desc):
        p.append(f'<text x="28" y="{113+i*21}" font-family="{SANS}" font-size="14.5" fill="{WHITE}" fill-opacity=".85">{esc(l)}</text>')
    tw = len(tag) * 8 + 24
    p.append(f'<rect x="28" y="{H-42}" width="{tw}" height="24" rx="3" fill="none" stroke="{G}" stroke-opacity=".7"/>')
    p.append(f'<text x="{28+tw/2}" y="{H-25}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{G2}">{esc(tag)}</text>')
    p.append(f'<text x="{W-28}" y="{H-25}" text-anchor="end" font-family="{MONO}" font-size="13" font-weight="800" letter-spacing="2" fill="{G}">OPEN  &gt;&gt;</text>')
    p.append(brackets(8, 8, W - 16, H - 16, 14))
    p.append("</svg>")
    write(fn, "".join(p))


def vcards():
    vcard("card-1.svg", "01", "cpp-snake-game", ["Classic 2D Snake game built with", "C++ and Windows Forms."], "C++")
    vcard("card-2.svg", "02", "Apple-and-X-AI-testing", ["Front-end, API, performance and security", "testing, cloud automation, QA docs."], "QA / HTML")
    vcard("card-3.svg", "03", "Blue-Origin-and-X-AI-testing", ["The full QA cycle again, now with", "Playwright and cloud automation."], "QA / Playwright")
    vcard("card-4.svg", "04", "Demo-Menu", ["A demo menu page: layout and", "interaction in plain JavaScript."], "JavaScript")



def bullet():
    W, H = 1100, 170
    p = [open_svg(W, H, f'<clipPath id="bp"><rect width="{W}" height="{H}" rx="10"/></clipPath>'
                  f'<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset="1" stop-color="{WHITE}" stop-opacity=".9"/></linearGradient>')]
    p.append("<title>Bullet time</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{GD}"/><g clip-path="url(#bp)">')
    for gy in range(24, H, 24):
        p.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="#08210f"/>')
    specs = [(34, 7.5, 0), (62, 9.5, -2.2), (92, 8.2, -4.5), (120, 10.5, -1.0), (148, 8.8, -6.0), (48, 11.0, -7.5)]
    for i, (y, d, off) in enumerate(specs):
        x_static = 150 + i * 150
        grp = f'<g transform="translate({x_static} {y})">'
        grp += f'<rect x="-120" y="-1.6" width="120" height="3.2" fill="url(#trail)"/>'
        grp += f'<ellipse cx="0" cy="0" rx="10" ry="3.6" fill="{WHITE}" filter="url(#glow)"/>'
        for j in range(2):
            if STATIC:
                grp += f'<ellipse cx="{-30-j*26}" cy="0" rx="6" ry="{12+j*6}" fill="none" stroke="{G}" stroke-opacity=".5"/>'
            else:
                grp += (f'<ellipse cx="-14" cy="0" rx="3" ry="6" fill="none" stroke="{G}" stroke-width="1.5" opacity="0">'
                        f'<animate attributeName="rx" values="3;12" dur="1.8s" begin="{j*0.9}s" repeatCount="indefinite"/>'
                        f'<animate attributeName="ry" values="6;30" dur="1.8s" begin="{j*0.9}s" repeatCount="indefinite"/>'
                        f'<animate attributeName="cx" values="-10;-70" dur="1.8s" begin="{j*0.9}s" repeatCount="indefinite"/>'
                        f'<animate attributeName="opacity" values="0.9;0" dur="1.8s" begin="{j*0.9}s" repeatCount="indefinite"/></ellipse>')
        if not STATIC:
            grp += f'<animateTransform attributeName="transform" type="translate" values="-140 {y};{W+60} {y}" dur="{d}s" begin="{off}s" repeatCount="indefinite"/>'
        grp += "</g>"
        p.append(grp)
    p.append(f'<rect x="250" y="52" width="{W-500}" height="68" rx="6" fill="{BG}" opacity=".82"/>')
    p.append(f'<text x="{W/2}" y="86" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="800" letter-spacing="3" fill="{WHITE}" filter="url(#glow)">BULLET TIME</text>')
    p.append(f'<text x="{W/2}" y="110" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{G2}">EDGE CASES, DODGED IN SLOW MOTION</text>')
    p.append(f'<text x="30" y="34" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">SPEED  x0.001</text>')
    p.append(f'<text x="{W-30}" y="34" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">BUGS DODGED: ALL</text>')
    p.append("</g>")
    p.append("</svg>")
    write("bullet.svg", "".join(p))


def cat(scale=1.35, legs=True):
    s = f'<g transform="scale({scale})" stroke="{G}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" fill="#021a0a">'
    s += '<path d="M-36 -4 C-62 -8 -66 -34 -50 -42" fill="none" stroke-width="6"/>'
    for lx, ph in ((-24, 0), (-14, 1), (24, 1), (34, 0)):
        a = "" if STATIC else f'<animate attributeName="x2" values="{lx-7};{lx+7};{lx-7}" dur="0.7s" begin="{ph*0.35}s" repeatCount="indefinite"/>'
        s += f'<line x1="{lx}" y1="8" x2="{lx}" y2="26" stroke-width="5">{a}</line>'
    s += '<ellipse cx="0" cy="-2" rx="38" ry="15"/>'
    s += '<circle cx="46" cy="-14" r="13"/>'
    s += '<polygon points="37,-22 41,-38 48,-25"/><polygon points="47,-25 55,-37 58,-20"/>'
    s += f'<circle cx="51" cy="-15" r="2.2" fill="{WHITE}" stroke="none" filter="url(#glow)"/>'
    return s + "</g>"


def dejavu():
    W, H, T = 1100, 200, 16.0
    gy = 150
    p = [open_svg(W, H, f'<clipPath id="dp"><rect width="{W}" height="{H}" rx="10"/></clipPath>')]
    p.append("<title>Deja vu: a black cat walks by twice</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{GD}"/><g clip-path="url(#dp)">')
    p.append(rain(10, W - 10, H, 24, 6, 6, 12, .35))
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}" opacity=".4"/>')
    p.append(f'<line x1="0" y1="{gy+34}" x2="{W}" y2="{gy+34}" stroke="{GD}" stroke-width="2"/>')
    def walker(start, end, static_x):
        if STATIC:
            return f'<g transform="translate({static_x} {gy})">{cat()}</g>'
        return (f'<g transform="translate(-150 {gy})">{cat()}'
                f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" calcMode="linear" '
                f'keyTimes="0;{start/T:.4f};{end/T:.4f};1" values="-150 {gy};-150 {gy};1250 {gy};1250 {gy}"/></g>')
    p.append(walker(0.5, 7.0, 260))
    p.append(walker(8.0, 14.5, 640))
    p.append(f'<text x="{W/2}" y="52" text-anchor="middle" font-family="{MONO}" font-size="26" font-weight="800" letter-spacing="2" fill="{G}" filter="url(#glow)">DEJA VU.  A BLACK CAT WALKED BY TWICE.</text>')
    if not STATIC:
        for off, col in ((-3, RED), (3, BLUE)):
            p.append(f'<text x="{W/2+off}" y="52" text-anchor="middle" font-family="{MONO}" font-size="26" font-weight="800" letter-spacing="2" fill="{col}" opacity="0">{flash([8.0, 8.4], T, 0.06)}DEJA VU.  A BLACK CAT WALKED BY TWICE.</text>')
    p.append(f'<text x="{W/2}" y="82" text-anchor="middle" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{G2}" fill-opacity=".85">IN THE MATRIX IT MEANS THEY CHANGED SOMETHING. IN QA IT MEANS YOU FOUND A BUG.</text>')
    p.append("</g>")
    p.append("</svg>")
    write("dejavu.svg", "".join(p))


def rabbit():
    W, H = 1100, 210
    p = [open_svg(W, H, f'<clipPath id="rp"><rect width="{W}" height="{H}" rx="10"/></clipPath>')]
    p.append("<title>Knock, knock, Serine. Follow the white rabbit.</title>")
    p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{GD}"/><g clip-path="url(#rp)">')
    p.append(rain(10, 190, H, 22, 8, 5, 10, .5))
    p.append(rain(W - 150, W - 10, H, 22, 8, 5, 10, .5))
    hop = "" if STATIC else '<animateTransform attributeName="transform" type="translate" values="0 0;0 -14;0 0" keyTimes="0;.45;1" dur="1.3s" repeatCount="indefinite" calcMode="spline" keySplines=".3 .7 .5 1;.5 0 .7 .3"/>'
    ear = lambda rot, d: ('<g transform="rotate(' + str(rot) + ' 36 -26)">' + ('' if STATIC else f'<animateTransform attributeName="transform" type="rotate" values="{rot} 36 -26;{rot+9} 36 -26;{rot} 36 -26" dur="1.3s" begin="{d}s" repeatCount="indefinite"/>')
                          + f'<ellipse cx="36" cy="-50" rx="5.5" ry="24" fill="{WHITE}"/><ellipse cx="36" cy="-50" rx="2.4" ry="18" fill="{G2}" opacity=".5"/></g>')
    p.append(f'<g transform="translate(150 150)" filter="url(#glow)"><g>{hop}'
             f'<ellipse cx="0" cy="0" rx="34" ry="24" fill="{WHITE}"/><circle cx="-36" cy="4" r="9" fill="{WHITE}"/>'
             f'<circle cx="34" cy="-22" r="16" fill="{WHITE}"/>{ear(-10, 0)}{ear(14, 0.2)}'
             f'<circle cx="41" cy="-25" r="2.4" fill="#021a0a"/><ellipse cx="-10" cy="22" rx="16" ry="7" fill="{WHITE}"/><ellipse cx="22" cy="22" rx="12" ry="6" fill="{WHITE}"/></g></g>')
    p.append(f'<text x="290" y="96" font-family="{MONO}" font-size="42" font-weight="800" fill="{G}" filter="url(#glow)">Knock, knock, Serine.</text>')
    cur = '<animate attributeName="opacity" values="1;0" keyTimes="0;.5" dur="1s" calcMode="discrete" repeatCount="indefinite"/>' if not STATIC else ""
    p.append(f'<rect x="{290 + 21 * 25.2 + 8:.0f}" y="64" width="22" height="40" fill="{G}">{cur}</rect>')
    p.append(f'<text x="292" y="136" font-family="{MONO}" font-size="16" letter-spacing="5" fill="{WHITE}">FOLLOW THE WHITE RABBIT.</text>')
    p.append(f'<text x="292" y="162" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">(OR JUST SCROLL DOWN AND PICK A PILL)</text>')
    p.append("</g>")
    p.append(brackets(8, 8, W - 16, H - 16))
    p.append("</svg>")
    write("rabbit.svg", "".join(p))


pills()
for fn in (header, terminal, subject, monitors, bullet, messages, dejavu, vcards, rabbit, footer):
    fn()
strip("rain-1.svg", "rain")
print("built ->", OUT, "static" if STATIC else "animated")
