# 06 · Estados especiales

Cada estado define qué ve el usuario, qué puede hacer y cómo se sale de él. Ningún estado especial deja la pantalla en blanco ni muestra una traza de error de Go.

## 1. Vacíos

| ID | Situación | Dónde | Qué se muestra | Acción sugerida |
| --- | --- | --- | --- | --- |
| EE-01 | No hay proyectos registrados | Proyectos | "Aún no hay proyectos. Ejecuta `hipo init` dentro de un repo." | — |
| EE-02 | Proyecto sin recuerdos | Recuerdos | "Este proyecto aún no tiene memoria. Se llenará sola al trabajar con un agente, o con `hipo bootstrap`." | — |
| EE-03 | Ningún recuerdo pasa los filtros | Recuerdos | "Ningún recuerdo con estos filtros" + lista de filtros activos | `x` para quitar |
| EE-04 | Sin sesión activa | Contexto, Agentes | "Sin sesión activa" + datos de la última sesión cerrada, marcados "última sesión · hace N" | `[` `]` |
| EE-05 | Sin tareas | Tareas | "No hay tareas. Los agentes las crean con `hipo task`." | — |
| EE-06 | Sin eventos | Pizarra | "Sin eventos todavía" | — |
| EE-07 | Sin ciclos de sueño | Sueño | "La memoria aún no ha dormido. El primer ciclo ocurre tras 3 sesiones o 24 h." | `S` si Ollama está disponible |
| EE-08 | Sin reglas propuestas | Sueño | "No hay reglas por revisar" + resumen del último ciclo | — |
| EE-09 | Recuerdo sin enlaces | Red | El nodo solo, con "sin enlaces todavía" | — |
| EE-10 | Sin datos para el rango | Métricas | Tarjetas con `—` y "sin sesiones en este rango" | `←` `→` |

## 2. Carga y espera

| ID | Situación | Qué se muestra |
| --- | --- | --- |
| EE-11 | Primer cuadro mientras se leen datos | La estructura de paneles con sus títulos y "cargando…" atenuado dentro; nunca una pantalla vacía |
| EE-12 | Recalculando la activación (más de 100 ms) | "calculando…" en el título del panel Recuerdos; la lista anterior sigue visible y navegable |
| EE-13 | Calculando deriva del ancla (llama a git) | En Detalle, "deriva: calculando…" en su línea; el resto del detalle ya visible |
| EE-14 | Ciclo de sueño en curso | En Sueño y en la cabecera: "durmiendo · paso k de 9"; la TUI sigue usable |

## 3. Errores y degradación

| ID | Situación | Detección | Qué se muestra | Comportamiento |
| --- | --- | --- | --- | --- |
| EE-15 | Ollama no responde | Sondeo (05, sección 1) | Cabecera `Ollama ○`; en Sueño, "pasos 3, 4 y 5 encolados desde …" | `S` desactivado con explicación; búsqueda solo de texto (H-28) |
| EE-16 | Falta un modelo de Ollama | `/api/tags` sin el modelo | Cabecera `Ollama ●` amarillo; `!` lista "falta el modelo X: `ollama pull X`" | Igual que EE-15 para lo que use ese modelo |
| EE-17 | `index.db` no existe o está corrupto | Error al abrir | Banner: "El índice no está disponible. Ejecuta `hipo reindex`." | Las vistas que leen archivos (Detalle, Tareas, Pizarra, Sueño) siguen; Recuerdos, Red y Métricas muestran el banner |
| EE-18 | Índice atrasado frente a los archivos | `doctor` | `!` con "índice desactualizado" | Funciona con lo que hay |
| EE-19 | Ruta del proyecto no existe | Al abrir | En Proyectos `✕ ruta no encontrada`; si es el proyecto actual, se abre la vista de Proyectos | No se puede abrir |
| EE-20 | Almacén inaccesible (permisos) | Al abrir | "No se puede leer el almacén en <ruta>: permiso denegado" | Se vuelve a Proyectos |
| EE-21 | `events.jsonl` con una línea inválida | Al leer | La línea se omite; en `!` "N eventos ilegibles" | Sigue leyendo las siguientes |
| EE-22 | Archivo de recuerdo con frontmatter inválido | Al leer | En la lista, fila con `✕ inválido` y el error en Detalle | No cuenta en activación; `o` para abrirlo |
| EE-23 | `config.toml` inválido | Al abrir | Banner: "config.toml inválido (línea N): se usan valores por defecto" | Funciona con los valores por defecto del spec |
| EE-24 | Versión del esquema mayor que la del binario | `schema_version` | "Este almacén usa el esquema N; actualiza hipo" | Solo lectura forzada, sin acciones |
| EE-25 | Git no disponible | Al calcular deriva | "deriva: no disponible (git no encontrado)" | El resto funciona |

## 4. Escrituras

| ID | Situación | Qué se muestra | Comportamiento |
| --- | --- | --- | --- |
| EE-26 | El recuerdo cambió desde que se abrió (versión distinta) | Modal "Este recuerdo cambió mientras lo mirabas" con ambas versiones resumidas | No se escribe; se ofrece recargar y repetir la acción |
| EE-27 | Lock ocupado (otro proceso escribiendo) | Aviso "Ocupado, reintentando…" | Reintenta 3 veces con 200 ms; si falla, aviso con la causa (CW-4) |
| EE-28 | El agente renovó el lease mientras se liberaba | "El lease se renovó: el agente sigue activo" | No se libera |
| EE-29 | El editor externo termina con error | "El editor terminó con error; no se guardó nada" | Se descarta |
| EE-30 | Disco lleno o sin permiso de escritura | Aviso con la ruta y el error del sistema | No cambia la vista |

## 5. Terminal

| ID | Situación | Comportamiento |
| --- | --- | --- |
| EE-31 | Terminal menor a 60×20 | Solo el mensaje de tamaño mínimo (H-29.4) |
| EE-32 | Redimensionado | Rediseño en el siguiente cuadro, conservando selección y scroll (H-29.6) |
| EE-33 | Sin color (`NO_COLOR`, `--no-color` o terminal sin soporte) | Iconos y etiquetas de texto en lugar de colores (H-29.5) |
| EE-34 | Solo 16 colores | Paleta reducida definida en 09, sección 6 |
| EE-35 | Caracteres de dibujo no disponibles (`--ascii`) | Marcos con `+-|`, iconos ASCII: `^` por `▲`, `>` por `▶`, `#` por `■`, `v` por `✓` |
| EE-36 | Salida que no es una terminal (tubería) | No se abre la TUI; mensaje "hipo tui necesita una terminal interactiva; usa hipo stats o hipo recall" y código de salida 2 |
