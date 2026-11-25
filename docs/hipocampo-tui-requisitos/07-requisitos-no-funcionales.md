# 07 · Requisitos no funcionales

Cada requisito tiene una forma de medirlo; la columna "Prueba" remite a 08.

## 1. Rendimiento

Referencia: laptop de gama media, SSD, proyecto con 5,000 recuerdos y 20,000 eventos (fixture `escala`).

| ID | Requisito | Medida | Prueba |
| --- | --- | --- | --- |
| RNF-01 | Primer cuadro con datos | ≤ 300 ms desde `hipo tui` hasta la vista Resumen dibujada | P-14 |
| RNF-02 | Cambio de proyecto | ≤ 500 ms | P-14 |
| RNF-03 | Recalcular activación de la lista | ≤ 100 ms para 5,000 recuerdos | P-14 |
| RNF-04 | Latencia de datos en vivo | Un evento escrito en `events.jsonl` aparece en pantalla en ≤ 1 s | P-15 |
| RNF-05 | Fluidez | Respuesta a una tecla en ≤ 50 ms; nunca se bloquea el ciclo de dibujo por E/S | P-14 |
| RNF-06 | Consumo en reposo | < 2 % de CPU y < 80 MB de RAM con la TUI abierta 10 min sin tocarla | P-16 |

## 2. Compatibilidad

| ID | Requisito | Medida | Prueba |
| --- | --- | --- | --- |
| RNF-07 | Sistemas | Linux, macOS y Windows (amd64 y arm64), con el mismo binario `hipo` | P-17 |
| RNF-08 | Terminales | Windows Terminal, PowerShell, iTerm2, Terminal de macOS, GNOME Terminal, Alacritty, kitty, WezTerm, terminal integrada de VS Code; dentro de tmux y por SSH | P-17 |
| RNF-09 | Tamaños | Diseños de 03, sección 4, desde 60×20 | P-10 |
| RNF-10 | Color | Detecta truecolor, 256 y 16 colores; respeta `NO_COLOR` y `--no-color` | P-11 |

## 3. Concurrencia e integridad

| ID | Requisito | Medida | Prueba |
| --- | --- | --- | --- |
| RNF-11 | No bloquear a los agentes | Con la TUI abierta, la latencia p95 de `hipo hook pre_tool` no sube más de 10 ms | P-15 |
| RNF-12 | Lectura del índice | Conexión SQLite en solo lectura (`mode=ro`); transacciones de lectura cortas (< 50 ms) | P-15 |
| RNF-13 | Sin locks propios | La TUI no crea locks en el almacén; las escrituras usan los del núcleo | Revisión de código |
| RNF-14 | Escritura segura | Toda escritura verifica la versión del archivo antes de cambiarlo (EE-26) | P-08 |
| RNF-15 | Trazabilidad | Toda escritura produce un evento y un commit del almacén con `source.agent: human` | P-08 |

## 4. Accesibilidad y legibilidad

| ID | Requisito | Medida | Prueba |
| --- | --- | --- | --- |
| RNF-16 | Nunca solo color | Todo estado se distingue también por icono o texto | P-11 |
| RNF-17 | Contraste | Sobre el fondo de los temas oscuro y claro: texto principal ≥ 7:1; secundario y de color ≥ 4.5:1; atenuado (`faint`) ≥ 2.8:1 y solo para información que también está en otra forma | P-11 |
| RNF-18 | Teclado completo | Todas las funciones accesibles sin mouse | P-12 |
| RNF-19 | Sin parpadeo | Nada parpadea; los avisos aparecen y desaparecen sin animación más rápida que 2 Hz | Revisión |
| RNF-20 | Lectores de pantalla | Fuera del MVP; los comandos `hipo recall`, `hipo stats` y `hipo task list` cubren la misma información en texto plano | — |

## 5. Seguridad y privacidad

| ID | Requisito | Medida | Prueba |
| --- | --- | --- | --- |
| RNF-21 | Sin red | La TUI solo habla con Ollama en la URL configurada; ninguna otra conexión de red | P-18 |
| RNF-22 | Contenido como datos | El texto de los recuerdos se muestra escapado: las secuencias de escape ANSI y caracteres de control del contenido se eliminan antes de dibujar | P-19 |
| RNF-23 | Secretos | Si un recuerdo contiene un patrón de secreto que escapó a la redacción, se muestra como `[REDACTED]` y aparece en `!` | P-19 |
| RNF-24 | Modo home | Al mostrar proyectos en modo `home`, nunca se escribe nada en el repo del cliente | P-08 |

## 6. Mantenibilidad

| ID | Requisito | Medida |
| --- | --- | --- |
| RNF-25 | Sin cálculos duplicados | Activación, fatiga, deriva y métricas solo vienen del núcleo (D-4) |
| RNF-26 | Textos en un solo lugar | Todas las cadenas visibles en `internal/tui/text/es.go`, preparadas para otro idioma |
| RNF-27 | Estilos con tokens | Colores y bordes solo vía tokens del tema (09, sección 6) |
| RNF-28 | Cobertura | ≥ 80 % de líneas en `internal/tui/query` y en los `Update` de cada vista |
| RNF-29 | Tamaño | La TUI no agrega más de 6 MB al binario `hipo` |
