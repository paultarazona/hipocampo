# 09 · Arquitectura de la TUI

## 1. Pila

| Pieza | Librería | Por qué |
| --- | --- | --- |
| Ciclo de la aplicación | `github.com/charmbracelet/bubbletea` | Arquitectura Elm (modelo, actualización, vista); estado inmutable y fácil de probar |
| Componentes | `github.com/charmbracelet/bubbles` | Listas, tablas, viewport con scroll, campo de texto, ayuda de teclas |
| Estilos y diseño | `github.com/charmbracelet/lipgloss` | Bordes, colores con degradación a 256 / 16 colores, composición de paneles |
| Pruebas | `github.com/charmbracelet/x/exp/teatest` | Ejecuta el programa con tamaño fijo y compara la salida con archivos *golden* |
| Vigilancia de archivos | `github.com/fsnotify/fsnotify` | Notificaciones del sistema en Linux, macOS y Windows |
| Datos | Paquetes del núcleo de `hipo` | Sin duplicar cálculos (D-4) |

Todas son de código abierto con licencias compatibles con Apache-2.0 (MIT o BSD). Verificar versión y licencia al fijar dependencias, como el resto del proyecto.

## 2. Paquetes

```
cmd/hipo/                      # subcomando: hipo tui
internal/tui/
├── app/          # modelo raíz: vista activa, historial, tamaño, modales, avisos
├── query/        # consultas de solo lectura sobre el núcleo (única puerta a los datos)
├── watch/        # vigilancia de archivos, data_version de SQLite, sondeo de Ollama
├── actions/      # escrituras: llaman a las operaciones del núcleo (D-6)
├── views/
│   ├── resumen/
│   ├── memoria/
│   ├── red/      # incluye el algoritmo de diseño de 03, sección 3.3
│   ├── tareas/
│   ├── sueno/
│   └── metricas/
├── components/   # panel con título, barra, sparkline, etiqueta de estado, modal
├── keys/         # mapa de teclas (fuente de verdad para la ayuda y la prueba P-12)
├── theme/        # tokens de color y variantes (sección 6)
├── layout/       # cálculo de paneles por tamaño de terminal (03, sección 4)
└── text/         # cadenas visibles (es.go)
```

Reglas de dependencia:

- `views/*` solo importan `components`, `keys`, `theme`, `layout`, `text` y los **tipos** de `query`. Nunca abren archivos ni la base de datos.
- `query` y `actions` son los únicos que importan paquetes del núcleo.
- `watch` solo produce mensajes; no modifica modelos.

## 3. Modelo de estado

```go
type Model struct {
    project   query.Project      // proyecto abierto
    view      ViewID             // vista activa
    history   []ViewID           // para esc (máx. 20)
    size      layout.Size        // columnas y filas
    session   *query.Session     // sesión elegida para el contexto
    views     map[ViewID]tea.Model
    modal     tea.Model          // nil si no hay
    toasts    []Toast            // avisos
    status    query.GlobalStatus // cabecera: Ollama, agentes, problemas
    prefs     Prefs              // ~/.hipocampo/tui.toml
}
```

Cada vista es su propio `tea.Model` con su selección, scroll y filtros, de modo que volver a una vista restaura su estado (H-02.3).

## 4. Mensajes

| Mensaje | Lo produce | Lo consume |
| --- | --- | --- |
| `tea.KeyMsg`, `tea.WindowSizeMsg` | Bubble Tea | `app`, luego la vista activa |
| `ProjectLoaded`, `ProjectChanged` | `query` | `app` y todas las vistas |
| `MemoriesUpdated` | `watch` (cambio de `data_version` o de archivos) | Resumen, Memoria, Red |
| `EventsAppended{events}` | `watch` (offset nuevo de `events.jsonl`) | Resumen, Tareas |
| `LeasesChanged`, `SessionsChanged` | `watch` | Resumen, Tareas, cabecera |
| `OllamaStatus` | `watch` (cada 30 s) | Cabecera, Sueño, búsqueda |
| `DriftComputed{id, drift}` | `query` (en segundo plano) | Detalle |
| `ActionResult{ok, err}` | `actions` | `app` (aviso) y la vista afectada |
| `Tick` (1 s) | `app` | Contadores de lease, hora |

Toda E/S se hace en `tea.Cmd` (goroutines gestionadas por Bubble Tea) que devuelven uno de estos mensajes. `Update` y `View` nunca hacen E/S (RNF-05).

## 5. Acceso a datos

- **SQLite:** conexión propia de la TUI con `mode=ro`, una sola conexión de lectura por proyecto, transacciones cortas. Requiere que el núcleo use WAL (D-7), con lo que los lectores no bloquean al escritor.
- **Cambios en el índice:** `PRAGMA data_version` cada 1 s; si cambia, se emite `MemoriesUpdated`.
- **Eventos:** se guarda el offset en bytes de `events.jsonl`; al cambiar el archivo se lee solo lo nuevo; si el archivo se reduce (rotación), se relee desde el principio.
- **Archivos de recuerdo:** se leen al abrir el detalle; la lista usa el índice.
- **Agrupación de cambios:** varios eventos de vigilancia en menos de 150 ms se agrupan en un solo mensaje, para no recalcular en cada escritura de un hook.

## 6. Tema

Tokens usados en los mockups. Todos los colores de la interfaz salen de aquí (RNF-27).

| Token | Oscuro | Claro | 16 colores | Uso |
| --- | --- | --- | --- | --- |
| `bg` | `#0f1218` | `#fcfcfb` | por defecto | Fondo |
| `fg` | `#d9d6ce` | `#1f1e1b` | blanco / negro | Texto principal |
| `dim` | `#8b8880` | `#5e5c57` | gris | Texto secundario |
| `faint` | `#5c5f68` | `#8f8d87` | gris oscuro | Bordes, filas bajo el umbral |
| `sel` | `#262c42` | `#e6e3f5` | inverso | Fila seleccionada |
| `accent` | `#9085e9` | `#5a4bc9` | magenta | Teclas, foco, marca |
| `epi` | `#5a9cf0` | `#2a6fc8` | azul | Episódica |
| `sem` | `#2fc48d` | `#12855c` | verde | Semántica |
| `proc` | `#f08a5d` | `#b04a17` | rojo claro | Procedural |
| `pros` | `#e77ca3` | `#b83f71` | magenta claro | Prospectiva |
| `red` | `#ef6b6b` | `#c43636` | rojo | Error, riesgo, rechazo |
| `yellow` | `#e5b23a` | `#9a6a00` | amarillo | Suspect, cansado, umbral de inyección |
| `green` | `#46c25a` | `#1d7a2c` | verde | Done, validado, despierto |
| `cyan` | `#4fc3d9` | `#1b7f93` | cian | Pistas (rutas y símbolos) |

- El tema se elige por el fondo detectado de la terminal; se puede forzar con `tui.theme = "dark" | "light"`.
- `faint` no se usa nunca para información que no esté también en otra forma (las filas bajo el umbral llevan además el separador con texto).
- Sin color: los tokens de estado se sustituyen por etiquetas: `[suspect]`, `[proposed]`, `▲`, `■`.

## 7. Arranque

1. Resolver el proyecto (H-01): `--project`, carpeta actual (registro + `git rev-parse --git-common-dir`) o vista de Proyectos.
2. Leer `config.toml` y `~/.hipocampo/tui.toml`.
3. Dibujar la estructura con "cargando…" (EE-11).
4. En paralelo: abrir índice, leer sesiones, leases, últimos 200 eventos, primer sondeo de Ollama.
5. Al llegar los datos, dibujar; arrancar vigilancia.

## 8. Lo que la TUI nunca hace

- Escribir en el almacén sin pasar por `actions` → núcleo.
- Abrir el índice en modo escritura.
- Llamar a Ollama para generar (solo consulta `/api/tags` para saber si está).
- Guardar datos de memoria en su propio archivo de preferencias.
- Ejecutar comandos de shell sugeridos por el contenido de un recuerdo.
