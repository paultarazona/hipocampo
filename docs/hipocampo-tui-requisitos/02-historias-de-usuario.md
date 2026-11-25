# 02 · Historias de usuario y criterios de aceptación

29 historias en 8 épicas. Cada historia indica prioridad, vista y los diagramas del paquete de diagramas que la respaldan.

| Épica | Historias | Must | Should | Could |
| --- | --- | --- | --- | --- |
| E1 · Global y navegación | H-01 a H-05 | 4 | 1 | 0 |
| E2 · Proyectos | H-06 a H-08 | 2 | 1 | 0 |
| E3 · Memoria | H-09 a H-15 | 4 | 2 | 1 |
| E4 · Red de memoria | H-16 a H-17 | 1 | 1 | 0 |
| E5 · Tareas y agentes | H-18 a H-22 | 3 | 2 | 0 |
| E6 · Sueño | H-23 a H-25 | 2 | 0 | 1 |
| E7 · Métricas | H-26 a H-27 | 0 | 1 | 1 |
| E8 · Robustez | H-28 a H-29 | 2 | 0 | 0 |
| **Total** | **29** | **18** | **8** | **3** |

**Criterios comunes a toda acción que escribe** (aplican a H-13, H-14, H-15, H-21, H-24, H-25 aunque no se repitan):

- **CW-1** La acción abre un modal de confirmación que dice exactamente qué va a cambiar. `enter` confirma, `esc` cancela. Sin confirmación no se escribe nada.
- **CW-2** La escritura pasa por el núcleo (no por la TUI) y queda registrada con `source.agent: human` y un evento en `live/events.jsonl`.
- **CW-3** Al terminar, la TUI muestra un aviso de una línea con el resultado y refresca la vista afectada.
- **CW-4** Si la escritura falla (lock, conflicto de versión, disco), el aviso muestra la causa y la vista no cambia.
- **CW-5** Ninguna acción se ejecuta con una sola tecla accidental: las destructivas (olvidar, rechazar) piden escribir `s` o confirmar dos veces (ver H-14).

---

## E1 · Global y navegación

### H-01 · Abrir la TUI en el proyecto actual
**Must** · Todas las vistas · Diagramas 01, 12

Como desarrollador, quiero abrir la TUI con `hipo tui` desde la carpeta de mi repo, para ver de inmediato la memoria de ese proyecto.

- **H-01.1** Dado que estoy dentro de un repo registrado, cuando ejecuto `hipo tui`, entonces se abre la vista Resumen de ese proyecto.
- **H-01.2** Dado que estoy en un worktree del repo (por ejemplo `../wt-T12`), cuando ejecuto `hipo tui`, entonces se abre el mismo proyecto (se resuelve por `git rev-parse --git-common-dir` o por el id del primer commit).
- **H-01.3** Dado que estoy fuera de cualquier repo registrado, cuando ejecuto `hipo tui`, entonces se abre la vista de Proyectos sin ninguno seleccionado.
- **H-01.4** Cuando ejecuto `hipo tui --project <id|nombre>`, entonces se abre ese proyecto sin importar la carpeta actual.
- **H-01.5** Cuando ejecuto `hipo tui --view <vista>`, entonces se abre directamente esa vista (`resumen`, `memoria`, `red`, `tareas`, `sueno`, `metricas`).
- **H-01.6** El primer cuadro aparece en menos de 300 ms con 5,000 recuerdos (RNF-01).

### H-02 · Cambiar de vista con el teclado
**Must** · Global · Mockups tui-01 a tui-03

Como desarrollador, quiero cambiar entre vistas con una tecla, para moverme sin perder el contexto.

- **H-02.1** Cuando presiono `1` a `6`, entonces se abre la vista correspondiente y su pestaña queda resaltada en la segunda línea.
- **H-02.2** Dado que tenía un recuerdo seleccionado en Memoria, cuando cambio a Red, entonces la red se centra en ese recuerdo.
- **H-02.3** Dado que vuelvo a una vista, entonces conserva la selección, el scroll y los filtros que tenía.
- **H-02.4** Cuando presiono `tab` / `shift+tab`, entonces el foco pasa al panel siguiente / anterior de la vista, y el panel con foco tiene el borde resaltado.
- **H-02.5** Cuando presiono `esc` en una vista sin modal abierto, entonces vuelve a la vista anterior (historial de navegación, máximo 20 pasos).

### H-03 · Ver ayuda contextual
**Must** · Global

Como usuario nuevo, quiero ver qué teclas existen en la vista actual, para no memorizarlas.

- **H-03.1** Cuando presiono `?`, entonces se abre un modal con las teclas globales y las de la vista y panel actuales, agrupadas.
- **H-03.2** La barra inferior siempre muestra entre 6 y 9 teclas relevantes de la vista actual.
- **H-03.3** Cada tecla listada en la ayuda funciona; cada tecla que funciona está listada (se verifica con P-12).

### H-04 · Buscar en la memoria
**Should** · Global → Memoria · Diagrama 06 (FTS5)

Como desarrollador, quiero buscar por texto en todos los recuerdos del proyecto, para encontrar algo que recuerdo a medias.

- **H-04.1** Cuando presiono `/`, entonces aparece una línea de búsqueda en la parte inferior con el cursor activo.
- **H-04.2** Dado que escribo al menos 2 caracteres, entonces los resultados se actualizan mientras escribo (con 150 ms de espera tras la última tecla), usando FTS5 sobre título, resumen y cuerpo.
- **H-04.3** Los resultados se muestran en la vista Memoria, ordenados por relevancia de texto, con la activación actual visible en su columna.
- **H-04.4** Admite prefijos: `kind:error`, `status:suspect`, `path:prisma/**`, `agent:codex`. Se pueden combinar con texto libre.
- **H-04.5** Dado que no hay resultados, entonces se muestra "Sin resultados para «…»" y una sugerencia de quitar filtros.
- **H-04.6** `esc` cierra la búsqueda y restaura la lista anterior.

### H-05 · Ver el estado global en la cabecera
**Must** · Global · Mockup tui-01

Como desarrollador, quiero ver de un vistazo en qué proyecto estoy y si todo funciona, para confiar en lo que muestra la pantalla.

- **H-05.1** La primera línea muestra: nombre del proyecto, modo (`repo` / `home`), id corto (6 caracteres), estado de Ollama, número de agentes con lease activo y la hora local.
- **H-05.2** El estado de Ollama es `●` verde si responde, `●` amarillo si responde pero falta algún modelo configurado, `○` gris si no responde. Se comprueba cada 30 s, nunca en el hilo de dibujo.
- **H-05.3** Dado que el almacén tiene problemas detectados por `doctor` (conflictos, leases vencidos, índice desactualizado), entonces aparece un indicador `!` con el número de problemas, que abre la lista al presionar `!`.

---

## E2 · Proyectos

### H-06 · Ver todos mis proyectos
**Must** · Resumen (panel Proyectos) · Diagrama 12

Como desarrollador con varios repos, quiero ver todos mis proyectos con memoria, para saber dónde hay actividad.

- **H-06.1** El panel Proyectos lista todos los proyectos de `~/.hipocampo/projects.json` con nombre, número de recuerdos activos y modo.
- **H-06.2** El orden es por última actividad (último evento en su pizarra), el más reciente arriba.
- **H-06.3** Los proyectos en modo `home` se distinguen con su etiqueta en otro color, para no confundir repos propios con los de clientes.
- **H-06.4** Dado que la ruta de un proyecto ya no existe, entonces se muestra con `✕ ruta no encontrada` y no se puede abrir, pero no desaparece de la lista.
- **H-06.5** Debajo de la lista se muestra el total de proyectos y de recuerdos.

### H-07 · Cambiar de proyecto
**Must** · Resumen (panel Proyectos)

Como desarrollador, quiero cambiar de proyecto sin cerrar la TUI, para revisar varios repos seguidos.

- **H-07.1** Dado que el foco está en Proyectos, cuando muevo con `↑↓` y presiono `enter`, entonces todas las vistas pasan a mostrar ese proyecto.
- **H-07.2** Cuando presiono `p` desde cualquier vista, entonces se abre un selector rápido de proyectos con filtro por nombre.
- **H-07.3** Al cambiar de proyecto se cierran las conexiones al índice anterior y se abren las del nuevo; no quedan watchers del proyecto anterior.
- **H-07.4** El cambio tarda menos de 500 ms (RNF-02).

### H-08 · Ver la salud del proyecto
**Should** · Resumen (panel Sistemas) · Diagrama 07

Como desarrollador, quiero saber si la memoria de un proyecto tiene problemas, para corregirlos antes de que confundan a un agente.

- **H-08.1** El panel Sistemas muestra el conteo de recuerdos por sistema (episódica, semántica, procedural, prospectiva, archivo) con una barra proporcional.
- **H-08.2** Muestra cuántos recuerdos están `suspect`, cuántos conflictos de decisión hay abiertos, cuándo fue el último sueño y cuántas reglas esperan revisión.
- **H-08.3** Cada uno de esos números es navegable: al seleccionarlo y presionar `enter`, abre la vista Memoria filtrada por ese criterio (o Sueño, para las reglas).
- **H-08.4** Dado que los recuerdos semánticos activos superan el 90 % del tope `limits.max_semantic_rules`, entonces aparece un aviso amarillo.

---

## E3 · Memoria

### H-09 · Ver recuerdos ordenados por activación
**Must** · Resumen y Memoria (panel Recuerdos) · Diagramas 03, 09

Como desarrollador, quiero ver qué recuerdos están más activos en el contexto actual, para entender qué está "pensando" la memoria.

- **H-09.1** La lista muestra por fila: activación A con 2 decimales, marca `▲` si A ≥ `activation.inject_threshold`, tipo (con color de su sistema), título, estado y usos.
- **H-09.2** El orden por defecto es A descendente, calculada con el **contexto de la sesión seleccionada** (o sin contexto si no hay sesión, mostrándolo en el filtro).
- **H-09.3** Una línea separadora marca el umbral `activation.index_threshold`; las filas por debajo se ven atenuadas con la leyenda "bajo el umbral L1: no se muestran al agente".
- **H-09.4** Los recuerdos `superseded` y `archived` no aparecen salvo que se active su filtro; `suspect` aparecen con su estado en amarillo.
- **H-09.5** El pie del panel muestra "N recuerdos · M visibles" y las teclas de filtro y orden.
- **H-09.6** Cuando presiono `s`, entonces el orden alterna entre A, fecha de creación, último uso y saliencia; el criterio activo se muestra en el título del panel.
- **H-09.7** La activación mostrada coincide con la de `hipo recall` con el mismo contexto, al menos en los 2 decimales visibles (P-05).

### H-10 · Filtrar recuerdos
**Must** · Memoria

Como desarrollador, quiero filtrar por tipo, estado, pista, agente o fecha, para aislar lo que me interesa.

- **H-10.1** Cuando presiono `f`, entonces se abre un panel de filtros con: tipo (`kind`), estado, sistema, agente de origen, rango de fechas, pista (`path`, `symbol`, `tag`) y "solo validados por humano".
- **H-10.2** Los filtros activos se muestran como etiquetas en la línea de filtro del panel; `x` sobre una etiqueta la quita.
- **H-10.3** Cuando presiono `t`, entonces alterna rápidamente el filtro de tipo entre todos, `error`, `decision`, `solution`, `procedure`, `fact`, `episode`, `intention`.
- **H-10.4** Cuando presiono `c` en la vista Memoria, entonces alterna entre "contexto de la sesión seleccionada" y "sin contexto" para el cálculo de A.
- **H-10.5** Los filtros se guardan por proyecto en `~/.hipocampo/tui.toml` y se restauran al volver.

### H-11 · Ver el detalle de un recuerdo
**Must** · Resumen y Memoria (panel Detalle) · Diagramas 06, 08, 09

Como desarrollador, quiero ver todo lo que se sabe de un recuerdo, para decidir si confiar en él.

- **H-11.1** El panel Detalle muestra: tipo e id, estado, título, resumen y los primeros párrafos del cuerpo.
- **H-11.2** Muestra las pistas (`paths`, `symbols`, `tags`), la fuente (agente, modelo, validado por) y el ancla (commit corto y estado de deriva: porcentaje y veredicto `sin deriva` / `cambió` / `suspect` según `reconsolidation.drift_warn` y `drift_suspect`).
- **H-11.3** Muestra los enlaces con su relación y el título del recuerdo destino; `enter` sobre un enlace abre ese recuerdo.
- **H-11.4** Muestra saliencia y confianza como barra y número.
- **H-11.5** Muestra el desglose de la activación: `B`, `S`, `2·C`, `P`, `ln(conf)`, penalización y total, con los mismos pesos de `config.toml`. La suma de los términos es igual al total mostrado.
- **H-11.6** Muestra el historial: creación, número de usos, último uso, última reconsolidación y su resultado.
- **H-11.7** Cuando presiono `v`, entonces se abre el cuerpo completo en un visor con scroll; cuando presiono `o`, entonces se abre el archivo en `$EDITOR` en modo solo lectura (ver H-15 para editar).
- **H-11.8** Dado que el recuerdo es de tipo `error`, `decision`, `solution`, `procedure` o `intention`, entonces muestra también sus campos propios (síntoma y causa; elegida y descartadas; pasos y éxitos; disparador y siguiente paso).

### H-12 · Ver lo que se inyectó en una sesión
**Must** · Resumen (panel Contexto) · Diagramas 04, 10

Como desarrollador, quiero ver qué memoria recibió mi agente en la sesión activa, para entender por qué actuó así y corregir la memoria si hace falta.

- **H-12.1** Dado que hay una sesión activa, cuando abro el Resumen, entonces el panel Contexto muestra el agente, la rama, los archivos tocados recientemente y los comandos recientes.
- **H-12.2** Muestra lo inyectado por capa: L0, L1, semilla de despertar (si hubo) y advertencias proactivas, cada una con su número de elementos y tokens.
- **H-12.3** Dado que se inyectó una advertencia, cuando la selecciono y presiono `enter`, entonces se abre el detalle de ese recuerdo.
- **H-12.4** Muestra el total de tokens de memoria de la sesión, la latencia p95 del hook y la precisión de recuperación de los últimos 7 días.
- **H-12.5** El total de tokens coincide con el de `hipo stats` para esa sesión (P-06).
- **H-12.6** Dado que hay varias sesiones activas, cuando presiono `[` / `]`, entonces cambia la sesión mostrada; el título del panel indica cuál.
- **H-12.7** Dado que no hay sesiones activas, entonces el panel dice "sin sesión activa" y muestra los datos de la última sesión cerrada, marcados como tales.

### H-13 · Marcar un recuerdo como dudoso
**Should** · Memoria (Detalle) · Diagrama 07 · Aplica CW-1 a CW-4

Como desarrollador, quiero marcar un recuerdo como dudoso cuando sé que está mal, para que deje de inyectarse mientras lo reviso.

- **H-13.1** Cuando presiono `d` sobre un recuerdo `active`, entonces se abre un modal que pide un motivo (texto, obligatorio, máximo 200 caracteres).
- **H-13.2** Al confirmar, el núcleo pone `status: suspect` y guarda el motivo; el recuerdo aparece en amarillo y su A refleja la penalización.
- **H-13.3** Cuando presiono `d` sobre un recuerdo `suspect`, entonces se ofrece "volver a active", que también pide confirmación.

### H-14 · Olvidar un recuerdo
**Should** · Memoria (Detalle) · Diagrama 07 · Aplica CW-1 a CW-5

Como desarrollador, quiero borrar definitivamente un recuerdo incorrecto o peligroso, para que no vuelva a aparecer.

- **H-14.1** Cuando presiono `g`, entonces se abre un modal en rojo que explica que el borrado es definitivo, que queda solo un evento `forgotten` con el id, y que el contenido sigue en el historial git del almacén.
- **H-14.2** Para confirmar hay que escribir `olvidar` y presionar `enter`.
- **H-14.3** Dado que el recuerdo es la única fuente (`derived_from`) de una regla activa, entonces el modal lo advierte y lista las reglas afectadas.
- **H-14.4** Tras olvidar, la selección pasa al recuerdo siguiente de la lista.

### H-15 · Editar un recuerdo
**Could** · Memoria (Detalle) · Aplica CW-1 a CW-4

Como desarrollador, quiero corregir el texto de un recuerdo, para no tener que olvidarlo y crearlo de nuevo.

- **H-15.1** Cuando presiono `e`, entonces se abre el archivo del recuerdo en `$EDITOR` (o `vi` si no está definido) y la TUI se suspende.
- **H-15.2** Al cerrar el editor, el núcleo valida el frontmatter contra el esquema; si no es válido, se muestra el error y se ofrece volver a editar o descartar.
- **H-15.3** Si es válido, se guarda como nueva versión con `source.validated_by: human` y un commit del almacén.
- **H-15.4** Si otro proceso modificó el archivo mientras se editaba, no se sobrescribe: se muestra el conflicto y se ofrece abrir ambas versiones.

---

## E4 · Red de memoria

### H-16 · Explorar el vecindario de un recuerdo
**Must** · Red · Mockup tui-02, diagramas 06, 08

Como desarrollador, quiero ver con qué se conecta un recuerdo, para entender de dónde salió y qué produjo.

- **H-16.1** La vista Red muestra el recuerdo seleccionado al centro y sus vecinos hasta N saltos (por defecto 2), como cajas conectadas por líneas con la relación escrita.
- **H-16.2** Cada caja muestra tipo y título; el borde usa el color del sistema; los `suspect` en amarillo; los archivados atenuados.
- **H-16.3** Las flechas indican la dirección del enlace (`solves`, `derived_from`, `supersedes`, `causes`, `relates`).
- **H-16.4** Cuando muevo con las flechas, entonces la selección salta al vecino más cercano en esa dirección; `enter` abre el detalle; `c` centra la red en el seleccionado.
- **H-16.5** `+` / `-` cambian los saltos entre 1 y 3.
- **H-16.6** El panel lateral muestra leyenda, filtros activos y un resumen del nodo seleccionado (tipo, A, enlaces, fuente, ancla).
- **H-16.7** El diseño de la red es estable: el mismo vecindario se dibuja igual en dos aperturas seguidas (P-09).

### H-17 · Filtrar y agrupar la red
**Should** · Red

Como investigador, quiero filtrar la red por sistema o pista y agrupar cuando hay muchos nodos, para que siga siendo legible.

- **H-17.1** Los filtros de la red (sistemas, mostrar suspect, mostrar archivados, pista) se cambian desde el panel lateral con `espacio`.
- **H-17.2** Dado que el vecindario tiene más nodos de los que caben, entonces se agrupan por tipo en cajas "N episodios" que se expanden con `enter`.
- **H-17.3** Cuando presiono `z`, entonces se agrupan por pista (por ejemplo, todos los de `prisma/**`).
- **H-17.4** El pie muestra cuántos nodos y enlaces hay visibles.

---

## E5 · Tareas y agentes

### H-18 · Ver los agentes activos
**Must** · Resumen y Tareas (panel Agentes) · Diagramas 10, 11

Como desarrollador, quiero ver qué agentes trabajan ahora, en qué tarea y qué tan cansados están, para decidir si intervenir.

- **H-18.1** Cada agente con sesión abierta muestra: harness, modelo, tarea con lease, tiempo restante del lease, worktree y tokens de la sesión.
- **H-18.2** Muestra la fatiga F como barra y número, con el estado (`despierto`, `cansado`, `agotado`, `debe dormir`) según los umbrales de `config.toml`, y el color correspondiente.
- **H-18.3** Dado que un lease vence en menos de 5 minutos sin checkpoint, entonces el tiempo restante aparece en amarillo.
- **H-18.4** Se actualiza en vivo (RNF-04) sin que el usuario haga nada.
- **H-18.5** Muestra las tareas `ready` sin agente con `○`.

### H-19 · Ver las tareas y sus dependencias
**Must** · Resumen y Tareas · Diagrama 13

Como desarrollador, quiero ver todas las tareas con su estado y de qué dependen, para saber qué falta y qué está bloqueado.

- **H-19.1** La lista muestra por tarea: id, icono y estado (`done ✓`, `claimed ▶`, `pending ◷`, `ready ○`, `blocked ■`), título y agente o dependencias.
- **H-19.2** En la vista Tareas, `g` alterna entre lista y grafo de dependencias (DAG dibujado con cajas y flechas, de izquierda a derecha).
- **H-19.3** Al seleccionar una tarea se muestra su detalle: ámbito (`scope`), rol, siguiente paso, último checkpoint (commit y hora), preguntas abiertas del handoff y eventos de esa tarea.
- **H-19.4** Las tareas `blocked` muestran el motivo y las decisiones en conflicto, navegables a su detalle.
- **H-19.5** Dado que dos tareas `claimed` tienen ámbitos que se cruzan (no debería pasar), entonces se marcan en rojo y aparecen en el indicador de problemas (H-05.3).

### H-20 · Ver la pizarra de eventos en vivo
**Must** · Resumen y Tareas (panel Pizarra) · Diagrama 11

Como desarrollador, quiero ver los eventos de coordinación a medida que ocurren, para seguir el trabajo de varios agentes.

- **H-20.1** El panel muestra los eventos más recientes de `live/events.jsonl`, el más nuevo arriba, con hora, autor y mensaje.
- **H-20.2** El color depende del tipo: decisión (semántica), aviso de Hipocampo a un agente (acento), advertencia (amarillo), rechazo o conflicto (rojo), done (verde).
- **H-20.3** Los eventos nuevos aparecen sin recargar la vista en menos de 1 s desde que se escriben (RNF-04).
- **H-20.4** En la vista Tareas el panel ocupa más alto, admite scroll y filtro por agente o tarea con `f`.
- **H-20.5** Dado que el usuario está leyendo eventos antiguos (scroll hacia abajo), entonces los nuevos no le mueven la vista; aparece un aviso "N eventos nuevos ↑".

### H-21 · Liberar un lease vencido
**Should** · Tareas · Diagrama 13 · Aplica CW-1 a CW-4

Como desarrollador, quiero liberar una tarea cuyo agente se cayó, para que otro la tome sin esperar.

- **H-21.1** Dado que una tarea `claimed` tiene el lease vencido, cuando la selecciono y presiono `u`, entonces se ofrece liberarla.
- **H-21.2** Al confirmar, la tarea vuelve a `ready` con su último checkpoint, y se escribe un evento `handoff` con autor `human`.
- **H-21.3** Dado que el lease aún no venció, entonces `u` muestra cuánto falta y pide una confirmación adicional explicando que el agente podría seguir trabajando.

### H-22 · Recibir aviso de fatiga alta
**Should** · Global · Diagrama 10

Como desarrollador, quiero enterarme cuando un agente está agotado, para cerrar su sesión antes de que empeore.

- **H-22.1** Dado que la fatiga de una sesión cruza `fatigue.exhausted`, entonces aparece un aviso no bloqueante en la parte inferior durante 8 s, en cualquier vista.
- **H-22.2** Dado que cruza `fatigue.must_sleep`, entonces el aviso queda fijo hasta que el usuario lo descarte con `esc` o la sesión se cierre.
- **H-22.3** El aviso incluye si ya se escribió la semilla de despertar y su ruta.

---

## E6 · Sueño

### H-23 · Ver los ciclos de sueño
**Must** · Sueño · Mockup tui-03, diagrama 05

Como desarrollador, quiero ver cuándo durmió la memoria y qué cambió, para entender por qué ahora sabe algo nuevo.

- **H-23.1** La lista de ciclos muestra fecha, disparador (3 sesiones, 24 h o manual) y resumen (reglas, procedimientos, archivados, conflictos).
- **H-23.2** Al seleccionar un ciclo se muestran sus 9 pasos con estado (`✓`, `⏸ encolado`, `✕ error`) y si usaron modelo local o no.
- **H-23.3** Muestra los tokens que usó el modelo local frente al presupuesto `sleep.llm_token_budget`, y el commit del almacén.
- **H-23.4** Muestra los otros cambios del ciclo: procedimientos nuevos, recuerdos superseded, nuevos suspect, archivados y comprimidos; cada fila es navegable.
- **H-23.5** Dado que hay pasos encolados por falta de Ollama, entonces se indica cuántos y desde cuándo.
- **H-23.6** El panel Sueño del Resumen muestra el último ciclo, cuándo toca el próximo y cuántas reglas esperan revisión.

### H-24 · Revisar las reglas propuestas
**Must** · Sueño · Mockup tui-03, diagramas 05, 07, 08 · Aplica CW-1 a CW-5

Como desarrollador, quiero aprobar o rechazar las reglas que propone el sueño viendo de dónde salieron, para que solo lleguen a los agentes reglas correctas.

- **H-24.1** Cuando presiono `r` desde cualquier vista, entonces se abre la vista Sueño en la primera regla `proposed`.
- **H-24.2** Cada regla muestra: tipo, estado, confianza y saliencia iniciales, el texto de la regla, por qué el sueño la propone (episodios, sesiones, similitud, soluciones relacionadas, contradicciones), la lista `derived_from` navegable, las pistas y dónde aparecerá si se aprueba (L0, sección de `AGENTS.md`).
- **H-24.3** `a` aprueba: la regla pasa a `active` con `validated_by: human`; se hace commit del almacén; se pasa a la siguiente.
- **H-24.4** `x` rechaza: pide confirmación y un motivo opcional; la regla pasa a `forgotten` (evento con id, sin contenido), para que el sueño no la vuelva a proponer.
- **H-24.5** `e` abre la regla en `$EDITOR`; al guardar y validar, se aprueba con el texto editado.
- **H-24.6** `n` / `N` pasan a la regla siguiente / anterior sin decidir. El título del panel dice "Regla k de m".
- **H-24.7** Dado que no hay reglas propuestas, entonces la vista lo dice y muestra el último ciclo.
- **H-24.8** Dado que la regla contradice una decisión activa, entonces se muestra la decisión en conflicto en rojo antes de los botones.

### H-25 · Lanzar un ciclo de sueño manual
**Could** · Sueño · Diagrama 05 · Aplica CW-1 a CW-4

Como desarrollador, quiero ejecutar el sueño cuando lo necesito, para consolidar después de una sesión larga.

- **H-25.1** Cuando presiono `S` (mayúscula), entonces se ejecuta primero `hipo sleep --dry-run` y se muestra qué haría (reglas, procedimientos, archivados) sin escribir nada.
- **H-25.2** Al confirmar, se ejecuta el ciclo real en segundo plano; la TUI sigue usable y muestra el progreso por paso.
- **H-25.3** Dado que ya hay un ciclo en curso, entonces `S` muestra su progreso en lugar de lanzar otro.

---

## E7 · Métricas

### H-26 · Ver si la memoria funciona
**Should** · Métricas · Spec v1.0, sección Evaluación

Como investigador, quiero ver las métricas de la memoria en el tiempo, para saber si ayuda o estorba.

- **H-26.1** La vista muestra, para el rango elegido (7, 30 o 90 días): tokens de memoria por sesión (mediana y p90), precisión de recuperación, errores repetidos, handoffs completados sin contexto adicional y latencia p95 del hook.
- **H-26.2** Cada métrica se muestra como número grande, variación frente al periodo anterior y una línea de tendencia en caracteres (sparkline).
- **H-26.3** Cada métrica muestra su meta v1.0 del spec y si se cumple (`✓` / `✕`), con texto, no solo color.
- **H-26.4** Una tabla por agente y modelo muestra sesiones, tokens medios, fatiga media y handoffs.
- **H-26.5** `←` / `→` cambian el rango; los valores coinciden con `hipo stats --since` (P-07).

### H-27 · Exportar métricas
**Could** · Métricas

Como investigador, quiero exportar las métricas, para analizarlas fuera.

- **H-27.1** Cuando presiono `E`, entonces se escribe un CSV en la carpeta actual con las métricas del rango, y el aviso muestra la ruta.
- **H-27.2** El CSV usa los mismos nombres de columnas que `hipo stats --format csv`.

---

## E8 · Robustez

### H-28 · Usar la TUI sin Ollama
**Must** · Todas · Spec v1.0, sección Modelos locales

Como desarrollador, quiero que la TUI funcione aunque Ollama esté apagado, para no depender de él para revisar la memoria.

- **H-28.1** Dado que Ollama no responde, entonces todas las vistas abren y muestran sus datos; la cabecera indica `Ollama ○`.
- **H-28.2** La búsqueda usa solo FTS5 y lo indica ("búsqueda de texto; semántica no disponible").
- **H-28.3** La vista Sueño muestra los pasos encolados y desactiva `S` con una explicación.
- **H-28.4** La TUI nunca espera a Ollama para dibujar: todas las comprobaciones tienen tiempo máximo y corren en segundo plano.

### H-29 · Usar la TUI en terminales pequeñas o sin color
**Must** · Todas · RNF-06 a RNF-09

Como desarrollador que trabaja por SSH o en una terminal partida, quiero que la TUI siga siendo usable, para no depender de una pantalla grande.

- **H-29.1** Con 150×46 o más se muestra el diseño completo de tres columnas.
- **H-29.2** Entre 100×30 y 149×45 se usa el diseño de dos columnas definido en 03; ningún texto se sale de su panel.
- **H-29.3** Por debajo de 100×30 se muestra un panel por vez, con `tab` para rotar, y un aviso en la cabecera.
- **H-29.4** Por debajo de 60×20 se muestra solo el mensaje "La terminal es muy pequeña (mínimo 60×20)", sin errores.
- **H-29.5** Con `NO_COLOR` definida, o con `--no-color`, la TUI no emite colores; los estados se distinguen por iconos y texto (`▲`, `■`, `✓`, `[suspect]`).
- **H-29.6** Al redimensionar la terminal, el diseño se recalcula en el siguiente cuadro sin perder selección ni scroll.
