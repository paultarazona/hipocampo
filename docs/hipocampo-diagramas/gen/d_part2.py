from svglib import Diagram, C, tw


def d05():
    d = Diagram("05-proceso-de-sueno", 1200, 790, "Proceso de sueño: consolidación offline",
                "hipo sleep convierte episodios en conocimiento, repeticiones en procedimientos, y poda lo que sobra.")
    d.box(60, 100, 560, 46, None, ["Disparo: cada 3 sesiones o cada 24 h, lo que llegue primero  ·  hipo sleep"],
          color=C["work"], lsize=13)
    steps = [
        ("1 · Purga sensorial", ["borra sensory/ de sesiones cerradas"], False),
        ("2 · Replay", ["episodios nuevos + los antiguos", "que un recuerdo nuevo enlaza"], False),
        ("3 · Abstracción", ["3+ episodios de 2+ sesiones", "→ regla semántica (proposed)"], True),
        ("4 · Procedimentalización", ["solución con 3+ éxitos", "→ procedimiento o script"], True),
        ("5 · Interferencia", ["recuerdos que se contradicen", "→ superseded o suspect"], True),
        ("6 · Homeostasis", ["recalcula B; saliencia −10% por ciclo", "si lleva 30 días sin uso"], False),
        ("7 · Poda", ["archiva A < −1.0 con 60 días sin uso;", "comprime episodios de 30+ días"], False),
        ("8 · Proyecciones", ["regenera L0 y la sección", "de AGENTS.md / CLAUDE.md"], False),
        ("9 · Reporte", ["episodio agent: sleep", "con lo que hizo el ciclo"], False),
    ]
    X = [60, 440, 820]
    Y = [180, 340, 500]
    W, H = 320, 112
    order = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
    pos = []
    for (r, c), (t, ln, llm) in zip(order, steps):
        x, y = X[c], Y[r]
        pos.append((x, y))
        d.box(x, y, W, H, t, ln, color=C["proc"] if llm else None,
              tag="LLM local (Ollama)" if llm else "sin LLM", lsize=12)
    d.arrow([(220, 146), (220, 180)])
    for i in range(8):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            if x2 > x1:
                d.arrow([(x1 + W, y1 + H / 2), (x2, y2 + H / 2)])
            else:
                d.arrow([(x1, y1 + H / 2), (x2 + W, y2 + H / 2)])
        else:
            d.arrow([(x1 + W / 2, y1 + H), (x2 + W / 2, y2)])
    # salidas
    d.box(440, 664, 320, 70, "Commit propio del almacén", [("memory: sleep cycle 2026-11-04", True)], tsize=13)
    d.box(820, 664, 320, 70, "Revisión humana", ["reglas proposed → hipo review"], color=C["pros"], tsize=13)
    d.arrow([(980, 612), (980, 664)])
    d.arrow([(900, 612), (900, 640), (600, 640), (600, 664)])
    d.box(60, 664, 320, 70, "Sin Ollama", ["3, 4 y 5 se encolan en", ("live/pending_sleep.jsonl", True)],
          dash=True, tsize=13, lsize=11.5)
    d.legend(60, 766, [("usa el modelo local (presupuesto 20,000 tokens por ciclo)", C["proc"]),
                       ("cálculo determinista", C["border"])])
    return d.save()


def entity(d, x, y, w, name, fields, color=None, note=None):
    rowh = 19
    h = 38 + rowh * len(fields) + 10
    col = color or C["line"]
    d.rect(x, y, w, h, fill=C["surface"], rx=8)
    d.rect(x, y, w, 30, fill=col, rx=8, opacity=0.16)
    d.rect(x, y + 22, w, 8, fill=C["surface"], rx=0)
    d.rect(x, y + 22, w, 8, fill=col, rx=0, opacity=0.16)
    d.rect(x, y, w, h, stroke=col, rx=8, sw=1.5)
    d.raw(f'<line x1="{x}" y1="{y+30}" x2="{x+w}" y2="{y+30}" stroke="{col}" stroke-width="1"/>')
    d.text(x + 12, y + 20, name, 13, C["ink"], 700, maxw=w - 20)
    for i, f in enumerate(fields):
        fname, ftype = f
        fy = y + 30 + 18 + i * rowh
        pk = fname.endswith("*")
        nm = fname.rstrip("*")
        d.text(x + 12, fy, nm, 11.5, C["ink"], 600 if pk else 400, mono=True)
        if pk:
            d.text(x + 14 + tw(nm, 11.5, True), fy, " PK", 9.5, C["work"], 700)
        d.text(x + w - 10, fy, ftype, 11, C["muted"], 400, "end",
               maxw=w - 30 - tw(nm, 11.5, True))
    return h


def d06():
    d = Diagram("06-modelo-de-datos", 1400, 1010, "Modelo de datos",
                "Qué entidades existen, dónde se guarda cada una y cómo se relacionan.")
    d.panel(30, 92, 920, 690, "Almacén · archivos Markdown + YAML (fuente de verdad)", color=C["epi"])
    d.panel(965, 92, 405, 355, "live/ · coordinación (json, jsonl)", color=C["work"])
    d.panel(965, 462, 405, 320, "index.db · derivado, regenerable", color=C["sem"])
    d.panel(30, 800, 1340, 175, "~/.hipocampo/ · registro de proyectos", color=C["pros"])

    entity(d, 60, 132, 210, "Pistas", [("paths", "globs"), ("symbols", "lista"), ("tags", "lista"),
                                       ("branch", "texto")], C["epi"])
    entity(d, 60, 280, 210, "Fuente", [("agent", "texto"), ("model", "texto"), ("validated_by", "texto|null")], C["epi"])
    entity(d, 60, 408, 210, "Ancla", [("commit", "SHA"), ("files", "ruta→hash")], C["epi"])
    entity(d, 330, 132, 270, "Recuerdo", [
        ("id*", "ULID"), ("kind", "enum"), ("title", "≤ 80 car."), ("summary", "≤ 300 car."),
        ("salience", "0–1"), ("confidence", "0–1"), ("status", "enum"), ("uses", "entero"),
        ("last_used", "fecha"), ("created", "fecha"), ("schema_version", "entero")], C["epi"])
    entity(d, 670, 132, 250, "Enlace", [("from", "→ Recuerdo.id"), ("rel", "enum"), ("to", "→ Recuerdo.id")], C["epi"])
    d.text(670, 268, "rel: causes · solves · supersedes", 11, C["ink2"])
    d.text(670, 285, "relates · derived_from", 11, C["ink2"])

    # relaciones dentro de A
    d.arrow([(270, 188), (330, 188)], head=False, label="1:1", lpos=(300, 180))
    d.arrow([(270, 330), (330, 330)], head=False, label="1:1", lpos=(300, 322))
    d.arrow([(270, 447), (300, 447), (300, 372), (330, 372)], head=False, label="1:1", lpos=(286, 462))
    d.arrow([(600, 170), (670, 170)], label="from", lpos=(635, 162))
    d.arrow([(670, 210), (600, 210)], label="to", lpos=(635, 202))
    d.text(635, 240, "N:N", 11, C["muted"], 600, "middle")

    # subtipos
    subs = [
        ("Episodio", [("session_id", "→ Sesión"), ("outcome", "enum"), ("tokens_used", "ent."),
                      ("surprises", "lista")]),
        ("Decisión", [("context", "texto"), ("chosen", "texto"), ("rejected", "lista")]),
        ("Error", [("symptom", "texto"), ("root_cause", "texto"), ("cost_minutes", "ent."), ("retries", "ent.")]),
        ("Solución / Proced.", [("steps", "lista"), ("success_count", "ent."), ("script", "ruta?")]),
        ("Intención / Tarea", [("trigger", "pista"), ("due", "fecha"), ("task_state", "enum"),
                               ("next_step", "texto"), ("depends_on", "lista"), ("scope", "globs"),
                               ("role", "enum")]),
    ]
    xs = [50, 228, 406, 584, 762]
    for x, (n, f) in zip(xs, subs):
        entity(d, x, 566, 168, n, f, C["epi"])
    # bus de herencia
    d.raw(f'<path d="M465 389 L465 520 M134 520 L846 520" fill="none" stroke="{C["line"]}" stroke-width="1.5"/>')
    for x in xs:
        d.raw(f'<path d="M{x+84} 520 L{x+84} 566" fill="none" stroke="{C["line"]}" stroke-width="1.5"/>')
    d.raw(f'<path d="M465 391 L457 405 L473 405 Z" fill="{C["surface"]}" stroke="{C["line"]}" stroke-width="1.5"/>')
    d.text(478, 470, "es un (kind)", 11, C["ink2"], 500)

    # live
    entity(d, 985, 132, 180, "Sesión", [("session_id*", ""), ("harness", "texto"), ("model", "texto"),
                                       ("started", "fecha"), ("ended", "fecha"), ("tokens", "ent."),
                                       ("fatigue", "0–1")], C["work"])
    entity(d, 1180, 132, 170, "Lease", [("task_id*", ""), ("agent", "texto"), ("worktree", "ruta"),
                                       ("expires", "fecha")], C["work"])
    entity(d, 1180, 278, 170, "Evento", [("ts", "fecha"), ("type", "enum"), ("agent", "texto"),
                                        ("task_id", "→ Tarea"), ("payload", "json")], C["work"])
    d.text(985, 345, "Evento.type: claimed · checkpoint ·", 11, C["ink2"])
    d.text(985, 362, "decision · blocked · handoff ·", 11, C["ink2"])
    d.text(985, 379, "done · forgotten", 11, C["ink2"])

    # index.db
    entity(d, 985, 502, 180, "AccessLog", [("memory_id", "→ Rec."), ("ts_active", "horas"),
                                           ("session_id", "→ Ses."), ("used", "bool")], C["sem"])
    entity(d, 1180, 502, 170, "Vector", [("memory_id", "→ Rec."), ("model", "texto"), ("dims", "ent."),
                                        ("vector", "f32[]")], C["sem"])
    entity(d, 985, 646, 365, "FTS5 (búsqueda de texto)", [("memory_id", "→ Recuerdo.id"),
                                                           ("title · summary · body", "texto")], C["sem"])

    d.arrow([(600, 350), (955, 350), (955, 560), (985, 560)], dash=True, color=C["sem"],
            label="memory_id", lpos=(780, 342))

    # registro
    entity(d, 60, 840, 330, "Proyecto", [("id*", "SHA del primer commit"), ("nombre", "texto"),
                                        ("ruta_repo", "ruta"), ("modo", "repo | home"),
                                        ("ruta_almacen", "ruta")], C["pros"])
    d.text(430, 872, "Un proyecto tiene un almacén, y un almacén tiene N recuerdos.", 13, C["ink"], 600)
    d.text(430, 894, "El id es igual en todos los clones y máquinas, así que la memoria", 12, C["ink2"])
    d.text(430, 912, "del mismo repo se reconoce aunque esté en otra ruta.", 12, C["ink2"])
    d.text(430, 944, "Notación:", 12, C["ink"], 600)
    d.text(500, 944, "PK = identificador · → = referencia a otra entidad · triángulo = subtipo de Recuerdo",
           12, C["ink2"])
    return d.save()


def d07():
    d = Diagram("07-estados-del-recuerdo", 1200, 620, "Estados de un recuerdo",
                "El estado decide si un recuerdo se inyecta, se muestra con advertencia o queda fuera.")
    W, H = 190, 60
    P = {"proposed": (285, 120), "active": (285, 290), "suspect": (625, 290),
         "superseded": (965, 290), "archived": (285, 470), "forgotten": (965, 120)}
    S = {"proposed": ("proposed", "regla del sueño sin aprobar", C["pros"]),
         "active": ("active", "se inyecta y se recupera", C["good"]),
         "suspect": ("suspect", "solo resumen + advertencia", C["warn"]),
         "superseded": ("superseded", "oculto; queda el historial", C["line"]),
         "archived": ("archived", "fuera del índice; en archive/", C["sens"]),
         "forgotten": ("forgotten", "borrado; queda un evento", C["bad"])}
    for k, (x, y) in P.items():
        t, s, c = S[k]
        d.pill(x, y, W, H, t, c, s)
    # inicio
    d.raw(f'<circle cx="110" cy="320" r="10" fill="{C["ink"]}"/>')
    d.arrow([(120, 320), (285, 320)], label="codificación", lpos=(200, 310))
    # proposed -> active / forgotten
    d.arrow([(380, 180), (380, 290)], label="hipo review aprueba", lpos=(392, 240), lanchor="start")
    d.arrow([(475, 150), (965, 150)], label="hipo review rechaza", lpos=(720, 140))
    # active <-> suspect
    d.arrow([(475, 306), (625, 306)], label="deriva > 60%, contradicción", lpos=(550, 298), lsize=11)
    d.arrow([(625, 336), (475, 336)], label="sigue vigente", lpos=(550, 356), lsize=11)
    # suspect -> superseded
    d.arrow([(815, 320), (965, 320)], label="nueva versión", lpos=(890, 310), lsize=11)
    # active -> superseded (por debajo)
    d.arrow([(440, 350), (440, 410), (1060, 410), (1060, 350)], label="reemplazado por otro recuerdo (supersedes)",
            lpos=(750, 402), lsize=11)
    # active -> archived
    d.arrow([(330, 350), (330, 470)], label="poda: A < −1.0", lpos=(318, 405), lanchor="end", lsize=11)
    d.text(318, 422, "y 60 días sin uso", 11, C["ink2"], 500, "end")
    # nota
    d.box(625, 470, 535, 90, None, ["hipo forget <id> lleva cualquier estado a forgotten.",
                                    "El evento forgotten guarda solo el id, para que la",
                                    "deduplicación no vuelva a crear ese recuerdo."], dash=True, align="left")
    d.text(285, 560, "Un uso exitoso puede reactivar un recuerdo archivado.", 11.5, C["muted"])
    return d.save()
