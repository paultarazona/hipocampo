from svglib import Diagram, C


def d01():
    d = Diagram("01-arquitectura", 1320, 700, "Arquitectura de Hipocampo",
                "Los agentes entran por hooks, CLI o MCP; un único núcleo en Go lee y escribe un almacén local.")
    # columnas
    d.section(40, 112, "Agentes")
    d.section(300, 112, "Canales de entrada")
    d.section(590, 112, "Núcleo hipo")
    d.section(1040, 112, "Almacenamiento local")

    d.box(40, 130, 200, 56, "Claude Code", ["hooks oficiales"])
    d.box(40, 206, 200, 56, "Codex", ["hooks oficiales"])
    d.box(40, 300, 200, 80, "Otros agentes", ["Antigravity, Cursor…", "MCP o shell"])
    d.box(40, 470, 200, 64, "Tú", ["navegador"], color=C["pros"])

    d.box(300, 130, 230, 132, "Hooks", ["camino principal", "6 eventos del ciclo de vida", "costo fijo: 0 tokens"],
          color=C["work"])
    d.box(300, 290, 230, 44, "CLI por shell", [], tsize=13)
    d.box(300, 346, 230, 44, "MCP opcional (3 tools)", [], tsize=13, dash=True)
    d.box(300, 470, 230, 64, "hipo ui", ["127.0.0.1 + token"], color=C["pros"])

    d.arrow([(240, 158), (300, 158)])
    d.arrow([(240, 234), (300, 234)])
    d.arrow([(240, 330), (270, 330), (270, 312), (300, 312)])
    d.arrow([(240, 352), (270, 352), (270, 368), (300, 368)], dash=True)
    d.arrow([(240, 502), (300, 502)])

    # núcleo
    d.panel(580, 130, 400, 430, None, color=C["work"])
    d.text(600, 160, "Núcleo (un binario Go, sin CGO)", 14, C["ink"], 600)
    d.text(600, 180, "hipo / hipo.exe · arranca, responde, termina", 11.5, C["ink2"])
    mods = [("Contrato de eventos", "6 eventos internos"), ("Codificación", "sorpresa + saliencia"),
            ("Activación", "ACT-R híbrida"), ("Recuperación", "L0 · L1 · L2 + know"),
            ("Reconsolidación", "deriva por hash"), ("Sueño", "9 pasos offline"),
            ("Fatiga", "semilla de despertar"), ("Tareas y leases", "pizarra multiagente")]
    for i, (t, s) in enumerate(mods):
        cx = 600 + (i % 2) * 185
        cy = 200 + (i // 2) * 86
        d.box(cx, cy, 175, 72, t, [s], tsize=13, lsize=11.5)
    d.arrow([(530, 196), (580, 196)])
    d.arrow([(530, 340), (580, 340)])
    d.arrow([(530, 502), (580, 502)])

    # almacenamiento
    d.box(1040, 130, 240, 110, "Almacén .memory/", ["Markdown + frontmatter YAML", "repositorio git propio",
                                                   "fuente de verdad"], color=C["epi"])
    d.box(1040, 262, 240, 90, "index.db", ["SQLite: FTS5 + sqlite-vec", "derivado y regenerable"], color=C["sem"])
    d.box(1040, 374, 240, 90, "Ollama local", ["embeddings + chat", "localhost:11434"], color=C["proc"])
    d.box(1040, 486, 240, 74, "~/.hipocampo/", ["projects.json (registro)"], color=C["pros"])
    d.arrow([(980, 185), (1040, 185)], both=True)
    d.arrow([(980, 307), (1040, 307)], both=True)
    d.arrow([(980, 419), (1040, 419)], label="solo sueño", lpos=(1010, 410), dash=True)
    d.arrow([(980, 523), (1040, 523)], both=True)

    d.rect(40, 600, 1240, 54, fill=C["panel"], rx=10)
    d.text(60, 625, "Todo corre en tu máquina.", 13, C["ink"], 600)
    d.text(60, 643, "Sin servidor, sin nube. Si Ollama no responde, el sueño se encola y todo lo demás sigue igual.",
           12, C["ink2"])
    d.legend(760, 632, [("integración", C["work"]), ("cliente visual", C["pros"]), ("datos", C["epi"])])
    return d.save()


def d02():
    d = Diagram("02-sistemas-de-memoria", 1200, 760, "De la mente al código: los sistemas de memoria",
                "Cada estructura del cerebro tiene un componente con la misma función en Hipocampo.")
    rows = [
        ("Registro sensorial", "retiene percepciones crudas por segundos", "Buffer de sesión",
         "salidas de herramientas, diffs y comandos; se purga", "sensory/", C["sens"]),
        ("Memoria de trabajo", "pocos elementos activos (≈4 chunks)", "Ventana del agente",
         "presupuesto fijo de tokens en capas", "L0 · L1 · L2", C["work"]),
        ("Hipocampo", "graba episodios rápido, como índice", "Memoria episódica",
         "sesiones y eventos con fecha, append-only", "episodic/", C["epi"]),
        ("Neocorteza", "conocimiento estable, aprendido lento", "Memoria semántica",
         "hechos, decisiones vigentes, convenciones", "semantic/", C["sem"]),
        ("Ganglios basales", "habilidades y saber hacer", "Memoria procedural",
         "procedimientos y scripts que funcionaron 3+ veces", "procedural/", C["proc"]),
        ("Amígdala", "marca lo importante", "Saliencia",
         "costo del evento: tiempo, reintentos, severidad", "campo salience", C["amy"]),
        ("Memoria prospectiva", "recordar hacer algo después", "Intenciones y tareas",
         "siguiente paso, disparadores, leases", "prospective/", C["pros"]),
    ]
    d.section(40, 110, "En la mente")
    d.section(470, 110, "En Hipocampo")
    y = 124
    for brain, fn, comp, desc, path, col in rows:
        d.box(40, y, 340, 74, brain, [fn], color=col, align="left", tsize=14)
        d.arrow([(380, y + 37), (460, y + 37)], color=col)
        d.box(470, y, 690, 74, None, [], color=col)
        d.text(490, y + 31, comp, 14, C["ink"], 600)
        d.text(490, y + 52, desc, 12, C["ink2"])
        d.rect(990, y + 22, 150, 30, fill=C["surface"], stroke=col, rx=6, sw=1)
        d.text(1065, y + 42, path, 11.5, C["ink"], 500, "middle", mono=True)
        y += 86
    d.text(40, 744, "H.M., sin hipocampo, no formaba recuerdos nuevos pero sí aprendía habilidades:"
           " por eso episódica y procedural son sistemas separados.", 11.5, C["muted"])
    return d.save()


def d03():
    d = Diagram("03-ciclo-de-vida-del-recuerdo", 1200, 640, "Ciclo de vida de un recuerdo",
                "Codificar poco, consolidar offline, recuperar por activación, revalidar al recordar, olvidar archivando.")
    W, H = 170, 84
    d.box(40, 120, W, H, "Evento", ["salida de herramienta,", "corrección, decisión"], color=C["sens"])
    d.box(260, 120, W, H, "Codificación", ["E = ½ sorpresa", "+ ½ saliencia"], color=C["amy"])
    d.box(480, 120, W, H, "Episódica", ["episodio con pistas,", "fuente y ancla"], color=C["epi"])
    d.box(700, 120, W, H, "Sueño", ["replay + abstracción", "cada 3 sesiones o 24 h"], color=C["work"])
    d.box(960, 104, W, 74, "Semántica", ["reglas y decisiones"], color=C["sem"])
    d.box(960, 206, W, 74, "Procedural", ["procedimientos, scripts"], color=C["proc"])

    d.arrow([(210, 162), (260, 162)])
    d.arrow([(430, 162), (480, 162)], label="E ≥ 0.4", lpos=(455, 152))
    d.arrow([(650, 162), (700, 162)])
    d.arrow([(870, 150), (915, 150), (915, 141), (960, 141)], label="3+ episodios", lpos=(915, 128))
    d.arrow([(870, 176), (915, 176), (915, 243), (960, 243)], label="3+ éxitos", lpos=(926, 268), lanchor="start")

    d.box(260, 250, W, 50, None, ["E < 0.4 → se descarta"], dash=True, lsize=12)
    d.arrow([(345, 204), (345, 250)])
    d.box(690, 250, 196, 64, None, ["Archivo", "A < −1.0 y 60 días sin uso"], dash=True, lsize=11.5)
    d.arrow([(785, 204), (785, 250)], label="poda", lpos=(796, 232), lanchor="start")

    yb = 400
    d.box(960, yb, W, H, "Recuperación", ["A ≥ 1.2 se inyecta", "A ≥ 0.5 va al índice L1"], color=C["work"], lsize=11.5)
    d.box(720, yb, W, H, "Memoria de trabajo", ["presupuesto de tokens", "por capa"], color=C["work"], tsize=13)
    d.box(480, yb, W, H, "Agente usa", ["advertencia, regla", "o procedimiento"])
    d.box(260, yb, W, H, "Reconsolidación", ["compara con el", "código actual"], color=C["amy"], tsize=13)
    d.box(40, yb, W, H, "Resultado", ["fortalece, actualiza", "o marca dudoso"], color=C["sem"])

    d.arrow([(1045, 280), (1045, yb)])
    d.arrow([(1130, 141), (1160, 141), (1160, 442), (1130, 442)])
    d.arrow([(960, 442), (890, 442)])
    d.arrow([(720, 442), (650, 442)])
    d.arrow([(480, 442), (430, 442)])
    d.arrow([(260, 442), (210, 442)])
    d.arrow([(125, 400), (125, 350), (520, 350), (520, 204)], dash=True, color=C["sem"],
            label="actualiza el recuerdo", lpos=(320, 342))
    d.text(960, 504, "también recupera episodios", 11, C["muted"])

    d.rect(40, 540, 1120, 56, fill=C["panel"], rx=10)
    d.text(60, 564, "Base:", 12, C["ink"], 600)
    d.text(104, 564, "especificidad de codificación (Tulving) · sistemas complementarios (McClelland et al., 1995) ·",
           12, C["ink2"])
    d.text(104, 582, "reconsolidación (Nader et al., 2000) · homeostasis sináptica (Tononi y Cirelli, 2014) · ACT-R",
           12, C["ink2"])
    return d.save()


def d04():
    d = Diagram("04-flujo-hook-pre-tool", 1200, 736, "Flujo de un hook: antes de usar una herramienta",
                "Cómo una advertencia llega al agente justo cuando va a tocar un archivo con historia.")
    xs = [120, 360, 600, 840, 1070]
    names = [("Agente", "Claude Code / Codex"), ("Harness", "hook PreToolUse"), ("hipo", "hook pre_tool"),
             ("index.db", "SQLite local"), (".memory/", "archivos")]
    cols = [C["line"], C["line"], C["work"], C["sem"], C["epi"]]
    for x, (n, s), c in zip(xs, names, cols):
        d.box(x - 95, 100, 190, 52, n, [s], color=c if c != C["line"] else None, tsize=14, lsize=11)
        d.raw(f'<line x1="{x}" y1="152" x2="{x}" y2="650" stroke="{C["border"]}" stroke-width="1.5" '
              f'stroke-dasharray="4 5"/>')
    # activación de hipo
    d.rect(xs[2] - 7, 236, 14, 350, fill=C["work"], rx=3, opacity=0.18)
    d.rect(xs[2] - 7, 236, 14, 350, stroke=C["work"], rx=3, sw=1)

    msgs = [
        (0, 1, 196, "1  quiere editar prisma/schema.prisma"),
        (1, 2, 246, "2  hipo hook pre_tool (JSON por stdin)"),
        (2, 3, 296, "3  recuerdos con pistas prisma/**"),
        (3, 2, 346, "4  candidatos + log de accesos"),
        (2, 4, 446, "6  ¿cambió anchor.files? (hash)"),
        (2, 3, 496, "7  registra el acceso"),
        (2, 1, 566, "8  {\"inject\": \"⚠ migrate dev borró datos…\"}"),
        (1, 0, 616, "9  contexto adicional; la herramienta corre"),
    ]
    for a, b, y, t in msgs:
        x1, x2 = xs[a], xs[b]
        off = 8 if x2 > x1 else -8
        back = b < a and not (a == 2 and b == 1) and False
        d.arrow([(x1 + off, y), (x2 - off, y)], dash=(b < a),
                color=C["work"] if a == 2 or b == 2 else C["line"])
        d.text((x1 + x2) / 2, y - 8, t, 11.5, C["ink2"], 500, "middle", halo=True)
    # self call
    y = 386
    d.arrow([(xs[2] + 8, y), (xs[2] + 60, y), (xs[2] + 60, y + 26), (xs[2] + 10, y + 26)], color=C["work"])
    d.text(xs[2] + 72, y + 9, "5  A = B + S + 2·C + P + ln(conf)", 11.5, C["ink2"], 500)
    d.text(xs[2] + 72, y + 26, "solo pasan los recuerdos con A ≥ 1.2", 11, C["muted"])

    d.rect(40, 662, 1120, 36, fill=C["panel"], rx=8)
    d.text(60, 685, "Tiempo máximo 2 s. Si hipo falla o tarda, el agente sigue sin memoria: Hipocampo informa, nunca bloquea.",
           12, C["ink2"])
    return d.save()
