# 10 · Backlog y entregas

La TUI se construye en cuatro hitos. Cada hito termina en una TUI usable y cumple su criterio de salida antes de pasar al siguiente. Corresponde a la fase 6 del plan del MVP del spec, y necesita que las fases 1 a 5 estén hechas (o al menos sus datos).

## Hito T1 · Esqueleto que ya sirve (solo lectura)

**Objetivo:** abrir la TUI, ver proyectos y recuerdos, y entender por qué un recuerdo tiene su activación.

| Historia | Prioridad | Notas |
| --- | --- | --- |
| H-01 Abrir la TUI | Must | Sin `--view` todavía |
| H-02 Cambiar de vista | Must | Las vistas no hechas muestran "próximamente" |
| H-03 Ayuda | Must | Generada desde `keys` |
| H-05 Cabecera | Must | Sin indicador `!` |
| H-06 Ver proyectos | Must | |
| H-07 Cambiar de proyecto | Must | |
| H-09 Recuerdos por activación | Must | Sin contexto de sesión (C = 0) |
| H-11 Detalle | Must | Sin deriva (llega en T2) |
| H-28 Sin Ollama | Must | |
| H-29 Tamaños y sin color | Must | Diseños completo y de dos columnas |

**Base técnica:** paquetes `app`, `query`, `components`, `keys`, `theme`, `layout`, `text`; fixtures `vacio` y `basico`; P-01, P-02, P-03.

**Salida:** F-01 pasa; P-05 (paridad de activación) en verde; snapshots de Resumen y Memoria en 150×46 y 110×32.

## Hito T2 · Contexto y coordinación en vivo

**Objetivo:** ver qué recibió cada agente y qué hacen los agentes ahora.

**Requiere del núcleo:** D-1, D-2, D-3, D-7.

| Historia | Prioridad |
| --- | --- |
| H-12 Lo que se inyectó en la sesión | Must |
| H-09 completa (con contexto de sesión) | Must |
| H-11 completa (deriva del ancla) | Must |
| H-18 Agentes activos | Must |
| H-19 Tareas y dependencias | Must |
| H-20 Pizarra en vivo | Must |
| H-05.3 Indicador de problemas | Must |
| H-10 Filtros | Must |

**Base técnica:** `watch` (archivos, `data_version`, Ollama); fixture `multiagente`; P-06, P-15.

**Salida:** F-02 pasa; RNF-04 y RNF-11 medidos en P-15.

## Hito T3 · Sueño y acciones humanas

**Objetivo:** que el humano pueda corregir la memoria y aprobar reglas desde la TUI.

**Requiere del núcleo:** D-5, D-6.

| Historia | Prioridad |
| --- | --- |
| H-23 Ciclos de sueño | Must |
| H-24 Revisar reglas propuestas | Must |
| H-13 Marcar dudoso | Should |
| H-14 Olvidar | Should |
| H-21 Liberar lease vencido | Should |
| H-16 Red de memoria | Must |

**Base técnica:** `actions`, modales de confirmación y destructivo; fixture `home`; P-08, P-09.

**Salida:** F-03 a F-08 pasan; P-08 verifica eventos, commits y que el modo `home` no toca el repo del cliente.

## Hito T4 · Completar el MVP

| Historia | Prioridad |
| --- | --- |
| H-04 Búsqueda | Should |
| H-08 Salud del proyecto | Should |
| H-17 Filtrar y agrupar la red | Should |
| H-22 Aviso de fatiga alta | Should |
| H-26 Métricas | Should |
| H-29 completa (tres columnas estrechas, un panel por vez, `--ascii`) | Must |

**Base técnica:** fixtures `escala`, `roto`, `hostil`; P-07, P-10 a P-14, P-16 a P-19.

**Salida:** criterio de la sección 6 de 08 completo. Se publica con la v1.0 de Hipocampo.

## Después del MVP

| Historia | Prioridad |
| --- | --- |
| H-15 Editar un recuerdo | Could |
| H-25 Lanzar sueño manual | Could |
| H-27 Exportar métricas | Could |
| Cliente web `hipo ui` reutilizando `internal/tui/query` | — |
| Pantalla dividida con dos proyectos | — |

## Definición de hecho (para cada historia)

- [ ] Todos sus criterios de aceptación tienen al menos una prueba enlazada en `matriz-trazabilidad.csv`, y pasan.
- [ ] Sus teclas están en `keys` y aparecen en `?` (P-12).
- [ ] Tiene snapshot en el tamaño completo y en el de dos columnas, con y sin color.
- [ ] Sus estados especiales (06) están implementados y probados.
- [ ] No hace E/S en `Update` ni en `View`.
- [ ] Si escribe, cumple CW-1 a CW-5.
- [ ] Textos en `text/es.go`; colores solo vía `theme`.
- [ ] Revisada por otra persona (o, en solitario, por un segundo agente que no la escribió).
