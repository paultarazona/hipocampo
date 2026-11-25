import math
from svglib import Diagram, C, tw

S1, S2, S3, S4, S5 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"


def d08():
    d = Diagram("08-trazabilidad", 1260, 1000, "Trazabilidad: de dónde sale cada recuerdo",
                "Cada recuerdo apunta a su fuente, a su commit de código y a los recuerdos de los que se derivó.")
    W, H = 190, 132
    X = [40, 285, 530, 775, 1020]
    top = [
        ("Sesión", "s_7f3a", ["harness: claude-code", "model: opus", "2026-10-28"], C["work"]),
        ("Evento", "post_tool", ["test falla tras pasar", "sorpresa 0.8", "saliencia 0.9"], C["sens"]),
        ("Episodio", "ep_01JC8X", [("session_id → s_7f3a", True), "outcome: partial", "E = 0.85"], C["epi"]),
        ("Error", "01JC8XK4M2", ["source: codex", ("anchor: a1b2c3d", True), "validated_by: human"], C["amy"]),
        ("Solución", "01JC8XM7P1", [("solves → 01JC8XK4M2", True), "success_count: 3", "source: claude-code"], C["sem"]),
    ]
    for x, (tag, title, ln, col) in zip(X, top):
        d.box(x, 120, W, H, title, ln, color=col, tag=tag, lsize=11.5, mono=False)
    labels = ["emite", "E ≥ 0.4", "contiene", "solved_by"]
    for i in range(4):
        d.arrow([(X[i] + W, 186), (X[i + 1], 186)], label=labels[i], lpos=(X[i] + W + 27.5, 176), lsize=11)

    d.box(560, 330, 240, 132, "dec_014", ["fechas siempre en UTC", ("derived_from: 3 episodios", True),
                                          "proposed → active (human)"], color=C["sem"], tag="Regla semántica", lsize=11.5)
    d.box(1020, 330, 190, 132, "proc_007", [("derived_from → 01JC8XM7P1", True),
                                             ("script: scripts/migrate.sh", True), "3+ éxitos"], color=C["proc"],
          tag="Procedimiento", lsize=11)
    d.arrow([(625, 252), (625, 290), (660, 290), (660, 330)], dash=True, label="derived_from", lpos=(700, 284),
            color=C["sem"])
    d.arrow([(870, 252), (870, 290), (740, 290), (740, 330)], dash=True, color=C["sem"])
    d.arrow([(1115, 252), (1115, 330)], dash=True, color=C["proc"], label="sueño: 3+ éxitos", lpos=(1125, 296),
            lanchor="start")

    # bandas de commits
    def band(y, name, sub, commits, col):
        d.text(40, y - 26, name, 13, C["ink"], 600)
        d.text(40 + tw(name, 13, weight=600) + 10, y - 26, sub, 12, C["ink2"])
        d.raw(f'<line x1="40" y1="{y}" x2="1220" y2="{y}" stroke="{col}" stroke-width="2"/>')
        pts = {}
        for cx, sha, lab in commits:
            d.raw(f'<circle cx="{cx}" cy="{y}" r="7" fill="{C["surface"]}" stroke="{col}" stroke-width="2.5"/>')
            d.text(cx, y + 26, sha, 11, C["ink"], 600, "middle", mono=True)
            d.text(cx, y + 43, lab, 11, C["ink2"], 400, "middle")
            pts[sha] = cx
        return pts

    code = band(560, "Repo de código", "(tu proyecto)", [(200, "7c21e0f", "migración inicial"),
                                                         (480, "a1b2c3d", "cambia schema.prisma"),
                                                         (760, "d94f1aa", "fix de migraciones"),
                                                         (1080, "HEAD", "hoy")], C["line"])
    store = band(680, "Almacén de memoria", "(git propio: hipocampo/memory)",
                 [(260, "m01", "record ep_01JC8X"), (520, "m02", "record error + solución"),
                  (800, "m03", "sleep: dec_014 proposed"), (1060, "m04", "review: dec_014 aprobada")],
                 C["epi"])
    d.arrow([(930, 252), (930, 300), (990, 300), (990, 515), (480, 515), (480, 553)], dash=True, color=C["amy"],
            label="anchor.commit", lpos=(700, 507))

    # preguntas
    d.text(40, 780, "Preguntas que la trazabilidad responde", 14, C["ink"], 600)
    qs = [("¿De dónde salió esta regla?", "derived_from → episodios → sesión"),
          ("¿Qué agente y modelo lo escribió?", "source.agent · source.model"),
          ("¿Sigue siendo cierto con el código de hoy?", "anchor.commit + hash de anchor.files vs HEAD"),
          ("¿Quién lo validó?", "source.validated_by (human o un test)"),
          ("¿Por qué ya no aparece?", "status superseded / archived · evento forgotten · commit del almacén")]
    y = 800
    for i, (q, a) in enumerate(qs):
        if i % 2 == 0:
            d.rect(40, y, 1180, 30, fill=C["panel"], rx=4)
        d.text(56, y + 20, q, 12.5, C["ink"], 500)
        d.text(480, y + 20, a, 12, C["ink2"], 400, mono=False)
        y += 32
    return d.save()


def chart_frame(d, x, y, w, h):
    d.rect(x, y, w, h, fill="none", stroke=None)


def d09():
    d = Diagram("09-activacion", 1300, 680, "Activación: por qué un recuerdo aparece o no",
                "A = B + S + 2·C + P + ln(confianza) − penalización. Valores por defecto de config.toml.")
    # --- izquierda: curva de B ---
    px, py, pw, ph = 100, 150, 500, 380
    d.text(40, 122, "Activación base B según usos y horas activas", 14, C["ink"], 600)
    ymin, ymax = -3.0, 3.5
    def X(hh): return px + (math.log10(hh) - 0) / 3 * pw
    def Y(v): return py + (ymax - v) / (ymax - ymin) * ph
    for v in [-3, -2, -1, 0, 1, 2, 3]:
        yy = Y(v)
        d.raw(f'<line x1="{px}" y1="{yy:.1f}" x2="{px+pw}" y2="{yy:.1f}" stroke="{C["grid"]}" stroke-width="1"/>')
        d.text(px - 10, yy + 4, f"{v:+d}" if v else "0", 11, C["muted"], 400, "end")
    for hh, lab in [(1, "1 h"), (10, "10 h"), (100, "100 h"), (1000, "1000 h")]:
        xx = X(hh)
        d.raw(f'<line x1="{xx:.1f}" y1="{py}" x2="{xx:.1f}" y2="{py+ph}" stroke="{C["grid"]}" stroke-width="1"/>')
        d.text(xx, py + ph + 20, lab, 11, C["muted"], 400, "middle")
    d.raw(f'<line x1="{px}" y1="{Y(0):.1f}" x2="{px+pw}" y2="{Y(0):.1f}" stroke="{C["line"]}" stroke-width="1"/>')
    d.text(px + pw / 2, py + ph + 42, "horas activas desde la creación (escala log)", 11.5, C["ink2"], 400, "middle")
    d.text(px - 40, py - 12, "B", 12, C["ink2"], 600)
    series = [(1, S1, "1 uso"), (3, S2, "3 usos"), (10, S3, "10 usos")]
    for n, col, lab in series:
        pts = []
        for i in range(0, 61):
            hh = 10 ** (i / 20)
            if hh < n:  # no puede haber más usos que horas
                continue
            b = math.log(n / 0.5) - 0.5 * math.log(hh)
            pts.append((X(hh), Y(b)))
        dd = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        d.raw(f'<path d="{dd}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')
        ex, ey = pts[-1]
        d.raw(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{col}" stroke="{C["surface"]}" stroke-width="2">'
              f'<title>{lab}: B = {math.log(n/0.5)-0.5*math.log(1000):.2f} a las 1000 h</title></circle>')
        d.text(ex + 10, ey + 4, lab, 11.5, C["ink"], 500)
    d.legend(px, 600, [(l, c) for _, c, l in series])
    d.text(px, 628, "Aproximación estándar de ACT-R con d = 0.5. Cada uso suma; el tiempo resta.", 11.5, C["muted"])

    # --- derecha: barras divergentes ---
    qx, qy, qw = 760, 170, 480
    d.text(700, 122, "Mismo recuerdo, tres contextos", 14, C["ink"], 600)
    d.text(700, 142, "error de prisma migrate dev · 4 usos · 168 h · saliencia 0.9 · confianza 0.95", 11.5, C["ink2"])
    vmin, vmax = -2.0, 2.5
    def V(v): return qx + (v - vmin) / (vmax - vmin) * qw
    rows = [("Editando prisma/schema.prisma", [-0.483, -0.051], [0.9, 1.2], 1.566),
            ("Trabajando en el frontend", [-0.483, -0.051], [0.9], 0.366),
            ("Editando prisma, recuerdo suspect", [-0.483, -0.051, -1.0], [0.9, 1.2], 0.566)]
    negc = [S1, S4, S5]
    posc = [S2, S3]
    for v in [-2, -1, 0, 1, 2]:
        xx = V(v)
        d.raw(f'<line x1="{xx:.1f}" y1="{qy}" x2="{xx:.1f}" y2="{qy+330}" stroke="{C["grid"]}" stroke-width="1"/>')
        d.text(xx, qy + 350, f"{v:+d}" if v else "0", 11, C["muted"], 400, "middle")
    for thr, lab in [(0.5, "índice L1 (0.5)"), (1.2, "se inyecta (1.2)")]:
        xx = V(thr)
        d.raw(f'<line x1="{xx:.1f}" y1="{qy-8}" x2="{xx:.1f}" y2="{qy+330}" stroke="{C["ink2"]}" '
              f'stroke-width="1.2" stroke-dasharray="5 4"/>')
        d.text(xx + (4 if thr > 1 else -4), qy - 12, lab, 11, C["ink2"], 600, "start" if thr > 1 else "end")
    by = qy + 30
    for name, negs, poss, total in rows:
        d.text(700, by - 10, name, 12, C["ink"], 500)
        bh = 26
        cur = 0
        for v, col in zip(negs, negc):
            x1, x2 = V(cur + v), V(cur)
            d.raw(f'<rect x="{x1+1:.1f}" y="{by}" width="{max(x2-x1-2,1):.1f}" height="{bh}" rx="3" fill="{col}">'
                  f'<title>{v:+.3f}</title></rect>')
            cur += v
        cur = 0
        for v, col in zip(poss, posc):
            x1, x2 = V(cur), V(cur + v)
            d.raw(f'<rect x="{x1+1:.1f}" y="{by}" width="{x2-x1-2:.1f}" height="{bh}" rx="3" fill="{col}">'
                  f'<title>{v:+.3f}</title></rect>')
            cur += v
        tx = V(total)
        d.raw(f'<path d="M{tx:.1f} {by-6} L{tx+7:.1f} {by+bh/2} L{tx:.1f} {by+bh+6} L{tx-7:.1f} {by+bh/2} Z" '
              f'fill="{C["ink"]}" stroke="{C["surface"]}" stroke-width="2"><title>A = {total}</title></path>')
        verdict = "se inyecta" if total >= 1.2 else ("solo índice L1" if total >= 0.5 else "no aparece")
        d.text(V(vmax) + 0, by + bh + 22, f"A = {total:.3f} · {verdict}", 12, C["ink"], 600, "end", halo=True)
        by += 105
    d.legend(700, 600, [("B base", S1), ("saliencia", S2), ("contexto 2·C", S3), ("ln(conf)", S4),
                        ("penalización", S5)], gap=18)
    d.text(700, 628, "Rombo = A total. Barras a la derecha suman, a la izquierda restan.", 11.5, C["muted"])
    return d.save()


def d10():
    d = Diagram("10-fatiga-de-sesion", 1300, 660, "Fatiga de sesión y handoff",
                "Hipocampo corta la sesión antes de que el agente se degrade y arranca otra limpia desde la semilla.")
    px, py, pw, ph = 110, 130, 1110, 360
    T = 170
    def X(t): return px + t / T * pw
    def Y(f): return py + (1 - f) * ph
    bands = [(0.5, 0.7, C["warn"], "cansado"), (0.7, 0.85, C["proc"], "agotado"), (0.85, 1.0, C["bad"], "debe dormir")]
    d.text(px + 6, Y(0.5) + 18, "despierto", 11, C["ink2"], 600)
    for lo, hi, col, lab in bands:
        op = {0.5: 0.12, 0.7: 0.16, 0.85: 0.20}[lo]
        d.rect(px, Y(hi), pw, Y(lo) - Y(hi), fill=col, rx=0, opacity=op)
        d.text(px + 6, Y(hi) + 15, lab, 11, C["ink2"], 600)
    for f in [0, 0.25, 0.5, 0.7, 0.85, 1.0]:
        yy = Y(f)
        d.raw(f'<line x1="{px}" y1="{yy:.1f}" x2="{px+pw}" y2="{yy:.1f}" stroke="{C["grid"]}" stroke-width="1"/>')
        d.text(px - 10, yy + 4, f"{f:g}", 11, C["muted"], 400, "end")
    d.text(px - 60, py - 14, "F", 12, C["ink2"], 600)

    def F1(t):
        u = min(1, t / 120 * 0.95)
        k = (1 if t >= 70 else 0) + (1 if t >= 104 else 0)
        loop = 1 if 92 <= t else 0
        r = min(1, t / 160) * 0.6
        e = 0.75 if t >= 110 else (0.25 if 60 <= t < 66 else 0)
        return min(1, 0.45 * u + 0.15 * k / 2 + 0.15 * loop + 0.10 * r + 0.15 * e)
    pts, cross, tend = [], {}, None
    for t10 in range(0, 1201):
        t = t10 / 10
        f = F1(t)
        pts.append((t, f))
        for thr in (0.5, 0.7, 0.85):
            if thr not in cross and f >= thr:
                cross[thr] = t
        if f >= 0.85:
            tend = t
            break
    s2 = []
    t0 = tend + 8
    for t10 in range(int(t0 * 10), T * 10 + 1):
        t = t10 / 10
        s2.append((t, 0.05 + 0.45 * min(1, (t - t0) / 120 * 0.95) + 0.01 * ((t - t0) / 10)))

    def path(p):
        return "M" + " L".join(f"{X(a):.1f} {Y(b):.1f}" for a, b in p)
    d.raw(f'<path d="{path(pts)}" fill="none" stroke="{S1}" stroke-width="2" stroke-linejoin="round"/>')
    d.raw(f'<path d="{path(s2)}" fill="none" stroke="{S3}" stroke-width="2" stroke-linejoin="round"/>')

    acts = [(0.5, "checkpoint automático"), (0.7, "siesta: handoff escrito"), (0.85, "handoff forzado")]
    for i, (thr, lab) in enumerate(acts):
        t = cross[thr]
        cx, cy = X(t), Y(thr)
        d.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="{S1}" stroke="{C["surface"]}" stroke-width="2">'
              f'<title>{lab} · paso {t:.0f}</title></circle>')
        lx = cx - 14
        d.text(lx, cy - 12 - (0 if i != 1 else 0), lab, 12, C["ink"], 600, "end", halo=True)
    # eventos
    for t, lab in [(70, "compactación"), (104, "compactación"), (92, "bucle")]:
        xx = X(t)
        d.raw(f'<line x1="{xx:.1f}" y1="{py+ph}" x2="{xx:.1f}" y2="{py+ph+8}" stroke="{C["ink2"]}" stroke-width="1.5"/>')
    d.text(X(70), py + ph + 24, "compactación", 11, C["ink2"], 400, "middle")
    d.text(X(92), py + ph + 40, "bucle", 11, C["ink2"], 400, "middle")
    d.text(X(104) + 4, py + ph + 24, "compactación", 11, C["ink2"], 400, "start")
    # semilla
    xs = X(tend + 4)
    d.raw(f'<line x1="{xs:.1f}" y1="{py}" x2="{xs:.1f}" y2="{py+ph}" stroke="{C["ink2"]}" stroke-width="1.2" '
          f'stroke-dasharray="5 4"/>')
    d.text(xs + 8, py + 16, "wake_seed.md (≤ 1,000 tokens)", 12, C["ink"], 600, halo=True)
    d.text(xs + 8, py + 33, "la sesión nueva arranca limpia", 11.5, C["ink2"], halo=True)
    d.text(px + pw / 2, py + ph + 62, "pasos de la sesión (ilustrativo)", 11.5, C["ink2"], 400, "middle")
    d.legend(px, 588, [("sesión 1 (Claude Code)", S1), ("sesión 2 (Codex u otro agente)", S3)])
    d.text(px, 616, "F = 0.45·llenado + 0.15·compactaciones + 0.15·bucles + 0.10·relecturas + 0.15·errores",
           12, C["ink2"], mono=True)
    return d.save()


def d11():
    d = Diagram("11-coordinacion-multiagente", 1300, 880, "Dos agentes en el mismo flujo de tareas",
                "No se hablan entre sí: reclaman, avisan y entregan a través de la pizarra.")
    xs = {"A": 200, "P": 650, "B": 1100}
    heads = [("A", "Agente A", "Claude Code · worktree hipo/T-12", None),
             ("P", "Pizarra (Hipocampo)", "tareas · leases · events.jsonl", C["work"]),
             ("B", "Agente B", "Codex · worktree hipo/T-13", None)]
    for k, n, s, c in heads:
        x = xs[k]
        d.box(x - 140, 100, 280, 56, n, [s], color=c, lsize=11.5)
        d.raw(f'<line x1="{x}" y1="156" x2="{x}" y2="800" stroke="{C["border"]}" stroke-width="1.5" '
              f'stroke-dasharray="4 5"/>')
    msgs = [
        ("A", "P", 196, "task claim T-12 · scope src/api/**", False, None),
        ("P", "A", 236, "lease concedido · 30 min", True, C["good"]),
        ("B", "P", 288, "task claim T-12", False, None),
        ("P", "B", 328, "rechazado: T-12 ya tiene dueño", True, C["bad"]),
        ("B", "P", 380, "task claim T-13 · scope web/**", False, None),
        ("P", "B", 420, "lease concedido · 30 min", True, C["good"]),
        ("A", "P", 474, "checkpoint · renueva el lease", False, None),
        ("A", "P", 526, "decision: cambia el contrato de api/users", False, None),
        ("P", "B", 578, "pre_tool inyecta: «A cambió api/users»", True, C["work"]),
        ("A", "P", 632, "task done T-12", False, None),
        ("B", "P", 684, "task done T-13", False, None),
        ("A", "P", 770, "task claim T-14 · integración", False, None),
    ]
    for a, b, y, t, back, col in msgs:
        x1, x2 = xs[a], xs[b]
        off = 8 if x2 > x1 else -8
        d.arrow([(x1 + off, y), (x2 - off, y)], dash=back, color=col or C["line"])
        d.text((x1 + x2) / 2, y - 8, t, 12, C["ink2"], 500, "middle", halo=True)
    # self de la pizarra
    y = 712
    d.arrow([(658, y), (710, y), (710, y + 24), (660, y + 24)], color=C["work"])
    d.text(722, y + 8, "T-14 queda lista: depends_on T-12 y T-13 en done", 12, C["ink2"], 500)
    d.rect(40, 815, 1220, 44, fill=C["panel"], rx=8)
    d.text(60, 842, "Si un agente se cae, su lease vence sin checkpoint y la tarea vuelve a estar lista desde el último checkpoint.",
           12.5, C["ink2"])
    return d.save()


def tree(d, x, y, lines, hi=None, col=None, lh=21):
    for i, ln in enumerate(lines):
        yy = y + i * lh
        if hi is not None and i in hi:
            d.rect(x - 8, yy - 15, 330, 21, fill=col, rx=4, opacity=0.14)
        d.text(x, yy, ln, 12.5, C["ink"], 400, mono=True)


def d12():
    d = Diagram("12-almacenamiento", 1260, 720, "Dónde vive la memoria: modo repo y modo home",
                "En ambos modos el almacén es un repositorio git pequeño, separado del código. Se elige en hipo init.")
    d.panel(30, 96, 590, 560, "hipo init --store repo", color=C["epi"])
    d.panel(640, 96, 590, 560, "hipo init --store home", color=C["pros"])

    tree(d, 60, 150, ["mi-proyecto/", "├── src/", "├── .git/", "│   ├── objects/  refs/  …",
                      "│   └── hipocampo/", "│       ├── episodic/  semantic/  …", "│       ├── live/",
                      "│       └── index.db", "└── (ningún archivo nuevo en el árbol)"],
         hi={4, 5, 6, 7}, col=C["epi"])
    d.text(400, 234, "← almacén (git propio)", 12, C["ink"], 600)
    d.text(410, 297, "← ignorado por git", 11.5, C["ink2"])

    d.box(60, 370, 250, 64, "../wt-T12", [("rama hipo/T-12", True)], lsize=11.5, tsize=13)
    d.box(60, 452, 250, 64, "../wt-T13", [("rama hipo/T-13", True)], lsize=11.5, tsize=13)
    d.arrow([(310, 402), (400, 402), (400, 272), (388, 272)], color=C["epi"])
    d.arrow([(310, 484), (400, 484), (400, 402)], color=C["epi"], head=False)
    d.text(414, 420, "todos los worktrees comparten", 11.5, C["ink2"])
    d.text(414, 437, ("git-common-dir: una sola memoria"), 11.5, C["ink2"])
    d.text(414, 454, "aunque cambies de rama", 11.5, C["ink2"])

    d.box(60, 548, 530, 80, "origin · rama huérfana hipocampo/memory",
          ["hipo sync hace push y pull del almacén", "con el mismo remoto del proyecto"], color=C["epi"],
          lsize=11.5, tsize=13)

    tree(d, 670, 150, ["~/.hipocampo/", "├── projects.json", "├── global/        (opcional)", "└── projects/",
                       "    └── 9f3e2a…/", "        ├── episodic/  semantic/  …", "        └── index.db"],
         hi={4, 5, 6}, col=C["pros"])
    d.text(1010, 234, "← almacén", 12, C["ink"], 600)
    d.text(1010, 171, "← registro", 11.5, C["ink2"])

    tree(d, 670, 340, ["repo-del-cliente/", "├── src/", "└── .git/        (sin cambios)"])
    d.box(670, 420, 530, 64, None, ["0 archivos de Hipocampo en el repo del cliente.",
                                    "Los hooks se instalan a nivel de usuario."], color=C["good"], lsize=12.5)
    d.box(670, 506, 530, 122, "Identidad del proyecto",
          [("id = git rev-list --max-parents=0 HEAD", True), "el SHA del primer commit es igual en todos",
           "los clones, así que el almacén se reconoce", "aunque el repo cambie de ruta"], lsize=11.5, tsize=13)
    d.arrow([(812, 336), (1000, 336), (1000, 258), (996, 258)], dash=True, color=C["pros"],
            label="id 9f3e2a…", lpos=(900, 328))
    d.text(40, 690, "Nada sale de tu máquina salvo que tú hagas hipo sync (modo repo) o configures un remoto (modo home).",
           12, C["ink2"])
    return d.save()


def d13():
    d = Diagram("13-estados-de-tarea", 1260, 600, "Estados de una tarea",
                "Cómo pasa una tarea entre agentes: leases que vencen, handoffs y bloqueos por conflicto.")
    W, H, Y = 180, 60, 250
    P = {"pending": 120, "ready": 420, "claimed": 720, "done": 1020}
    S = {"pending": ("pending", "esperando dependencias", C["sens"]),
         "ready": ("ready", "cualquiera la puede tomar", C["epi"]),
         "claimed": ("claimed", "un agente con lease", C["work"]),
         "done": ("done", "terminada", C["good"])}
    for k, x in P.items():
        t, s, c = S[k]
        d.pill(x, Y, W, H, t, c, s)
    d.pill(720, 450, W, H, "blocked", C["warn"], "conflicto de decisión")
    d.raw(f'<circle cx="60" cy="280" r="10" fill="{C["ink"]}"/>')
    d.arrow([(70, 280), (120, 280)])
    d.arrow([(300, 280), (420, 280)], label="dependencias", lpos=(360, 262))
    d.text(360, 300, "en done", 11.5, C["ink2"], 500, "middle")
    d.arrow([(600, 280), (720, 280)], label="task claim", lpos=(660, 270))
    d.arrow([(900, 280), (1020, 280)], label="task done", lpos=(960, 270))
    d.arrow([(780, 250), (780, 214), (850, 214), (850, 250)], color=C["work"],
            label="checkpoint renueva el lease", lpos=(815, 206))
    d.arrow([(770, 310), (770, 370), (520, 370), (520, 310)],
            label="handoff · lease vencido", lpos=(645, 362))
    d.arrow([(850, 310), (850, 450)], label="decisiones en conflicto", lpos=(862, 390), lanchor="start")
    d.arrow([(720, 480), (460, 480), (460, 310)], label="un humano resuelve", lpos=(590, 472))
    d.arrow([(1110, 250), (1110, 160), (210, 160), (210, 250)], dash=True, color=C["good"],
            label="desbloquea a las que dependían de ella", lpos=(660, 152))
    d.box(40, 530, 1180, 46, None, ["El lease dura 30 min; cada checkpoint lo renueva. Al vencer, la tarea vuelve a ready "
                                    "con su último checkpoint, y otro agente sigue desde ahí."], lsize=12.5)
    return d.save()
