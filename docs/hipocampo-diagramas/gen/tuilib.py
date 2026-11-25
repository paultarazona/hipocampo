"""Renderiza mockups de TUI como SVG: rejilla de celdas monoespaciadas + marcos y barras vectoriales."""
import html, os

MONO = "'JetBrains Mono','Cascadia Mono','DejaVu Sans Mono',Consolas,'Liberation Mono',monospace"
SANS = "Inter,'Segoe UI','Helvetica Neue',Arial,sans-serif"

T = dict(
    bg="#0f1218", panel="#141821", border="#343b4a", title="#c9c6bd",
    fg="#d9d6ce", dim="#8b8880", faint="#5c5f68", sel="#262c42",
    accent="#9085e9", epi="#5a9cf0", sem="#2fc48d", proc="#f08a5d", pros="#e77ca3",
    red="#ef6b6b", yellow="#e5b23a", green="#46c25a", cyan="#4fc3d9",
)


def esc(s):
    return html.escape(s, quote=False)


class Screen:
    def __init__(self, cols, rows, cw=8.4, ch=19, fs=14):
        self.cols, self.rows, self.cw, self.ch, self.fs = cols, rows, cw, ch, fs
        self.cells = [[(" ", T["fg"], False) for _ in range(cols)] for _ in range(rows)]
        self.bgs, self.boxes, self.bars, self.edges = [], [], [], []

    def edge(self, pts, color=None, head=True, dash=False):
        """pts en coordenadas de celda; y entera = centro de esa fila."""
        self.edges.append((pts, color or T["faint"], head, dash))

    def put(self, x, y, s, fg=None, bold=False, maxw=None):
        fg = fg or T["fg"]
        if maxw is not None and len(s) > maxw:
            print(f"WARN recorte: {s!r} ({len(s)}>{maxw})")
            s = s[:maxw]
        for i, c in enumerate(s):
            if 0 <= x + i < self.cols and 0 <= y < self.rows:
                self.cells[y][x + i] = (c, fg, bold)
        return x + len(s)

    def seg(self, x, y, parts, maxw=None):
        """parts = [(texto, color, bold?)...]"""
        start = x
        for p in parts:
            t, col = p[0], p[1]
            b = p[2] if len(p) > 2 else False
            x = self.put(x, y, t, col, b)
        if maxw is not None and x - start > maxw:
            print(f"WARN segmento largo en fila {y}: {x-start}>{maxw}")
        return x

    def bg(self, x, y, w, color, h=1):
        self.bgs.append((x, y, w, h, color))

    def box(self, x, y, w, h, title=None, color=None, key=None):
        self.boxes.append((x, y, w, h, title, color or T["border"], key))

    def bar(self, x, y, w, frac, color):
        self.bars.append((x, y, w, frac, color))

    def svg_body(self, ox, oy):
        cw, ch, out = self.cw, self.ch, []
        for x, y, w, h, c in self.bgs:
            out.append(f'<rect x="{ox+x*cw:.1f}" y="{oy+y*ch:.1f}" width="{w*cw:.1f}" height="{h*ch:.1f}" '
                       f'rx="3" fill="{c}"/>')
        for x, y, w, h, title, col, key in self.boxes:
            X, Y = ox + (x + 0.5) * cw, oy + (y + 0.5) * ch
            W, H = (w - 1) * cw, (h - 1) * ch
            out.append(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{W:.1f}" height="{H:.1f}" rx="6" '
                       f'fill="none" stroke="{col}" stroke-width="1.2"/>')
            if title:
                label = f" {title} "
                tx = x + 2
                out.append(f'<rect x="{ox+tx*cw:.1f}" y="{oy+y*ch+2:.1f}" width="{len(label)*cw:.1f}" '
                           f'height="{ch-4:.1f}" fill="{T["bg"]}"/>')
                self.put(tx, y, label, T["title"], True)
                if key:
                    k = f"[{key}]"
                    kx = x + w - 2 - len(k)
                    out.append(f'<rect x="{ox+(kx-1)*cw:.1f}" y="{oy+y*ch+2:.1f}" width="{(len(k)+2)*cw:.1f}" '
                               f'height="{ch-4:.1f}" fill="{T["bg"]}"/>')
                    self.put(kx, y, k, T["faint"])
        for pts, col, head, dash in self.edges:
            mid = "e" + col.strip("#")
            out.append(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                       f'markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="{col}"/></marker></defs>')
            d = "M" + " L".join(f"{ox+x*cw:.1f} {oy+(y+0.5)*ch:.1f}" for x, y in pts)
            me = f' marker-end="url(#{mid})"' if head else ""
            da = ' stroke-dasharray="5 4"' if dash else ""
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.4" stroke-linejoin="round"{me}{da}/>')
        for x, y, w, frac, col in self.bars:
            X, Y = ox + x * cw, oy + y * ch + ch * 0.28
            out.append(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{w*cw:.1f}" height="{ch*0.44:.1f}" rx="2" '
                       f'fill="{T["border"]}" fill-opacity="0.55"/>')
            if frac > 0:
                out.append(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{max(w*cw*frac,2):.1f}" height="{ch*0.44:.1f}" '
                           f'rx="2" fill="{col}"/>')
        for r, row in enumerate(self.cells):
            c = 0
            while c < self.cols:
                ch_, fg, b = row[c]
                if ch_ == " ":
                    c += 1
                    continue
                s = c
                buf = []
                while c < self.cols and row[c][1] == fg and row[c][2] == b and not (
                        row[c][0] == " " and c + 1 < self.cols and row[c + 1][0] == " "):
                    buf.append(row[c][0])
                    c += 1
                txt = "".join(buf).rstrip()
                if not txt:
                    continue
                X = ox + s * cw
                Y = oy + r * ch + ch * 0.72
                w = ' font-weight="700"' if b else ""
                out.append(f'<text x="{X:.1f}" y="{Y:.1f}" textLength="{len(txt)*cw:.1f}" '
                           f'lengthAdjust="spacingAndGlyphs" xml:space="preserve" font-family="{MONO}" '
                           f'font-size="{self.fs}" fill="{fg}"{w}>{esc(txt)}</text>')
        return out


def window(screen, path, title, caption, subtitle):
    pad, bar = 22, 36
    W = screen.cols * screen.cw + pad * 2
    H = screen.rows * screen.ch + pad + bar + 10
    PX, PY = 40, 96
    SW, SH = W + PX * 2, H + PY + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SW:.0f} {SH:.0f}" width="{SW:.0f}" '
           f'height="{SH:.0f}" role="img" aria-label="{esc(caption)}">', f'<title>{esc(caption)}</title>',
           '<defs><filter id="sh" x="-5%" y="-5%" width="110%" height="115%"><feDropShadow dx="0" dy="10" '
           'stdDeviation="14" flood-color="#000" flood-opacity="0.22"/></filter></defs>',
           f'<rect width="{SW:.0f}" height="{SH:.0f}" fill="#fcfcfb"/>',
           f'<text x="{PX}" y="48" font-family="{SANS}" font-size="22" font-weight="700" fill="#0b0b0b">{esc(caption)}</text>',
           f'<text x="{PX}" y="74" font-family="{SANS}" font-size="13.5" fill="#52514e">{esc(subtitle)}</text>',
           f'<rect x="{PX}" y="{PY}" width="{W:.0f}" height="{H:.0f}" rx="12" fill="{T["bg"]}" filter="url(#sh)"/>',
           f'<rect x="{PX}" y="{PY}" width="{W:.0f}" height="{bar}" rx="12" fill="#1b2029"/>',
           f'<rect x="{PX}" y="{PY+bar-12}" width="{W:.0f}" height="12" fill="#1b2029"/>']
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        out.append(f'<circle cx="{PX+22+i*20}" cy="{PY+bar/2}" r="6" fill="{c}"/>')
    out.append(f'<text x="{PX+W/2:.0f}" y="{PY+bar/2+5}" font-family="{SANS}" font-size="13" fill="#9a9890" '
               f'text-anchor="middle">{esc(title)}</text>')
    out += screen.svg_body(PX + pad, PY + bar + 10)
    out.append(f'<text x="{SW-40:.0f}" y="{SH-16:.0f}" font-family="{SANS}" font-size="10.5" fill="#7a7974" '
               f'text-anchor="end">Hipocampo · mockup MVP · datos de ejemplo</text>')
    out.append("</svg>")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return path
