# Diagramas de Hipocampo (spec v1.0)

SVG independientes, con fondo propio, listos para el repo (`docs/diagramas/`), el README o una presentación.

| Archivo | Qué muestra |
| --- | --- |
| `01-arquitectura.svg` | Agentes → canales (hooks, CLI, MCP, UI) → núcleo Go → almacenamiento local |
| `02-sistemas-de-memoria.svg` | Cada estructura de la mente y su componente equivalente en Hipocampo |
| `03-ciclo-de-vida-del-recuerdo.svg` | Codificación, sueño, recuperación, reconsolidación y olvido |
| `04-flujo-hook-pre-tool.svg` | Secuencia completa de un hook antes de usar una herramienta |
| `05-proceso-de-sueno.svg` | Los 9 pasos del sueño, cuáles usan el modelo local y qué produce |
| `06-modelo-de-datos.svg` | Entidades, campos, relaciones y dónde se guarda cada una |
| `07-estados-del-recuerdo.svg` | Máquina de estados: proposed, active, suspect, superseded, archived, forgotten |
| `08-trazabilidad.svg` | Linaje de un recuerdo: sesión → evento → episodio → regla/procedimiento, con commits |
| `09-activacion.svg` | Curva de la activación base y desglose de la fórmula en tres contextos |
| `10-fatiga-de-sesion.svg` | Fatiga a lo largo de una sesión, umbrales, acciones y semilla de despertar |
| `11-coordinacion-multiagente.svg` | Dos agentes sobre el mismo flujo vía la pizarra: claims, leases, avisos |
| `12-almacenamiento.svg` | Modo repo vs modo home, worktrees, sincronización e identidad del proyecto |
| `13-estados-de-tarea.svg` | Máquina de estados de una tarea: pending, ready, claimed, blocked, done |

Los valores numéricos (umbrales, pesos, presupuestos) son los de `config.toml` en el spec v1.0.
Las curvas de los diagramas 09 y 10 son ilustrativas; 09 se calcula con la aproximación estándar de ACT-R (d = 0.5).

Fuente: los diagramas se generan con `gen/` (Python, sin dependencias). Para cambiar un valor, edita el script y vuelve a correr `python3 run.py d_part1 d_part2 d_part3`.

## Cliente TUI (mockup MVP)

| Archivo | Qué muestra |
| --- | --- |
| `tui/tui-01-resumen.svg` | Pantalla principal: proyectos, sistemas de memoria, recuerdos por activación, detalle, agentes, tareas, pizarra y sueño |
| `tui/tui-02-red.svg` | Red de memoria: vecindario de un recuerdo a 2 saltos, con leyenda y filtros |
| `tui/tui-03-sueno.svg` | Revisión del sueño: aprobar, rechazar o editar las reglas propuestas |

Datos de ejemplo. Para regenerarlos: `python3 gen/tui_screens.py`.
