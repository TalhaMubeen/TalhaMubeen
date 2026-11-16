"""Generates the profile's SVG panels into assets/. Run: python tools/make_svgs.py
Every number here comes from Talha's resume or his real GitHub activity."""
import os, math

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
FONT = '"Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif'
MONO = '"Cascadia Code", "JetBrains Mono", Consolas, monospace'
BG0, BG1, INK, MUTED, LINE = "#0B0F1F", "#141A35", "#F4F5FB", "#9AA4CC", "#252C55"
PURPLE, BLUE, GREEN, AMBER, CORAL, PINK, TEAL = "#C4A7FF", "#7CC4FF", "#63D9A8", "#F5C451", "#FF8F7A", "#F59AD6", "#5AD1C8"

def defs(extra=""):
    return f"""<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
    <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#DCD3FF"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
    <linearGradient id="hot" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PURPLE}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#FFFFFF" stroke-opacity=".04"/></pattern>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
    {extra}
  </defs>"""

def frame(w, h, r=24):
    return f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#bg)"/><rect width="{w}" height="{h}" rx="{r}" fill="url(#grid)"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LINE}"/>'

def svg(w, h, body, style="", label=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  {defs()}
  <style>
    text {{ font-family: {FONT}; }}
    .mono {{ font-family: {MONO}; }}
    .up {{ opacity: 0; animation: up .7s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .pulse {{ animation: pulse 2.8s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
    .flow {{ stroke-dasharray: 5 9; animation: dash 1.8s linear infinite; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -28; }} }}
    .blink {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {style}
  </style>
  {body}
</svg>
"""

def write(name, s):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)

# ------------------------------------------------------------------ header
def header():
    W, H = 1200, 400
    nodes = [(760, 92, PURPLE, 13, "gateway"), (880, 58, BLUE, 9, "identity"), (1000, 96, GREEN, 11, "AI"), (1110, 70, AMBER, 8, "WBS"),
             (820, 196, TEAL, 10, "tenancy"), (950, 214, PINK, 12, "scheduling"), (1080, 190, CORAL, 9, "documents"),
             (880, 316, BLUE, 8, "reporting"), (1010, 322, PURPLE, 10, "conversations"), (1130, 300, GREEN, 8, "Archivia"), (770, 318, AMBER, 9, "core")]
    edges = [(0, 1), (0, 2), (2, 3), (0, 4), (4, 5), (2, 5), (5, 6), (3, 6), (5, 8), (4, 7), (8, 9), (6, 9), (10, 4), (10, 7), (7, 8)]
    e = "".join(f'<path class="flow" d="M{nodes[a][0]} {nodes[a][1]} L{nodes[b][0]} {nodes[b][1]}" stroke="{BLUE}" stroke-opacity=".45" stroke-width="1.6" style="animation-delay:-{(i*0.37)%1.8:.2f}s"/>' for i, (a, b) in enumerate(edges))
    packets = ""
    for i, (a, b) in enumerate(edges[:8]):
        x1, y1, x2, y2 = nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]
        packets += f'<circle r="3" fill="#FFFFFF"><animateMotion dur="{2.2 + (i % 4) * 0.5}s" repeatCount="indefinite" begin="-{i*0.6:.1f}s" path="M{x1} {y1} L{x2} {y2}"/></circle>'
    n = "".join(f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="{c}" opacity=".18" filter="url(#soft)"/><circle class="pulse" style="animation-delay:-{i*0.4:.1f}s" cx="{x}" cy="{y}" r="{r}" fill="{c}"/><text x="{x}" y="{y + r + 18}" text-anchor="middle" font-size="12" fill="{MUTED}" font-weight="600">{lbl}</text>' for i, (x, y, c, r, lbl) in enumerate(nodes))
    chips = [("Agentic AI systems", PURPLE), ("LLM evals", BLUE), ("Multi-tenant SaaS", GREEN), ("Rail-safety IoT", AMBER)]
    cx, ch = 64, ""
    for i, (t, c) in enumerate(chips):
        w = 26 + len(t) * 9.4
        ch += f'<g class="up" style="animation-delay:{0.55 + i*0.1:.2f}s"><rect x="{cx}" y="266" width="{w:.0f}" height="36" rx="18" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".35"/><text x="{cx + 13}" y="290" font-size="16" font-weight="700" fill="{c}">{t}</text></g>'
        cx += w + 10
    body = f"""{frame(W, H, 26)}
  <circle cx="980" cy="60" r="240" fill="{PURPLE}" opacity=".10" filter="url(#soft)"/>
  <circle cx="1100" cy="330" r="200" fill="{BLUE}" opacity=".08" filter="url(#soft)"/>
  <g>{e}{packets}{n}</g>
  <g class="up"><text x="64" y="80" class="mono" font-size="17" fill="{GREEN}">~/talha $ <tspan fill="{INK}">whoami</tspan><tspan class="blink" fill="{GREEN}">▍</tspan></text></g>
  <g class="up" style="animation-delay:.12s"><text x="60" y="168" font-size="84" font-weight="800" letter-spacing="-3" fill="url(#ink)">Talha Mubeen</text></g>
  <g class="up" style="animation-delay:.25s"><text x="64" y="218" font-size="27" font-weight="600" fill="{INK}">Lead Technical Architect <tspan fill="{MUTED}">at Attimo</tspan>  <tspan fill="{PURPLE}">/</tspan>  ex-OpenAI</text></g>
  <g class="up" style="animation-delay:.38s"><text x="64" y="248" font-size="17" fill="{MUTED}">8+ years building systems where mistakes are expensive. Now: AI that earns trust before it acts.</text></g>
  {ch}
  <text x="64" y="356" font-size="13" fill="{MUTED}" class="mono">On the right: Panovia's 11 NestJS microservices, which I designed.</text>"""
    write("header.svg", svg(W, H, body, label="Talha Mubeen, Lead Technical Architect at Attimo, ex-OpenAI"))

# ------------------------------------------------------------------ impact tiles
def impact():
    tiles = [("11", "microservices", "I designed for Panovia", PURPLE),
             ("~100", "event types", "behind its transactional outbox", BLUE),
             ("~80", "enterprise sources", "its connector framework is sized for", GREEN),
             ("κ ≥ 0.6", "human agreement", "before an AI judge is trusted", AMBER),
             ("99.6%", "detection accuracy", "OpenCV detector, harsh daylight", CORAL),
             ("10K+", "requests / minute", "on backends I led, sub-100 ms APIs", TEAL),
             ("67", "merged pull requests", "on production platforms", PINK),
             ("1", "patent in preparation", "for Panovia's AI engine", PURPLE)]
    W, H, cols = 1200, 380, 4
    tw, th, gx, gy, x0, y0 = 272, 138, 16, 16, 24, 70
    body = frame(W, H) + f'<text x="28" y="44" font-size="22" font-weight="800" fill="{INK}">Impact, measured</text><text x="1172" y="44" text-anchor="end" font-size="14" fill="{MUTED}">from shipped work, not side quests</text>'
    for i, (big, lab, sub, c) in enumerate(tiles):
        x = x0 + (i % cols) * (tw + gx); y = y0 + (i // cols) * (th + gy)
        body += f"""<g class="up" style="animation-delay:{0.08*i:.2f}s">
    <rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="18" fill="#FFFFFF" fill-opacity=".03" stroke="{c}" stroke-opacity=".28"/>
    <rect x="{x}" y="{y}" width="4" height="{th}" rx="2" fill="{c}"/>
    <text x="{x + 22}" y="{y + 58}" font-size="44" font-weight="800" letter-spacing="-1.5" fill="{c}">{big}</text>
    <text x="{x + 22}" y="{y + 88}" font-size="16" font-weight="700" fill="{INK}">{lab}</text>
    <text x="{x + 22}" y="{y + 112}" font-size="12.5" fill="{MUTED}">{sub}</text></g>"""
    write("impact.svg", svg(W, H, body, label="Impact: 11 microservices, about 100 event types, about 80 enterprise sources, AI judges at kappa 0.6 or higher, 99.6% detection accuracy, 10K+ requests per minute, 67 merged pull requests, 1 patent in preparation"))

# ------------------------------------------------------------------ Panovia architecture
def panovia():
    W, H = 1200, 560
    def box(x, y, w, h, t, sub, c, d=0):
        return f'<g class="up" style="animation-delay:{d:.2f}s"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{c}" fill-opacity=".10" stroke="{c}" stroke-opacity=".55"/><text x="{x + w/2}" y="{y + h/2 - (4 if sub else -6)}" text-anchor="middle" font-size="16" font-weight="800" fill="{INK}">{t}</text>' + (f'<text x="{x + w/2}" y="{y + h/2 + 16}" text-anchor="middle" font-size="12" fill="{MUTED}">{sub}</text>' if sub else "") + "</g>"
    b = frame(W, H)
    b += f'<text x="28" y="46" font-size="22" font-weight="800" fill="{INK}">Panovia, the platform I architected</text><text x="28" y="72" font-size="14" fill="{MUTED}">AI-native project management and execution. Every AI action stays under human approval.</text>'
    b += box(80, 104, 240, 58, "Next.js 16 web app", "React 19, TanStack Query", BLUE, 0)
    b += box(480, 104, 240, 58, "Platform admin", "Cloudflare Access + Tunnel", BLUE, .05)
    b += box(880, 104, 240, 58, "Enterprise sources", "M365, Google, WhatsApp, Notion", BLUE, .1)
    b += box(380, 206, 440, 54, "Gateway", "", PURPLE, .15)
    svcs = [("identity", PURPLE), ("tenancy", PURPLE), ("WBS", GREEN), ("scheduling", GREEN), ("AI", AMBER), ("documents", TEAL), ("conversations", TEAL), ("reporting", PINK), ("Archivia", PINK)]
    sx = 52
    for i, (n, c) in enumerate(svcs):
        b += box(sx + i * 122, 304, 110, 48, n, "", c, .2 + i * .04)
    b += box(52, 372, 1096, 40, "shared core library", "", MUTED, .6)
    b += box(52, 440, 340, 72, "PostgreSQL, row-level tenancy", "Drizzle ORM, Aurora Serverless v2", GREEN, .7)
    b += box(430, 440, 340, 72, "Transactional outbox", "~100 catalogued event types", PURPLE, .75)
    b += box(808, 440, 340, 72, "AI layer", "Claude + Voyage, router, κ-gated judges", AMBER, .8)
    flows = [(200, 162, 520, 206), (600, 162, 600, 206), (1000, 162, 700, 206)] + [(600, 260, 107 + i * 122, 304) for i in range(9)] + [(222, 412, 222, 440), (600, 412, 600, 440), (978, 412, 978, 440)]
    b += "".join(f'<path class="flow" style="animation-delay:-{(i*0.3)%1.8:.1f}s" d="M{a} {c} L{d} {e}" stroke="{BLUE}" stroke-opacity=".5" stroke-width="1.5" fill="none"/>' for i, (a, c, d, e) in enumerate(flows))
    b += f'<text x="1172" y="540" text-anchor="end" font-size="12" fill="{MUTED}">AWS ECS Fargate · Valkey · S3 · BullMQ · SCIM · KVKK / GDPR</text>'
    write("panovia.svg", svg(W, H, b, label="Panovia architecture: web app, admin and enterprise sources into a gateway, nine domain services and a shared core library, over PostgreSQL, a transactional outbox and an AI layer"))

# ------------------------------------------------------------------ career timeline
def timeline():
    W, H = 1200, 330
    y0, y1 = 2018.0, 2026.9
    X = lambda y: 60 + (y - y0) / (y1 - y0) * 1080
    jobs = [("Powersoft19", "IoT engineer: rail-safety devices, C++ / Python", 2018.2, 2021.3, AMBER, 0),
            ("OpenAI", "Fullstack AI Engineer (Python)", 2021.45, 2022.85, GREEN, 1),
            ("TPG, Inc.", "Senior Backend Developer", 2021.95, 2022.95, BLUE, 2),
            ("WNK Associates", "Senior Backend Engineer, team lead", 2022.95, 2025.55, TEAL, 0),
            ("MID-Construction", "Senior Solution Architect", 2025.45, 2026.45, PINK, 1),
            ("Attimo · Panovia", "Lead Technical Architect", 2026.0, 2026.88, PURPLE, 2)]
    b = frame(W, H) + f'<text x="28" y="46" font-size="22" font-weight="800" fill="{INK}">Where I\'ve built</text>'
    for yr in range(2018, 2027):
        x = X(yr)
        b += f'<line x1="{x}" y1="74" x2="{x}" y2="262" stroke="#FFFFFF" stroke-opacity=".05"/><text x="{x}" y="290" text-anchor="middle" font-size="13" fill="{MUTED}">{yr}</text>'
    for i, (n, r, a, z, c, lane) in enumerate(jobs):
        x, w, y = X(a), X(z) - X(a), 88 + lane * 60
        tx = x + 12; anchor = "start"
        if x + 300 > 1170:
            tx = X(z) - 12; anchor = "end"
        b += f"""<g class="up" style="animation-delay:{0.1*i:.1f}s"><rect x="{x}" y="{y}" width="{w}" height="10" rx="5" fill="{c}"/>
  <text x="{tx}" y="{y + 32}" text-anchor="{anchor}" font-size="15" font-weight="800" fill="{INK}">{n} <tspan font-weight="500" fill="{MUTED}" font-size="13">{r}</tspan></text></g>"""
    b += f'<circle class="pulse" cx="{X(2026.88)}" cy="{88 + 2*60 + 5}" r="7" fill="{PURPLE}"/><text x="1172" y="316" text-anchor="end" font-size="12" fill="{MUTED}">BS Computer Science, FAST-NUCES, 2017</text>'
    write("timeline.svg", svg(W, H, b, label="Career: Powersoft19 2018 to 2021, OpenAI 2021 to 2022, TPG 2021 to 2022, WNK Associates 2022 to 2025, MID-Construction 2025 to 2026, Attimo since 2026"))

# ------------------------------------------------------------------ project cards
def card(name, title, desc, tags, c, stat=""):
    W, H = 580, 196
    lines, cur = [], ""
    for w in desc.split():
        if len(cur) + len(w) > 62:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    t = "".join(f'<text x="28" y="{98 + i*21}" font-size="14.5" fill="{MUTED}">{l}</text>' for i, l in enumerate(lines[:3]))
    tx, tg = 28, ""
    for g in tags:
        w = 18 + len(g) * 7.6
        tg += f'<rect x="{tx}" y="152" width="{w:.0f}" height="26" rx="13" fill="{c}" fill-opacity=".12"/><text x="{tx + 9}" y="170" font-size="12.5" font-weight="700" fill="{c}">{g}</text>'
        tx += w + 8
    body = f"""{frame(W, H, 20)}<rect x="0" y="0" width="{W}" height="4" rx="2" fill="{c}"/>
  <circle cx="{W - 40}" cy="40" r="60" fill="{c}" opacity=".12" filter="url(#soft)"/>
  <g class="up"><text x="28" y="56" font-size="24" font-weight="800" letter-spacing="-.5" fill="{INK}">{title}</text>
  <text x="{W - 28}" y="54" text-anchor="end" font-size="13" font-weight="700" fill="{c}">{stat}</text>{t}{tg}</g>"""
    write(f"card-{name}.svg", svg(W, H, body, label=f"{title}: {desc}"))

def stack():
    groups = [("AI and agents", PURPLE, ["Claude API", "Claude Code", "Agent loops", "Model routing", "RAG / hybrid search", "Voyage + rerank", "LLM-as-judge"]),
              ("Platform", BLUE, ["TypeScript", "NestJS 11", "Next.js 16", "React 19", "Node.js", "Python", "Haskell", "C++ / C#"]),
              ("Data and infra", GREEN, ["PostgreSQL", "Drizzle", "Redis / Valkey", "BullMQ", "MongoDB", "AWS Fargate", "Aurora", "Cloudflare"]),
              ("Architecture", AMBER, ["Microservices", "Multi-tenant SaaS", "Event-driven", "Outbox", "OAuth / SCIM", "MQTT / ZMQ", "GraphQL", "WebSockets"])]
    W, H = 1200, 300
    b = frame(W, H) + f'<text x="28" y="46" font-size="22" font-weight="800" fill="{INK}">Stack</text>'
    for gi, (g, c, items) in enumerate(groups):
        y = 82 + gi * 52
        b += f'<g class="up" style="animation-delay:{gi*0.1:.1f}s"><text x="28" y="{y + 18}" font-size="14" font-weight="800" fill="{c}">{g}</text>'
        x = 190
        for it in items:
            w = 22 + len(it) * 7.9
            b += f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="8" fill="#FFFFFF" fill-opacity=".04" stroke="{c}" stroke-opacity=".3"/><text x="{x + 11}" y="{y + 19}" font-size="13.5" font-weight="600" fill="{INK}">{it}</text>'
            x += w + 8
        b += "</g>"
    write("stack.svg", svg(W, H, b, label="Stack: AI and agents, platform languages, data and infrastructure, architecture"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    header(); impact(); panovia(); timeline(); stack()
    card("devmanager", "Dev Manager", "The task manager for developers: every Claude Code session, MCP server and dev server on Windows, what each one costs, and what is reaching the network. Runs locally.", ["Electron", "Node.js", "PowerShell"], GREEN, "NEW · v1.0")
    card("compress", "faithful-compress", "Context compression for LLMs that keeps exact anchors verbatim by construction and only compresses background. Property-tested invariants.", ["Haskell", "LLM context", "Property tests"], PURPLE)
    card("ingestion", "Document Ingestion Platform", "Upload PDFs and text, extract metadata and full text in a Python worker, and search it through a Fastify API on PostgreSQL full-text search.", ["TypeScript", "Fastify", "Python", "PostgreSQL"], BLUE)
    card("iam", "IAM System", "Identity and access management with role-based access control, groups, modules and permissions, JWT auth and a React admin.", ["Node.js", "Express", "React", "RBAC"], AMBER)
    card("hue", "Hue bridge for ESP32", "A XIAO ESP32-C3 that appears as a light in the Philips Hue app and drives WS2812 LEDs with patterns and a physical button.", ["C++", "ESP32", "IoT"], CORAL)
    card("glm", "Gatearm Light Monitor", "Monitors railway crossing gate lights on Raspberry Pi and Windows. The OpenCV detector behind it hit 99.6% accuracy in harsh daylight.", ["Python", "OpenCV", "Raspberry Pi"], TEAL, "99.6%")
    print("ok")
