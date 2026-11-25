"""Mini librería para generar los diagramas SVG de Hipocampo con un estilo común."""
import html, os

OUT = os.environ.get("HIPO_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

C = dict(
    surface="#fcfcfb", panel="#f4f3f0", ink="#0b0b0b", ink2="#52514e", muted="#7a7974",
    line="#8a8984", border="#c9c8c2", grid="#e6e5e0",
    sens="#8a8984",   # registro sensorial
    work="#6250d6",   # memoria de trabajo
    epi="#2a78d6",    # episódica (hipocampo)
    sem="#1baf7a",    # semántica (neocorteza)
    proc="#eb6834",   # procedural
    pros="#e87ba4",   # prospectiva
    amy="#e34948",    # amígdala / riesgo
    good="#008300", warn="#eda100", bad="#e34948",
)

WARN = []


def esc(s):
    return html.escape(str(s), quote=True)


def tw(text, size, mono=False, weight=400):
    k = 0.61 if mono else (0.56 if weight >= 600 else 0.53)
    return len(text) * size * k


class Diagram:
    def __init__(self, name, w, h, title, subtitle=None):
        self.name, self.w, self.h = name, w, h
        self.el = []
        self.markers = {}
        self.title, self.subtitle = title, subtitle

    # ---------- primitives ----------
    def raw(self, s):
        self.el.append(s)

    def text(self, x, y, t, size=12, color=None, weight=400, anchor="start", mono=False,
             italic=False, halo=False, maxw=None):
        color = color or C["ink2"]
        if maxw and tw(t, size, mono, weight) > maxw:
            WARN.append(f"{self.name}: texto largo ({t!r}) {tw(t,size,mono,weight):.0f}>{maxw:.0f}")
        fam = MONO if mono else FONT
        extra = ' font-style="italic"' if italic else ""
        h = (f' stroke="{C["surface"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
             if halo else "")
        self.el.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{extra}{h}>{esc(t)}</text>')

    def rect(self, x, y, w, h, fill="none", stroke=None, rx=10, sw=1.5, dash=False, opacity=None):
        d = ' stroke-dasharray="6 5"' if dash else ""
        o = f' fill-opacity="{opacity}"' if opacity is not None else ""
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{o}{s}{d}/>')

    def box(self, x, y, w, h, title=None, lines=(), color=None, tint=True, rx=10,
            tsize=14, lsize=12, mono=False, dash=False, align="center", tag=None, sw=1.5,
            lh=None, title_color=None):
        stroke = color or C["border"]
        self.rect(x, y, w, h, fill=C["surface"], rx=rx)
        if color and tint:
            self.rect(x, y, w, h, fill=color, rx=rx, opacity=0.09)
        self.rect(x, y, w, h, stroke=stroke, rx=rx, sw=sw, dash=dash)
        lh = lh or round(lsize * 1.45)
        lines = list(lines)
        block = (tsize * 1.3 if title else 0) + len(lines) * lh
        if tag:
            block += 20
        cy = y + (h - block) / 2
        if align == "center":
            ax, anc = x + w / 2, "middle"
        else:
            ax, anc = x + 14, "start"
        inner = w - 24
        if tag:
            tg_w = tw(tag, 10.5, weight=600) + 16
            tx = ax - tg_w / 2 if align == "center" else ax
            col = color or C["line"]
            self.rect(tx, cy, tg_w, 17, fill=col, rx=8.5, opacity=0.16)
            self.text(tx + tg_w / 2, cy + 12.3, tag, 10.5, C["ink2"], 600, "middle")
            cy += 22
        if title:
            self.text(ax, cy + tsize, title, tsize, title_color or C["ink"], 600, anc, maxw=inner)
            cy += tsize * 1.3
        for i, ln in enumerate(lines):
            m = mono
            if isinstance(ln, tuple):
                ln, m = ln
            self.text(ax, cy + lh * (i + 1) - (lh - lsize) / 2 - 1, ln, lsize - (0.5 if m else 0),
                      C["ink2"], 400, anc, mono=m, maxw=inner)

    def marker(self, color):
        mid = "m" + color.strip("#")
        if mid not in self.markers:
            self.markers[mid] = (
                f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                f'markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{color}"/></marker>')
        return mid

    def arrow(self, pts, color=None, label=None, lpos=None, dash=False, both=False, sw=1.5,
              head=True, lanchor="middle", lsize=11.5, lcolor=None):
        color = color or C["line"]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        mid = self.marker(color)
        me = f' marker-end="url(#{mid})"' if head else ""
        ms = f' marker-start="url(#{mid})"' if both else ""
        da = ' stroke-dasharray="6 5"' if dash else ""
        self.el.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
                       f'stroke-linejoin="round"{me}{ms}{da}/>')
        if label:
            if lpos is None:
                (x1, y1), (x2, y2) = pts[0], pts[-1]
                lpos = ((x1 + x2) / 2, (y1 + y2) / 2 - 7)
            self.text(lpos[0], lpos[1], label, lsize, lcolor or C["ink2"], 500, lanchor, halo=True)

    def section(self, x, y, t):
        self.text(x, y, t.upper(), 11, C["muted"], 700, "start")

    def panel(self, x, y, w, h, label=None, color=None, dash=False):
        self.rect(x, y, w, h, fill=C["panel"], rx=14)
        if color:
            self.rect(x, y, w, h, fill=color, rx=14, opacity=0.05)
        self.rect(x, y, w, h, stroke=color or C["border"], rx=14, sw=1, dash=dash)
        if label:
            self.text(x + 18, y + 26, label.upper(), 11, C["ink2"], 700)

    def pill(self, x, y, w, h, title, color, sub=None, tsize=14):
        self.rect(x, y, w, h, fill=C["surface"], rx=h / 2)
        self.rect(x, y, w, h, fill=color, rx=h / 2, opacity=0.13)
        self.rect(x, y, w, h, stroke=color, rx=h / 2, sw=2)
        if sub:
            self.text(x + w / 2, y + h / 2 - 3, title, tsize, C["ink"], 600, "middle", maxw=w - 16)
            self.text(x + w / 2, y + h / 2 + 14, sub, 11, C["ink2"], 400, "middle", maxw=w - 16)
        else:
            self.text(x + w / 2, y + h / 2 + tsize * 0.36, title, tsize, C["ink"], 600, "middle", maxw=w - 16)

    def legend(self, x, y, items, gap=26):
        cx = x
        for label, color in items:
            self.rect(cx, y - 10, 14, 14, fill=color, rx=4, opacity=0.25)
            self.rect(cx, y - 10, 14, 14, stroke=color, rx=4, sw=1.5)
            self.text(cx + 20, y + 1.5, label, 12, C["ink2"])
            cx += 20 + tw(label, 12) + gap

    # ---------- output ----------
    def svg(self):
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img" aria-label="{esc(self.title)}">',
                f'<title>{esc(self.title)}</title>']
        if self.subtitle:
            head.append(f'<desc>{esc(self.subtitle)}</desc>')
        head.append("<defs>" + "".join(self.markers.values()) + "</defs>")
        head.append(f'<rect width="{self.w}" height="{self.h}" fill="{C["surface"]}"/>')
        t = [f'<text x="40" y="48" font-family="{FONT}" font-size="22" font-weight="700" '
             f'fill="{C["ink"]}">{esc(self.title)}</text>']
        if self.subtitle:
            t.append(f'<text x="40" y="74" font-family="{FONT}" font-size="13.5" fill="{C["ink2"]}">'
                     f'{esc(self.subtitle)}</text>')
        foot = (f'<text x="{self.w-40}" y="{self.h-18}" font-family="{FONT}" font-size="10.5" '
                f'fill="{C["muted"]}" text-anchor="end">Hipocampo · spec v1.0</text>')
        # defs must come after markers are registered, so build body first
        return "\n".join(head + t + self.el + [foot, "</svg>"])

    def save(self):
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, self.name + ".svg")
        with open(p, "w", encoding="utf-8") as f:
            f.write(self.svg())
        return p
