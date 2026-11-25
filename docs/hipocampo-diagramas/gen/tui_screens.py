import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tuilib import Screen, window, T

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tui")
COLS, ROWS = 150, 46
TABS = ["1 Resumen", "2 Memoria", "3 Red", "4 Tareas", "5 Sueño", "6 Métricas"]


def chrome(s, active, ctx_right):
    s.bg(0, 0, 13, T["accent"])
    s.put(1, 0, "◆ HIPOCAMPO", "#0f1218", True)
    s.seg(15, 0, [("mi-proyecto", T["fg"], True), ("  ·  repo  ·  9f3e2a  ·  rama de memoria hipocampo/memory",
                                                       T["dim"])])
    s.put(COLS - len(ctx_right) - 1, 0, ctx_right, T["dim"])
    x = 1
    for i, t in enumerate(TABS):
        lab = f" {t} "
        if i == active:
            s.bg(x, 1, len(lab), T["sel"])
            s.put(x, 1, lab, T["fg"], True)
        else:
            s.put(x, 1, lab, T["dim"])
        x += len(lab) + 1


def footer(s, keys, right):
    s.bg(0, ROWS - 1, COLS, "#1a1f2a")
    x = 1
    for k, d in keys:
        x = s.seg(x, ROWS - 1, [(k, T["accent"], True), (" " + d + "   ", T["dim"])])
    s.put(COLS - len(right) - 1, ROWS - 1, right, T["dim"])


KIND = {"error": T["red"], "decisión": T["sem"], "proced.": T["proc"], "solución": T["sem"],
        "hecho": T["sem"], "intención": T["pros"], "episodio": T["epi"]}


def screen_resumen():
    s = Screen(COLS, ROWS)
    chrome(s, 0, "Ollama ●  ·  2 agentes  ·  10:32")

    # ---- izquierda
    s.box(0, 2, 34, 11, "Proyectos", key="p")
    rows = [("▸", "mi-proyecto", "312", "repo", True), (" ", "app-turismo", "148", "repo", False),
            (" ", "cliente-acme", " 57", "home", False), (" ", "hipocampo", " 23", "repo", False)]
    for i, (m, n, c, mode, sel) in enumerate(rows):
        y = 4 + i
        if sel:
            s.bg(1, y, 32, T["sel"])
        s.seg(2, y, [(m + " ", T["accent"], True), (f"{n:<15}", T["fg"], sel), (f"{c:>4}  ", T["dim"]),
                     (mode, T["pros"] if mode == "home" else T["faint"])])
    s.put(2, 9, "4 proyectos · 540 recuerdos", T["dim"])
    s.seg(2, 10, [("[p]", T["accent"]), (" cambiar   ", T["dim"]), ("[/]", T["accent"]), (" buscar", T["dim"])])

    s.box(0, 13, 34, 12, "Sistemas de memoria")
    sysrows = [("episódica", 184, T["epi"]), ("semántica", 61, T["sem"]), ("procedural", 9, T["proc"]),
               ("prospectiva", 14, T["pros"]), ("archivo", 44, T["faint"])]
    for i, (n, v, col) in enumerate(sysrows):
        y = 15 + i
        s.seg(2, y, [("● ", col), (f"{n:<12}", T["fg"]), (f"{v:>4}", T["dim"])])
        s.bar(21, y, 11, v / 184, col)
    s.seg(2, 21, [("▲ ", T["yellow"]), ("3 suspect", T["fg"]), ("   ", T["dim"]), ("✕ ", T["red"]),
                  ("1 conflicto", T["fg"])])
    s.put(2, 22, "último sueño hace 3 h", T["dim"])
    s.seg(2, 23, [("2 reglas proposed  ", T["fg"]), ("[r]", T["accent"])])

    s.box(0, 25, 34, 20, "Contexto · sesión claude")
    ctx = [("rama", "hipo/T-12"), ("archivos", "prisma/schema.prisma"), ("", "src/api/payments.ts"),
           ("", "src/api/users.ts"), ("comandos", "pnpm test"), ("", "pnpm prisma migrate")]
    for i, (k, v) in enumerate(ctx):
        s.seg(2, 27 + i, [(f"{k:<10}", T["dim"]), (v, T["fg"])])
    s.put(2, 34, "lo que se inyectó", T["title"], True)
    inj = [("L0", "tarea y 4 reglas", "540 tk"), ("L1", "7 títulos", "410 tk"),
           ("▲", "1 advertencia", "290 tk")]
    for i, (a, b, c) in enumerate(inj):
        s.seg(2, 35 + i, [(f"{a:<4}", T["accent"]), (f"{b:<20}", T["fg"]), (f"{c:>6}", T["dim"])])
    s.put(2, 39, "─" * 30, T["faint"])
    s.seg(2, 40, [(f"{'total memoria':<21}", T["dim"]), ("1,240 tk", T["fg"], True)])
    s.seg(2, 41, [(f"{'hook p95':<21}", T["dim"]), ("  42 ms", T["fg"])])
    s.seg(2, 42, [(f"{'precisión (7 días)':<21}", T["dim"]), ("   68 %", T["green"])])

    # ---- centro: recuerdos
    s.box(34, 2, 68, 22, "Recuerdos · por activación", key="2")
    s.seg(36, 3, [("filtro ", T["dim"]), ("contexto actual", T["fg"]), ("  ·  ", T["faint"]),
                  ("▲ se inyecta ≥ 1.2   ", T["yellow"]), ("· índice L1 ≥ 0.5", T["dim"])])
    s.put(35, 5, f"{'A':>5}  {'tipo':<10} {'título':<34} {'estado':<9}{'usos':>4}", T["faint"], True)
    mem = [(1.57, "error", "prisma migrate dev borra datos", "active", 3),
           (1.31, "decisión", "fechas siempre en UTC", "active", 11),
           (1.18, "proced.", "migrar DB sin reset", "active", 4),
           (0.94, "solución", "usar migrate deploy en staging", "active", 3),
           (0.82, "hecho", "API REST bajo /api/v2", "active", 7),
           (0.71, "error", "timeout de Postgres en e2e", "suspect", 2),
           (0.63, "intención", "revisar índices al tocar orders", "active", 1),
           (0.58, "episodio", "codex · refactor de auth", "active", 1),
           (0.52, "decisión", "zod para validar payloads", "active", 5)]
    y = 6
    for i, (a, k, t, st, u) in enumerate(mem):
        sel = i == 0
        if sel:
            s.bg(35, y, 66, T["sel"])
        mark = "▲" if a >= 1.2 else " "
        stcol = T["yellow"] if st == "suspect" else T["dim"]
        s.seg(35, y, [(f"{a:>5.2f}", T["yellow"] if a >= 1.2 else T["fg"], a >= 1.2), (f"{mark} ", T["yellow"]),
                      (f"{k:<10}", KIND[k]), (f" {t:<34}", T["fg"], sel), (f" {st:<9}", stcol), (f"{u:>4}", T["dim"])],
              maxw=66)
        y += 1
    s.put(35, y, "─ ─ ─ bajo el umbral L1: no se muestran al agente ─ ─ ─ ─ ─ ─ ─ ─ ─", T["faint"])
    y += 1
    for a, k, t, st, u in [(0.41, "hecho", "monorepo con pnpm workspaces", "active", 9),
                           (0.22, "episodio", "claude · fix de CORS", "active", 1),
                           (-0.37, "solución", "reiniciar contenedor de Redis", "active", 1)]:
        s.seg(35, y, [(f"{a:>5.2f}  ", T["faint"]), (f"{k:<10}", T["faint"]), (f" {t:<34}", T["faint"]),
                      (f" {st:<9}", T["faint"]), (f"{u:>4}", T["faint"])])
        y += 1
    s.seg(36, 22, [("312 recuerdos · 12 visibles   ", T["dim"]), ("[f]", T["accent"]), (" filtrar  ", T["dim"]),
                   ("[t]", T["accent"]), (" tipo  ", T["dim"]), ("[s]", T["accent"]), (" ordenar", T["dim"])])

    # ---- centro: detalle
    s.box(34, 24, 68, 21, "Detalle", key="enter")
    s.seg(36, 26, [("error", T["red"], True), (" · 01JC8XK4M2", T["dim"])])
    s.seg(89, 26, [("● ", T["green"]), ("active", T["fg"])])
    s.put(36, 27, "prisma migrate dev borra datos en la DB compartida", T["fg"], True)
    s.put(36, 28, "Correr migrate dev contra staging reseteó la tabla users.", T["dim"])
    s.put(36, 29, "Usar migrate deploy.", T["dim"])
    det = [("pistas", [("prisma/**  scripts/db/**  ", T["cyan"]), ("prisma migrate dev", T["cyan"])]),
           ("fuente", [("codex · gpt-x · ", T["fg"]), ("validado por human", T["green"])]),
           ("ancla", [("a1b2c3d", T["fg"], True), (" · schema.prisma cambió 4 % ", T["dim"]), ("sin deriva", T["green"])]),
           ("enlaces", [("solved_by → ", T["dim"]), ("01JC8XM7P1", T["sem"]), (" usar migrate deploy", T["fg"])]),
           ("", [("relates   → ", T["dim"]), ("proc_007", T["proc"]), ("   migrar DB sin reset", T["fg"])])]
    for i, (k, parts) in enumerate(det):
        s.seg(36, 31 + i, [(f"{k:<11}", T["dim"])] + parts, maxw=64)
    s.put(36, 36, "saliencia", T["dim"])
    s.bar(47, 36, 18, 0.90, T["red"])
    s.put(66, 36, "0.90", T["fg"])
    s.put(73, 36, "confianza", T["dim"])
    s.bar(83, 36, 12, 0.95, T["green"])
    s.put(96, 36, "0.95", T["fg"])
    s.seg(36, 38, [("activación  ", T["dim"]), ("B ", T["dim"]), ("−0.48", T["epi"]), ("  S ", T["dim"]),
                   ("+0.90", T["proc"]), ("  2·C ", T["dim"]), ("+1.20", T["sem"]), ("  ln(conf) ", T["dim"]),
                   ("−0.05", T["yellow"]), ("  = ", T["dim"]), ("1.57", T["yellow"], True)], maxw=64)
    s.seg(36, 39, [("historial   ", T["dim"]), ("creado 28 oct · 3 usos · reconsolidado hace 2 h", T["fg"])])
    s.seg(36, 42, [("[e]", T["accent"]), (" editar   ", T["dim"]), ("[d]", T["accent"]), (" marcar dudoso   ", T["dim"]),
                   ("[g]", T["accent"]), (" olvidar   ", T["dim"]), ("[l]", T["accent"]), (" ver en la red", T["dim"])])

    # ---- derecha
    s.box(102, 2, 48, 12, "Agentes", key="4")
    ag = [("Claude Code", "opus", "T-12", "lease 18 m", 0.62, "cansado", "hipo/T-12 · 84k tokens", T["yellow"]),
          ("Codex", "gpt-x", "T-13", "lease 26 m", 0.31, "despierto", "hipo/T-13 · 41k tokens", T["green"])]
    y = 4
    for n, m, t, l, f, st, wt, col in ag:
        s.seg(104, y, [("● ", T["green"]), (f"{n:<12}", T["fg"], True), (f"{m:<7}", T["dim"]), (f"{t:<6}", T["accent"]),
                       (l, T["dim"])])
        s.put(106, y + 1, "fatiga", T["dim"])
        s.bar(113, y + 1, 16, f, col)
        s.seg(130, y + 1, [(f"{f:.2f} ", T["fg"]), (st, col)])
        s.put(106, y + 2, wt, T["faint"])
        y += 4
    s.seg(104, 12, [("○ ", T["faint"]), ("T-15 lista, sin agente", T["dim"])])

    s.box(102, 14, 48, 11, "Tareas", key="4")
    tk = [("T-11", "✓", "done", "modelo de usuarios", "", T["green"]),
          ("T-12", "▶", "claimed", "API de pagos", "claude", T["accent"]),
          ("T-13", "▶", "claimed", "pantalla de pago", "codex", T["accent"]),
          ("T-14", "◷", "pending", "integración", "← 12, 13", T["dim"]),
          ("T-15", "○", "ready", "tests e2e de pagos", "", T["epi"]),
          ("T-16", "■", "blocked", "formato de moneda", "conflicto", T["yellow"])]
    for i, (i_, ic, st, n, who, col) in enumerate(tk):
        s.seg(104, 16 + i, [(f"{i_} ", T["fg"], True), (f"{ic} ", col), (f"{st:<8}", col), (f"{n:<19}", T["fg"]),
                            (who, T["dim"])], maxw=44)
    s.seg(104, 23, [("[enter]", T["accent"]), (" detalle  ", T["dim"]), ("[u]", T["accent"]), (" liberar  ", T["dim"]),
                    ("[g]", T["accent"]), (" grafo", T["dim"])])

    s.box(102, 25, 48, 13, "Pizarra · eventos")
    ev = [("10:31", "codex", "checkpoint T-13", T["dim"]),
          ("10:28", "claude", "decision: api/users v2", T["sem"]),
          ("10:28", "hipo", "→ codex «A cambió api/users»", T["accent"]),
          ("10:24", "hipo", "▲ advertencia a claude", T["yellow"]),
          ("10:20", "claude", "claim T-12", T["dim"]),
          ("10:19", "codex", "claim T-12 rechazado", T["red"]),
          ("10:19", "codex", "claim T-13", T["dim"]),
          ("10:02", "hipo", "sueño · 2 reglas proposed", T["pros"]),
          ("09:58", "claude", "checkpoint T-11 · done", T["green"])]
    for i, (t, w, m, col) in enumerate(ev):
        s.seg(104, 27 + i, [(t + "  ", T["faint"]), (f"{w:<7}", T["dim"]), (m, col)], maxw=44)

    s.box(102, 38, 48, 7, "Sueño", key="5")
    s.seg(104, 40, [("último ciclo ", T["dim"]), ("hace 3 h", T["fg"]), (" · próximo en 1 sesión", T["dim"])])
    s.seg(104, 41, [("2 reglas proposed", T["pros"], True), (" · 1 procedimiento nuevo", T["fg"])])
    s.seg(104, 42, [("Ollama ", T["dim"]), ("● ", T["green"]), ("bge-m3 · modelo de chat local", T["fg"])])

    footer(s, [("↑↓", "mover"), ("tab", "panel"), ("enter", "abrir"), ("/", "buscar"), ("1-6", "vistas"),
               ("r", "revisar"), ("S", "dormir ahora"), ("?", "ayuda"), ("q", "salir")],
           "v1.0")
    return window(s, f"{OUT}/tui-01-resumen.svg", "hipo tui — mi-proyecto",
                  "Cliente TUI · Resumen", "Proyectos, memoria, agentes, tareas y eventos en una sola pantalla.")


def node(s, x, y, kind, label, col, sel=False, dim=False):
    txt = f" {kind} · {label} "
    w = len(txt) + 2
    s.box(x, y, w, 3, None, col if not dim else T["faint"])
    if sel:
        s.bg(x + 1, y + 1, w - 2, T["sel"])
    s.put(x + 1, y + 1, txt, T["fg"] if not dim else T["dim"], sel)
    return x, y, w


def hline(s, x1, x2, y, col=None, label=None):
    col = col or T["faint"]
    s.put(min(x1, x2), y, "─" * abs(x2 - x1), col)
    if label:
        mx = (x1 + x2) // 2 - len(label) // 2
        s.put(mx, y, label, T["dim"])


def vline(s, x, y1, y2, col=None):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        s.put(x, y, "│", col or T["faint"])


def screen_red():
    s = Screen(COLS, ROWS)
    chrome(s, 2, "Ollama ●  ·  2 agentes  ·  10:34")
    s.box(0, 2, 112, 43, "Red de memoria · vecindario de 01JC8XK4M2 · 2 saltos", key="l")
    s.box(112, 2, 38, 43, "Leyenda y filtros")

    # nodos (x, y = esquina superior; alto 3 filas)
    node(s, 42, 20, "error", "prisma migrate dev borra datos", T["red"], sel=True)          # 42..84
    for y, l in [(8, "test falla tras pasar"), (14, "staging sin users"), (30, "migrate en CI")]:
        node(s, 2, y, "episodio", l, T["epi"])
    node(s, 46, 6, "error", "timeout de Postgres en e2e", T["yellow"])                     # 46..84
    node(s, 76, 12, "solución", "usar migrate deploy", T["sem"])                           # 76..110
    node(s, 76, 28, "proced.", "migrar DB sin reset", T["proc"])
    node(s, 40, 34, "decisión", "staging solo con migrate deploy", T["sem"])
    node(s, 2, 38, "solución", "reiniciar Redis", T["faint"], dim=True)

    s.edge([(37.5, 9), (40, 9), (40, 21), (42.5, 21)], T["epi"], head=True)
    s.edge([(33.5, 15), (40, 15)], T["epi"], head=False)
    s.edge([(29.5, 31), (40, 31), (40, 21)], T["epi"], head=False)
    s.put(26, 12, "contiene", T["dim"])
    s.edge([(63, 8), (63, 20)], T["yellow"], dash=True)
    s.put(65, 11, "relates", T["dim"])
    s.put(48, 4, "▲ suspect: el código cambió 64 %", T["yellow"])
    s.edge([(80, 20), (80, 14)], T["sem"])
    s.put(82, 17, "solved_by", T["dim"])
    s.edge([(100, 14), (100, 28)], T["proc"])
    s.put(102, 20, "sueño:", T["dim"])
    s.put(102, 21, "3+ éxitos", T["dim"])
    s.edge([(60, 22), (60, 34)], T["sem"], dash=True)
    s.put(62, 27, "derived_from", T["dim"])
    s.put(62, 28, "(+3 episodios)", T["faint"])
    s.put(48, 38, "proposed · esperando revisión", T["pros"])
    s.edge([(17, 32), (17, 35), (40.5, 35)], T["sem"], dash=True)
    s.put(2, 42, "archivado · A = −1.32", T["faint"])

    # leyenda
    leg = [("episódica", T["epi"]), ("semántica", T["sem"]), ("procedural", T["proc"]), ("prospectiva", T["pros"]),
           ("error / riesgo", T["red"]), ("suspect", T["yellow"]), ("archivado", T["faint"])]
    for i, (n, col) in enumerate(leg):
        s.seg(114, 4 + i, [("■ ", col), (n, T["fg"])])
    s.put(114, 12, "brillo = activación actual", T["dim"])
    s.put(114, 13, "▼ ▶ = dirección del enlace", T["dim"])
    s.put(114, 15, "filtros", T["title"], True)
    fl = [("[x]", "episódica"), ("[x]", "semántica"), ("[x]", "procedural"), ("[ ]", "prospectiva"),
          ("[x]", "mostrar suspect"), ("[ ]", "mostrar archivados")]
    for i, (b, n) in enumerate(fl):
        s.seg(114, 16 + i, [(b + " ", T["accent"]), (n, T["fg"])])
    s.seg(114, 23, [("saltos  ", T["dim"]), ("◀ 2 ▶", T["fg"], True)])
    s.seg(114, 24, [("pista   ", T["dim"]), ("prisma/**", T["cyan"])])
    s.put(114, 26, "selección", T["title"], True)
    sel = [("tipo", "error"), ("A", "1.57 ▲"), ("enlaces", "5"), ("fuente", "codex"), ("ancla", "a1b2c3d")]
    for i, (k, v) in enumerate(sel):
        s.seg(114, 27 + i, [(f"{k:<9}", T["dim"]), (v, T["fg"])])
    s.seg(114, 33, [("[enter]", T["accent"]), (" abrir detalle", T["dim"])])
    s.seg(114, 34, [("[c]", T["accent"]), (" centrar en vecino", T["dim"])])
    s.seg(114, 35, [("[z]", T["accent"]), (" agrupar por pista", T["dim"])])
    s.put(114, 38, "con más de 2,000 nodos", T["dim"])
    s.put(114, 39, "visibles se agrupan por", T["dim"])
    s.put(114, 40, "pista o tipo", T["dim"])

    footer(s, [("←↑↓→", "moverse"), ("enter", "abrir"), ("c", "centrar"), ("+/-", "saltos"), ("z", "agrupar"),
               ("f", "filtros"), ("esc", "volver")], "12 nodos · 14 enlaces")
    return window(s, f"{OUT}/tui-02-red.svg", "hipo tui — mi-proyecto · red",
                  "Cliente TUI · Red de memoria", "Navegar por enlaces: de qué episodios salió un error, qué lo resolvió y qué se aprendió.")


def screen_sueno():
    s = Screen(COLS, ROWS)
    chrome(s, 4, "Ollama ●  ·  2 agentes  ·  10:36")
    s.box(0, 2, 44, 43, "Ciclos de sueño", key="5")
    cyc = [("hoy 10:02", "3 sesiones", "2 reglas · 1 proced. · 6 archivados", True),
           ("ayer 18:40", "24 h", "1 regla · 9 archivados", False),
           ("3 nov 09:15", "3 sesiones", "0 reglas · 2 conflictos", False),
           ("1 nov 20:03", "24 h", "1 proced. · 4 archivados", False)]
    y = 4
    for d_, why, what, sel in cyc:
        if sel:
            s.bg(1, y, 42, T["sel"], 2)
        s.seg(2, y, [("▸ " if sel else "  ", T["accent"]), (f"{d_:<14}", T["fg"], sel), (why, T["dim"])])
        s.put(4, y + 1, what, T["dim"])
        y += 3
    s.put(2, 17, "pasos del ciclo de hoy", T["title"], True)
    steps = [("1", "purga sensorial", "✓", "sin LLM"), ("2", "replay · 14 episodios", "✓", "sin LLM"),
             ("3", "abstracción", "✓", "LLM"), ("4", "procedimentalización", "✓", "LLM"),
             ("5", "interferencia", "✓", "LLM"), ("6", "homeostasis", "✓", "sin LLM"),
             ("7", "poda · 6 archivados", "✓", "sin LLM"), ("8", "proyecciones", "✓", "sin LLM"),
             ("9", "reporte", "✓", "sin LLM")]
    for i, (n, t, ok, llm) in enumerate(steps):
        s.seg(2, 18 + i, [(f"{n} ", T["faint"]), (f"{t:<24}", T["fg"]), (ok + " ", T["green"]),
                          (llm, T["proc"] if llm == "LLM" else T["faint"])])
    s.seg(2, 28, [("tokens del modelo local ", T["dim"]), ("11,820 / 20,000", T["fg"])])
    s.bar(2, 29, 40, 11820 / 20000, T["proc"])
    s.seg(2, 31, [("commit ", T["dim"]), ("m03", T["fg"], True), (" memory: sleep cycle", T["dim"])])

    s.box(44, 2, 106, 30, "Regla propuesta 1 de 2 · dec_015", key="r")
    s.seg(46, 4, [("decisión", T["sem"], True), ("  ·  ", T["faint"]), ("proposed", T["pros"], True),
                  ("  ·  confianza inicial 0.60  ·  saliencia 0.72", T["dim"])])
    s.put(46, 6, "En staging, las migraciones se aplican solo con `prisma migrate deploy`;", T["fg"], True)
    s.put(46, 7, "`migrate dev` queda reservado para la base local.", T["fg"], True)
    s.put(46, 9, "por qué el sueño la propone", T["title"], True)
    s.seg(46, 10, [("• ", T["dim"]), ("3 episodios", T["fg"]), (" de ", T["dim"]), ("2 sesiones", T["fg"]),
                   (" con el mismo error y pistas en común (similitud 0.86)", T["dim"])])
    s.seg(46, 11, [("• ", T["dim"]), ("1 solución", T["fg"]), (" con 3 éxitos que ya apunta en esa dirección", T["dim"])])
    s.seg(46, 12, [("• ", T["dim"]), ("ninguna", T["fg"]), (" decisión activa la contradice", T["dim"])])
    s.put(46, 14, "derived_from", T["title"], True)
    src = [("episodio", "ep_01JC8X", "test falla tras pasar · codex · 28 oct", T["epi"]),
           ("episodio", "ep_01JD2Q", "staging sin users · claude · 30 oct", T["epi"]),
           ("episodio", "ep_01JF7K", "migrate en CI · codex · 3 nov", T["epi"]),
           ("solución", "01JC8XM7P1", "usar migrate deploy · 3 éxitos", T["sem"])]
    for i, (k, i_, d_, col) in enumerate(src):
        s.seg(46, 15 + i, [(f"{k:<10}", col), (f"{i_:<12}", T["fg"], True), (d_, T["dim"])])
    s.put(46, 20, "pistas", T["title"], True)
    s.seg(46, 21, [("prisma/**   scripts/db/**   .github/workflows/deploy.yml   prisma migrate", T["cyan"])])
    s.put(46, 23, "dónde aparecerá si la apruebas", T["title"], True)
    s.seg(46, 24, [("• ", T["dim"]), ("L0", T["accent"], True), (" de cualquier sesión que toque prisma/** (entra entre las 5 reglas de mayor saliencia)", T["dim"])],
          maxw=102)
    s.seg(46, 25, [("• ", T["dim"]), ("sección generada de AGENTS.md / CLAUDE.md", T["fg"])])
    s.bg(46, 28, 14, "#1f3a2a")
    s.put(47, 28, "[a] aprobar", T["green"], True)
    s.bg(62, 28, 14, "#3a1f24")
    s.put(63, 28, "[x] rechazar", T["red"], True)
    s.bg(78, 28, 22, T["sel"])
    s.put(79, 28, "[e] editar y aprobar", T["fg"], True)
    s.put(102, 28, "[n] siguiente   [o] abrir fuentes", T["dim"])
    s.put(46, 30, "al aprobar: status active · validated_by human · commit propio del almacén", T["faint"])

    s.box(44, 32, 106, 13, "Otros cambios del ciclo")
    ch = [("+", "procedimiento", "proc_008 · regenerar cliente de prisma", "3 éxitos · script propuesto", T["proc"]),
          ("~", "superseded", "dec_009 · usar moment.js", "reemplazada por dec_011 (date-fns)", T["faint"]),
          ("!", "suspect", "01JE1B · timeout de Postgres en e2e", "el código cambió 64 %", T["yellow"]),
          ("-", "archivado", "6 recuerdos", "A < −1.0 y 60 días sin uso · [v] ver", T["dim"]),
          ("·", "comprimido", "11 episodios de más de 30 días", "cuerpo → summary, completo en git", T["dim"])]
    for i, (sg, k, n, w, col) in enumerate(ch):
        s.seg(46, 34 + i * 2, [(sg + " ", col, True), (f"{k:<15}", col), (f"{n:<42}", T["fg"]), (w, T["dim"])],
              maxw=102)

    footer(s, [("a", "aprobar"), ("x", "rechazar"), ("e", "editar"), ("n", "siguiente"), ("↑↓", "ciclo"),
               ("o", "fuentes"), ("esc", "volver")], "las decisiones quedan con source.agent: human")
    return window(s, f"{OUT}/tui-03-sueno.svg", "hipo tui — mi-proyecto · sueño",
                  "Cliente TUI · Revisión del sueño", "Las reglas que propone el sueño no llegan a los agentes hasta que tú las apruebas.")


if __name__ == "__main__":
    import subprocess, os
    for f in (screen_resumen, screen_red, screen_sueno):
        p = f()
        png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "png", os.path.basename(p)[:-4] + ".png"); os.makedirs(os.path.dirname(png), exist_ok=True)
        subprocess.run(["rsvg-convert", "-w", "1500", p, "-o", png], check=True)
        print("ok", p)
