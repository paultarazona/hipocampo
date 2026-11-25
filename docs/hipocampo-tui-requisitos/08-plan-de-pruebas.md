# 08 · Plan de pruebas

## 1. Niveles

| ID | Nivel | Qué prueba | Herramienta | Corre en |
| --- | --- | --- | --- | --- |
| P-01 | Unitarias de consultas | `internal/tui/query`: cada función devuelve lo esperado sobre fixtures | `go test` | CI, cada push |
| P-02 | Unitarias de vistas | `Update` de cada vista: dado un modelo y un mensaje (tecla, datos nuevos, tamaño), el modelo resultante es el esperado | `go test` | CI |
| P-03 | Snapshots | `View` de cada vista con un fixture fijo produce exactamente el texto guardado (archivo *golden*) | `go test` + `teatest` | CI |
| P-04 | Flujos de punta a punta | Secuencias de teclas sobre la TUI real con un almacén de prueba | `teatest` | CI |
| P-05 | Paridad de activación | A mostrada = `hipo recall --explain` con el mismo contexto, en los 2 decimales visibles | `go test` | CI |
| P-06 | Paridad de tokens | Total del panel Contexto = `hipo stats --session` | `go test` | CI |
| P-07 | Paridad de métricas | Métricas de la vista = `hipo stats --since` | `go test` | CI |
| P-08 | Escrituras | Cada acción de CW: confirmación, evento, commit, `source.agent: human`, conflicto de versión, modo `home` sin tocar el repo | `teatest` + inspección del almacén | CI |
| P-09 | Estabilidad de la red | Mismo vecindario → mismo dibujo en dos ejecuciones | Snapshot | CI |
| P-10 | Tamaños | Snapshots de cada vista en 150×46, 130×40, 110×32, 80×24, 59×19 | Snapshot | CI |
| P-11 | Color y contraste | Snapshots con `NO_COLOR`; validación de contraste de los tokens del tema | `go test` + script de contraste | CI |
| P-12 | Teclas y ayuda | Cada tecla del mapa (04) tiene efecto en su contexto y aparece en `?`; ninguna tecla sin efecto aparece en la ayuda | `go test` generado desde una tabla | CI |
| P-13 | Estados especiales | Un caso por cada EE-01 a EE-36 | `teatest` + fixtures | CI |
| P-14 | Rendimiento | RNF-01, 02, 03, 05 con el fixture `escala` | `go test -bench` | CI nocturno |
| P-15 | Concurrencia en vivo | Un proceso escribe eventos y ejecuta hooks mientras la TUI está abierta; se mide RNF-04 y RNF-11 | Prueba de integración | CI nocturno |
| P-16 | Reposo | CPU y RAM tras 10 min abierta (RNF-06) | Script con `ps` | Manual por release |
| P-17 | Matriz de terminales | Checklist manual (sección 5) en cada terminal de RNF-08 | Manual | Por release |
| P-18 | Sin red | Con la red bloqueada salvo `localhost:11434`, la TUI no intenta otras conexiones | Prueba de integración | CI nocturno |
| P-19 | Contenido hostil | Recuerdos con secuencias ANSI, caracteres de control, textos de 10,000 caracteres, secretos sin redactar | Snapshot | CI |

## 2. Fixtures

En `testdata/tui/`, cada fixture es un almacén completo (archivos + `index.db` + `live/`) generado por un script determinista (`go run ./testdata/tui/gen`), con reloj fijo en `2026-11-06T10:32:00-05:00`.

| Fixture | Contenido | Usado por |
| --- | --- | --- |
| `vacio` | Proyecto registrado sin recuerdos, sin sesiones | EE-01 a EE-10 |
| `basico` | Los datos de los mockups: 312 recuerdos, 2 sesiones, 6 tareas, 9 eventos, 4 ciclos, 2 reglas propuestas | P-03, P-04, P-05, P-06 |
| `escala` | 5,000 recuerdos, 20,000 eventos, 50 tareas, 200 sesiones | P-14, P-15 |
| `roto` | `index.db` corrupto, un frontmatter inválido, `events.jsonl` con líneas truncadas, `config.toml` inválido | EE-17 a EE-23 |
| `multiagente` | Dos sesiones y un generador que escribe eventos cada 200 ms | P-15, H-20 |
| `home` | Proyecto en modo `home` con su repo de cliente | P-08, RNF-24 |
| `hostil` | Contenido de P-19 | P-19 |

Ollama se simula con un servidor HTTP de prueba que puede responder, tardar o estar caído.

## 3. Snapshots

- Se generan con `teatest` en tamaño fijo y se comparan contra archivos *golden* en `internal/tui/<vista>/testdata/*.golden`.
- Se actualizan solo con `go test ./internal/tui/... -update` y el cambio se revisa en el PR como texto.
- Dos variantes por vista: con color (secuencias ANSI) y sin color (`NO_COLOR`), para revisar fácilmente el texto.
- Además, `vhs` puede grabar GIF de los flujos para la documentación; no forma parte de la verificación.

## 4. Flujos de punta a punta (P-04)

| Flujo | Pasos | Verificación |
| --- | --- | --- |
| F-01 Primera mirada | `hipo tui` → Resumen | Los 9 paneles con datos; foco en Recuerdos (H-01, H-05) |
| F-02 Entender una advertencia | Resumen → `tab` a Contexto → seleccionar advertencia → `enter` | Se abre el detalle con el desglose de activación ≥ 1.2 (H-12, H-11) |
| F-03 Seguir el linaje | Detalle → `l` → Red → `←` a un episodio → `enter` | Se abre el episodio con su sesión (H-16) |
| F-04 Aprobar una regla | `r` → Sueño → `a` → confirmar | La regla queda `active`, `validated_by: human`, commit nuevo; se muestra la siguiente (H-24) |
| F-05 Rechazar una regla | `r` → `x` → escribir confirmación | `forgotten` + evento; el sueño de prueba no la vuelve a proponer (H-24.4) |
| F-06 Marcar dudoso | Memoria → `d` → motivo → `enter` | `suspect`, A penalizada, evento (H-13) |
| F-07 Olvidar | Memoria → `g` → escribir `olvidar` | Archivo borrado, evento con id, selección en la siguiente fila (H-14) |
| F-08 Liberar lease | Tareas → tarea vencida → `u` → confirmar | `ready` con último checkpoint, evento `handoff` de `human` (H-21) |
| F-09 Cambiar de proyecto | `p` → filtrar → `enter` | Todas las vistas con el nuevo proyecto en ≤ 500 ms (H-07) |
| F-10 Buscar | `/` → `kind:error prisma` | Resultados en Memoria con su A (H-04) |
| F-11 Sin Ollama | Arrancar con Ollama caído | `Ollama ○`, Sueño con pasos encolados, `S` desactivado (H-28) |
| F-12 Terminal chica | Redimensionar a 80×24 durante F-02 | Vista compacta; la selección se conserva (H-29) |

## 5. Checklist manual por terminal (P-17)

Para cada terminal de RNF-08:

- [ ] Los marcos se dibujan sin huecos ni desalineación.
- [ ] Los iconos `▲ ▶ ◷ ○ ■ ✓ ●` se ven (si no, `--ascii` funciona).
- [ ] Los colores coinciden con los tokens (o caen bien a 256 / 16 colores).
- [ ] `tab`, `shift+tab`, flechas, `pgup` / `pgdn`, `home` / `end` funcionan.
- [ ] Redimensionar no deja restos en pantalla.
- [ ] `$EDITOR` se abre y la TUI vuelve intacta al cerrarlo.
- [ ] Al salir con `q` y con `ctrl+c`, la terminal queda como estaba (cursor visible, sin modo alternativo).

## 6. Criterio para dar por buena una versión

- Todas las pruebas de CI en verde, incluidas P-05 a P-07 (paridad con el CLI).
- Ninguna historia *Must* con criterios sin prueba (ver `matriz-trazabilidad.csv`).
- Checklist de P-17 completo en al menos Windows Terminal, iTerm2 y una terminal Linux.
- P-14 y P-15 dentro de los límites de RNF-01 a RNF-05 y RNF-11.
