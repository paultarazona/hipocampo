# 05 · Contrato de datos

Qué muestra cada panel, de dónde lo lee, cómo lo calcula y cuándo se actualiza. Regla general: **la TUI no calcula nada que el núcleo ya calcule.** Activación, fatiga, deriva y métricas vienen de los paquetes del núcleo (`internal/activation`, `internal/fatigue`, `internal/reconsolidate`, `internal/stats`) a través de una capa de consultas de solo lectura (`internal/tui/query`, ver 09).

## 1. Fuentes y cómo se vigilan

| Fuente | Ruta | Acceso | Cómo se detectan cambios |
| --- | --- | --- | --- |
| Registro de proyectos | `~/.hipocampo/projects.json` | Lectura | Vigilancia de archivo; si no hay, sondeo cada 5 s |
| Configuración | `.memory/config.toml` | Lectura | Vigilancia de archivo |
| Recuerdos | `.memory/{episodic,semantic,procedural,prospective,archive}/**.md` | Lectura (escritura solo por el núcleo) | Vigilancia de carpetas |
| Índice | `.memory/index.db` | SQLite en solo lectura | `PRAGMA data_version` cada 1 s (barato; cambia cuando otro proceso escribe) |
| Eventos | `.memory/live/events.jsonl` | Lectura incremental desde el último offset | Vigilancia de archivo; sondeo cada 1 s de respaldo |
| Leases | `.memory/live/leases.json` | Lectura | Vigilancia de archivo |
| Sesiones | `.memory/live/sessions/<session_id>.json` (ver D-1) | Lectura | Vigilancia de carpeta |
| Ciclos de sueño | Episodios `agent: sleep` + `live/pending_sleep.jsonl` | Lectura | Vigilancia de archivo |
| Ollama | `GET {ollama.url}/api/tags` | HTTP, tiempo máximo 1 s | Sondeo cada 30 s en segundo plano |
| Preferencias de la TUI | `~/.hipocampo/tui.toml` | Lectura y escritura (solo de la TUI) | — |

Todas las lecturas se hacen fuera del ciclo de dibujo y llegan a la vista como mensajes (ver 09). Si un archivo está a medio escribir (JSON inválido), se descarta esa lectura y se reintenta en el siguiente cambio, sin mostrar error salvo que falle 3 veces seguidas.

## 2. Cabecera

| Dato | Fuente | Cálculo |
| --- | --- | --- |
| Proyecto, modo, id | Registro | `nombre`, `modo`, primeros 6 caracteres de `id` |
| Ollama | Sondeo | `●` verde: responde y están `embed_model` y `chat_model`; `●` amarillo: responde y falta alguno; `○`: no responde |
| Agentes | Sesiones + leases | Sesiones abiertas con al menos un lease vigente |
| Problemas `!` | `doctor` del núcleo | Cuenta de: conflictos de decisión, leases vencidos, ámbitos cruzados, índice con `data_version` atrasado frente a archivos, modelos faltantes |

## 3. Resumen y Memoria

### Proyectos

| Campo | Fuente | Nota |
| --- | --- | --- |
| nombre, modo, ruta | Registro | Ruta inexistente → `✕ ruta no encontrada` |
| recuerdos activos | `index.db`: `COUNT(*) WHERE status = 'active'` | Por proyecto; se abre cada índice en solo lectura solo para contar, y se cierra |
| orden | `ts` del último evento en `live/events.jsonl` | Proyectos sin eventos al final, por nombre |

### Sistemas de memoria

| Campo | Cálculo |
| --- | --- |
| episódica / semántica / procedural / prospectiva | Conteo por carpeta del almacén, `status ≠ archived` |
| archivo | Conteo en `archive/` |
| suspect | `status = 'suspect'` |
| conflictos | Pares de decisiones activas marcados por el paso 5 del sueño y no resueltos |
| último sueño | `created` del último episodio `agent: sleep` |
| reglas por revisar | `status = 'proposed'` |
| aviso de tope | `semánticas activas / limits.max_semantic_rules ≥ 0.9` |

### Contexto de sesión

| Campo | Fuente | Nota |
| --- | --- | --- |
| agente, modelo, rama | Sesión | `harness`, `model`, rama del worktree |
| archivos, comandos | Sesión: ventana de pistas de contexto | Los mismos que usa la activación: archivos de los últimos 10 pasos y comandos recientes |
| inyectado por capa | `index.db`, tabla `injections` (ver D-2) | Agrupado por `layer` (`L0`, `L1`, `seed`, `warning`), con `SUM(tokens)` |
| total memoria | Suma de lo anterior + costo fijo declarado (`AGENTS.md`, definiciones MCP si están activas) | Debe coincidir con `hipo stats --session` |
| hook p95 | `index.db`, tabla `hook_timings` (ver D-3) | Últimas 24 h del proyecto |
| precisión (7 días) | `AccessLog`: inyectados con `used = true` / inyectados | Ventana de 7 días |

### Recuerdos

| Columna | Cálculo |
| --- | --- |
| A | `activation.Score(memory, ctx)` del núcleo, con el contexto de la sesión seleccionada; sin sesión, `ctx` vacío (C = 0) |
| ▲ | `A ≥ activation.inject_threshold` |
| separador L1 | Entre la última fila con `A ≥ activation.index_threshold` y la primera por debajo |
| tipo, título, estado, usos | Frontmatter (`kind`, `title`, `status`, `uses`) |
| fuente | `source.agent` |

Límite: se calcula A para todos los recuerdos que pasan los filtros, pero se dibujan solo las filas visibles. Con 5,000 recuerdos el cálculo debe tardar menos de 100 ms (RNF-03); si tarda más, se muestra "calculando…" en el título del panel y la lista anterior sigue visible.

### Detalle

| Bloque | Fuente | Cálculo |
| --- | --- | --- |
| cabecera, cuerpo | Archivo Markdown del recuerdo | Se lee el archivo, no el índice, para mostrar el texto real |
| pistas, fuente | Frontmatter | — |
| ancla y deriva | `reconsolidate.Drift(memory)` del núcleo | Porcentaje de líneas cambiadas desde `anchor.commit`; veredicto según `drift_warn` y `drift_suspect`. Se calcula al seleccionar, en segundo plano (puede llamar a git) |
| enlaces | Frontmatter `links` + enlaces entrantes desde `index.db` | Muestra entrantes y salientes, con flecha |
| saliencia, confianza | Frontmatter | Barra 0–1 |
| desglose de activación | `activation.Explain(memory, ctx)` | Devuelve cada término; la TUI solo los muestra |
| historial | `AccessLog` + frontmatter + último evento de reconsolidación | — |

## 4. Red

| Dato | Fuente | Nota |
| --- | --- | --- |
| nodos y aristas | `index.db`, tabla de enlaces, búsqueda en anchura desde el nodo central hasta N saltos | Máximo 60 nodos dibujados; el resto se agrupa |
| color y estado | Frontmatter | — |
| A de cada nodo | `activation.Score` con el contexto actual | Para el brillo y el resumen de selección |

## 5. Tareas y agentes

| Dato | Fuente | Cálculo |
| --- | --- | --- |
| tareas | `prospective/` con `kind: intention` y `task_state` | Estado según diagrama 13 |
| dependencias | `depends_on` | Una tarea es `ready` si todas sus dependencias están `done` |
| lease | `live/leases.json` | Restante = `expires − ahora`; vencido si es negativo |
| agente de la tarea | Lease → sesión | — |
| fatiga | Sesión, campo `fatigue` (lo escribe el núcleo en cada `post_tool`) | Estado según `fatigue.tired`, `exhausted`, `must_sleep` |
| tokens de la sesión | Sesión, campo `tokens` | — |
| eventos | `live/events.jsonl` | Lectura incremental; se mantienen los últimos 2,000 en memoria |
| ámbitos cruzados | `scope` de tareas `claimed` | Intersección de globs (la misma función que usa `task claim`) |

## 6. Sueño

| Dato | Fuente |
| --- | --- |
| ciclos | Episodios `agent: sleep` (uno por ciclo), con su reporte del paso 9 |
| pasos y estado | Reporte del ciclo; pasos encolados en `live/pending_sleep.jsonl` |
| tokens del modelo local | Reporte del ciclo |
| commit | Reporte del ciclo (`m03`, etc.) |
| reglas propuestas | `status = 'proposed'` con `derived_from` |
| "por qué la propone" | Reporte del ciclo: tamaño del grupo, sesiones distintas, similitud media, contradicciones revisadas |
| dónde aparecerá | Simulación: `activation.Score` de la regla con los contextos de las 10 últimas sesiones; si entraría en L0 o L1 |

## 7. Métricas

Todas vienen de `stats.Compute(proyecto, desde, hasta)` del núcleo, el mismo que usa `hipo stats`. La TUI no calcula métricas propias.

| Métrica | Definición (del spec, sección Evaluación) |
| --- | --- |
| tokens de memoria por sesión | Mediana y p90 del total de la sesión, incluido el costo fijo |
| precisión de recuperación | Inyectados que el agente usó / inyectados |
| errores repetidos | Eventos de error cuyo recuerdo `error` ya existía y estaba activo |
| handoffs sin contexto adicional | Handoffs cuya sesión receptora no pidió `recall` del mismo tema en sus primeros 5 pasos |
| latencia del hook | p95 de `hook_timings` |

## 8. Dependencias del núcleo (lo que el núcleo debe exponer para la TUI)

Estas piezas no están detalladas en el spec v1.0 y la TUI las necesita. Deben entrar al spec antes del hito T2 (ver 10).

| ID | Dependencia | Motivo |
| --- | --- | --- |
| D-1 | Persistir cada sesión en `live/sessions/<session_id>.json` con `harness`, `model`, `branch`, `worktree`, `started`, `ended`, `tokens`, `fatigue`, ventana de pistas de contexto | Paneles Contexto y Agentes |
| D-2 | Tabla `injections(session_id, memory_id, layer, tokens, ts)` en `index.db`, escrita por los hooks al inyectar | H-12 y la precisión de recuperación |
| D-3 | Tabla `hook_timings(event, ms, ts)` en `index.db` | Latencia p95 |
| D-4 | Funciones de solo lectura: `activation.Score`, `activation.Explain`, `reconsolidate.Drift`, `stats.Compute`, `doctor.Check`, `tasks.ScopesOverlap` | Que la TUI no duplique cálculos |
| D-5 | El reporte del ciclo de sueño (paso 9) en formato estructurado: pasos, estado, tokens, commit, y para cada regla propuesta el tamaño del grupo, sesiones, similitud y contradicciones revisadas | Vista Sueño |
| D-6 | Operaciones de escritura del núcleo con verificación de versión: `memory.MarkSuspect`, `memory.Restore`, `memory.Forget`, `memory.Update`, `rules.Approve`, `rules.Reject`, `tasks.Release` | Acciones de la TUI (CW-2) |
| D-7 | `index.db` en modo WAL | Lectores sin bloquear al escritor (RNF-11) |
