# 03 · Pantallas y navegación

## 1. Estructura común

Toda vista comparte cuatro franjas fijas:

```
fila 0       cabecera: ◆ HIPOCAMPO · proyecto · modo · id · estado global        (H-05)
fila 1       pestañas: 1 Resumen  2 Memoria  3 Red  4 Tareas  5 Sueño  6 Métricas (H-02)
filas 2…n-2  cuerpo de la vista (paneles)
fila n-1     barra de teclas de la vista · indicador de estado a la derecha       (H-03)
```

Encima del cuerpo pueden aparecer, por orden de prioridad: **modales** (bloquean la vista), **línea de búsqueda** (fila n-2) y **avisos** (una línea sobre la barra de teclas, desaparecen solos salvo los fijos).

## 2. Inventario de vistas

| Tecla | Vista | Para qué | Paneles | Historias | Referencia |
| --- | --- | --- | --- | --- | --- |
| `1` | Resumen | Ver todo de un vistazo | Proyectos, Sistemas, Contexto, Recuerdos, Detalle, Agentes, Tareas, Pizarra, Sueño | H-05 a H-09, H-11, H-12, H-18 a H-20, H-23.6 | Mockup tui-01 |
| `2` | Memoria | Buscar, filtrar y revisar recuerdos | Filtros, Recuerdos, Detalle | H-04, H-09 a H-15 | Diagramas 06, 07, 09 |
| `3` | Red | Navegar enlaces entre recuerdos | Red, Leyenda y filtros | H-16, H-17 | Mockup tui-02, diagrama 08 |
| `4` | Tareas | Coordinación multiagente | Agentes, Tareas (lista o grafo), Detalle de tarea, Pizarra | H-18 a H-21 | Diagramas 11, 13 |
| `5` | Sueño | Ciclos y revisión de reglas | Ciclos, Regla propuesta, Otros cambios | H-23 a H-25 | Mockup tui-03, diagrama 05 |
| `6` | Métricas | Saber si la memoria funciona | Tarjetas de métricas, Tabla por agente | H-26, H-27 | Spec v1.0, Evaluación |

## 3. Diseño por vista

Las medidas están en columnas (c) y filas (f) para el diseño completo de 150×46. La sección 4 define cómo se adaptan.

### 3.1 Resumen (`1`)

```
┌ Proyectos 34c ┐┌ Recuerdos · por activación 68c ──────┐┌ Agentes 48c ─────┐
│ (11 f)        ││ (22 f)                                ││ (12 f)           │
├ Sistemas ─────┤│                                       │├ Tareas ──────────┤
│ (12 f)        │├ Detalle ──────────────────────────────┤│ (11 f)           │
├ Contexto ─────┤│ (21 f)                                │├ Pizarra ─────────┤
│ (20 f)        ││                                       ││ (13 f)           │
│               ││                                       │├ Sueño ───────────┤
└───────────────┘└───────────────────────────────────────┘└ (7 f) ───────────┘
```

| Panel | Contenido mínimo | Foco por defecto |
| --- | --- | --- |
| Proyectos | Lista de proyectos, total, teclas | No |
| Sistemas | 5 sistemas con barra; suspect, conflictos, último sueño, reglas por revisar | No |
| Contexto | Sesión seleccionada: rama, archivos, comandos; inyectado por capa con tokens; total, p95, precisión | No |
| Recuerdos | Top por activación en el contexto de la sesión; separador del umbral L1 | **Sí** |
| Detalle | Recuerdo seleccionado en Recuerdos (versión compacta de 3.2) | No |
| Agentes | Sesiones abiertas con lease y fatiga | No |
| Tareas | Lista compacta de tareas (máx. 6 filas, la más urgente arriba) | No |
| Pizarra | Últimos 9 eventos | No |
| Sueño | Último ciclo, próximo, reglas por revisar, estado de Ollama | No |

### 3.2 Memoria (`2`)

```
┌ Filtros 30c ──┐┌ Recuerdos 70c ────────────────────────┐┌ Detalle 48c ─────┐
│ tipo          ││ A ▲ tipo título estado usos fuente    ││ completo (H-11)  │
│ estado        ││ …                                     ││                  │
│ sistema       ││ ─ bajo el umbral L1 ─                 ││                  │
│ agente        ││ …                                     ││                  │
│ fechas        ││                                       ││                  │
│ pistas        ││                                       ││                  │
└───────────────┘└ N recuerdos · M visibles · orden ─────┘└──────────────────┘
```

- La lista agrega la columna `fuente` (agente) frente a la del Resumen.
- El panel Filtros se oculta con `f`; la lista ocupa entonces su ancho.
- Visor de cuerpo completo (`v`): modal a pantalla casi completa con scroll y `esc` para cerrar.

### 3.3 Red (`3`)

```
┌ Red de memoria · vecindario de <id> · N saltos 112c ────┐┌ Leyenda y filtros 38c ┐
│               [ error · timeout… ]                      ││ colores por sistema    │
│ [episodio]──┐         ┊                 [solución]      ││ filtros (espacio)      │
│ [episodio]──┼──▶ [ error · seleccionado ]──▶ ▲          ││ saltos ◀ 2 ▶           │
│ [episodio]──┘         ┊                    ▼            ││ selección: tipo, A …   │
│               [ decisión · proposed ]  [proced.]        ││ teclas                 │
└─────────────────────────────────────────────────────────┘└────────────────────────┘
```

**Algoritmo de diseño (para que sea estable, H-16.7):**

1. El nodo central va al centro del panel.
2. Por relación: los orígenes (`derived_from` hacia el centro, `contiene` desde episodios) a la izquierda; los resultados (`solves`, `procedure`) a la derecha; `relates` arriba; derivados del centro abajo; archivados abajo a la izquierda.
3. Dentro de cada lado, los nodos se ordenan por fecha de creación y se apilan con 3 filas de separación.
4. Si un lado no cabe, sus nodos se agrupan por tipo (H-17.2).
5. Las líneas son ortogonales; las etiquetas de relación se colocan en el tramo más largo sin tocar cajas.

### 3.4 Tareas (`4`)

```
┌ Agentes 48c ─────┐┌ Tareas · lista | grafo 100c ───────────────────────────────┐
│ (14 f)           ││ lista: id ▶ estado título agente/deps lease                │
├ Pizarra ─────────┤│ grafo: DAG izquierda → derecha                             │
│ (27 f, scroll)   │├ Detalle de tarea ──────────────────────────────────────────┤
│                  ││ scope, rol, siguiente paso, checkpoint, preguntas, eventos │
└──────────────────┘└────────────────────────────────────────────────────────────┘
```

### 3.5 Sueño (`5`)

Como el mockup tui-03: Ciclos (44c) a la izquierda con los 9 pasos del ciclo seleccionado; Regla propuesta (106c × 30f) a la derecha arriba; Otros cambios del ciclo (106c × 13f) abajo.

### 3.6 Métricas (`6`)

```
┌ Rango: [7 d] 30 d 90 d ──────────────────────────────────────────────────────────┐
│ ┌ tokens/sesión ┐ ┌ precisión ────┐ ┌ errores rep. ─┐ ┌ handoffs ─────┐ ┌ p95 hook ┐│
│ │ 1,240  ↓ 8 %  │ │ 68 %   ↑ 4 pp │ │ 2      ↓ 3    │ │ 83 %   ↑ 6 pp │ │ 42 ms    ││
│ │ ▁▂▃▂▂▁▁ meta ✓│ │ ▃▄▄▅▅▆▆ meta ✓│ │ ▅▄▃▃▂▂▁ meta ✓│ │ ▄▄▅▅▆▆▇ meta ✓│ │ meta ✓   ││
│ └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘ └──────────┘│
├ Por agente y modelo ───────────────────────────────────────────────────────────────┤
│ agente  modelo  sesiones  tokens medios  fatiga media  handoffs ok  errores rep.  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

Las metas son las de la sección Evaluación del spec: errores repetidos < 50 % de la línea base, handoffs ≥ 80 %, precisión ≥ 60 %, tokens < 2,000, p95 < 150 ms.

## 4. Diseño adaptable

| Tamaño de terminal | Diseño | Regla |
| --- | --- | --- |
| ≥ 150×46 | Completo | Como en la sección 3 |
| 120×36 a 149×45 | Tres columnas estrechas | Columnas proporcionales 22 % / 46 % / 32 %; paneles secundarios del Resumen (Sistemas, Sueño) se fusionan en uno |
| 100×30 a 119×35 | Dos columnas | La columna derecha pasa debajo de la central como pestañas internas (`Agentes · Tareas · Pizarra · Sueño`) |
| 60×20 a 99×29 | Un panel por vez | `tab` rota; la cabecera muestra "vista compacta"; la barra de teclas se reduce a 4 teclas + `?` |
| < 60×20 | Sin interfaz | Mensaje "La terminal es muy pequeña (mínimo 60×20)" |

Reglas para todos los tamaños:

- Ningún texto se sale de su panel: se recorta con `…` al final (o al medio para rutas: `src/…/payments.ts`).
- Los números nunca se recortan; si no caben, se oculta la columna completa de menor prioridad (orden de ocultación en la lista de recuerdos: `fuente`, `usos`, `estado`, `tipo`).
- Las barras tienen un ancho mínimo de 6 columnas; por debajo se muestra solo el número.

## 5. Modales

| Modal | Se abre con | Contenido | Cierre |
| --- | --- | --- | --- |
| Ayuda | `?` | Teclas globales, de la vista y del panel | `esc`, `?` |
| Selector de proyecto | `p` | Lista filtrable de proyectos | `enter` abre, `esc` cancela |
| Problemas | `!` | Resultado de `doctor`: conflictos, leases vencidos, índice, Ollama | `esc` |
| Confirmación | Acciones que escriben | Qué va a cambiar, botón por defecto seguro | `enter` / `esc` |
| Confirmación destructiva | Olvidar, rechazar | Texto en rojo + escribir palabra de confirmación | `enter` tras escribir / `esc` |
| Motivo | Marcar dudoso, rechazar | Campo de texto de una línea | `enter` / `esc` |
| Visor | `v` | Cuerpo completo del recuerdo | `esc` |
| Filtros | `f` | Campos de filtro de la vista | `esc` aplica y cierra |
| Simulación de sueño | `S` | Resultado de `--dry-run` y botón para ejecutar | `enter` ejecuta / `esc` |

Los modales se centran, ocupan como máximo 80 % del ancho y 70 % del alto, y oscurecen el fondo.

## 6. Mapa de navegación

```
                     ┌──────────── p (selector) ────────────┐
                     ▼                                      │
 hipo tui ──▶ [1 Resumen] ◀──▶ [2 Memoria] ◀──▶ [3 Red] ◀──▶ [4 Tareas] ◀──▶ [5 Sueño] ◀──▶ [6 Métricas]
                 │  enter en recuerdo ──▶ 2 Memoria (detalle)
                 │  enter en tarea ────▶ 4 Tareas (detalle)
                 │  enter en reglas ───▶ 5 Sueño
                 │  l en detalle ──────▶ 3 Red centrada en ese recuerdo
                 │  r (global) ────────▶ 5 Sueño, primera regla proposed
                 └  ! (global) ────────▶ modal Problemas ──enter──▶ vista del problema
```

`esc` vuelve por el historial de navegación (máximo 20 pasos); con historial vacío no hace nada. `q` sale desde cualquier vista sin modal abierto; si hay un ciclo de sueño lanzado desde la TUI, pide confirmación y el ciclo sigue en segundo plano.
