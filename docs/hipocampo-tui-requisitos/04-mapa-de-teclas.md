# 04 · Mapa de teclas

## 1. Reglas

1. **Tres niveles**: global (siempre), vista (solo en esa vista) y panel (solo con ese panel enfocado). Una tecla de un nivel inferior **no puede** usar una tecla global.
2. **Precedencia de `esc`**: cierra el modal abierto → cierra la búsqueda → quita el foco de un campo de texto → vuelve a la vista anterior. Nunca hace dos cosas con una pulsación.
3. **Mayúscula = más fuerte**: `s` ordena, `S` duerme; `e` edita, `E` exporta; `n` siguiente, `N` anterior. Las acciones con mayúscula nunca son destructivas sin modal.
4. **Destructivo nunca en una tecla**: olvidar y rechazar abren siempre un modal destructivo (CW-5).
5. **Sin combinaciones con `ctrl` salvo `ctrl+c`**, que sale siempre, incluso con un modal abierto. Así la TUI funciona igual en tmux, screen y SSH.
6. **Estilo vim opcional**: `j` / `k` / `h` / `l` equivalen a las flechas solo si `tui.vim_keys = true` en `~/.hipocampo/tui.toml`. Por defecto está desactivado porque `l` se usa para "ver en la red".
7. Cada tecla de este documento aparece en la ayuda (`?`) de su contexto y viceversa (prueba P-12).

## 2. Globales

| Tecla | Acción | Historia |
| --- | --- | --- |
| `1` … `6` | Ir a Resumen, Memoria, Red, Tareas, Sueño, Métricas | H-02.1 |
| `tab` / `shift+tab` | Panel siguiente / anterior | H-02.4 |
| `↑` `↓` | Mover la selección en el panel enfocado | — |
| `pgup` `pgdn` | Página arriba / abajo | — |
| `home` `end` | Primero / último elemento | — |
| `enter` | Abrir o activar el elemento seleccionado | — |
| `esc` | Ver regla 2 | H-02.5 |
| `/` | Buscar en la memoria | H-04 |
| `p` | Selector de proyecto | H-07.2 |
| `r` | Revisar reglas propuestas | H-24.1 |
| `!` | Problemas del proyecto (solo si hay alguno) | H-05.3 |
| `[` `]` | Sesión anterior / siguiente para el contexto | H-12.6 |
| `?` | Ayuda contextual | H-03 |
| `q` | Salir | — |
| `ctrl+c` | Salir siempre | — |

## 3. Por vista

### Resumen (`1`)

| Tecla | Panel | Acción | Historia |
| --- | --- | --- | --- |
| `enter` | Proyectos | Abrir el proyecto | H-07.1 |
| `enter` | Sistemas | Abrir Memoria filtrada por ese número | H-08.3 |
| `enter` | Contexto | Abrir el recuerdo inyectado seleccionado | H-12.3 |
| `enter` | Recuerdos | Abrir el recuerdo en Memoria | — |
| `l` | Recuerdos / Detalle | Ver en la red | — |
| `enter` | Tareas | Abrir la tarea en Tareas | — |
| `S` | Cualquiera | Simular y lanzar sueño | H-25 |

### Memoria (`2`)

| Tecla | Panel | Acción | Historia |
| --- | --- | --- | --- |
| `f` | Cualquiera | Mostrar / ocultar Filtros | H-10.1 |
| `t` | Recuerdos | Alternar tipo | H-10.3 |
| `s` | Recuerdos | Alternar orden (A, creación, último uso, saliencia) | H-09.6 |
| `c` | Recuerdos | Alternar con contexto / sin contexto | H-10.4 |
| `x` | Filtros | Quitar el filtro seleccionado | H-10.2 |
| `espacio` | Filtros | Activar / desactivar opción | H-10.1 |
| `v` | Detalle | Ver cuerpo completo | H-11.7 |
| `o` | Detalle | Abrir en `$EDITOR` solo lectura | H-11.7 |
| `l` | Detalle | Ver en la red | — |
| `d` | Detalle | Marcar dudoso / volver a active | H-13 |
| `g` | Detalle | Olvidar (modal destructivo) | H-14 |
| `e` | Detalle | Editar en `$EDITOR` | H-15 |

### Red (`3`)

| Tecla | Panel | Acción | Historia |
| --- | --- | --- | --- |
| `←` `↑` `↓` `→` | Red | Saltar al vecino en esa dirección | H-16.4 |
| `enter` | Red | Abrir detalle del nodo | H-16.4 |
| `c` | Red | Centrar en el nodo seleccionado | H-16.4 |
| `+` `-` | Red | Más / menos saltos (1 a 3) | H-16.5 |
| `z` | Red | Agrupar por pista | H-17.3 |
| `espacio` | Leyenda y filtros | Activar / desactivar filtro | H-17.1 |

### Tareas (`4`)

| Tecla | Panel | Acción | Historia |
| --- | --- | --- | --- |
| `g` | Tareas | Alternar lista / grafo | H-19.2 |
| `enter` | Tareas | Ver detalle de la tarea | H-19.3 |
| `u` | Tareas | Liberar lease | H-21 |
| `f` | Pizarra | Filtrar por agente o tarea | H-20.4 |
| `home` | Pizarra | Ir a los eventos más nuevos | H-20.5 |

### Sueño (`5`)

| Tecla | Panel | Acción | Historia |
| --- | --- | --- | --- |
| `↑` `↓` | Ciclos | Elegir ciclo | H-23.2 |
| `a` | Regla propuesta | Aprobar | H-24.3 |
| `x` | Regla propuesta | Rechazar (modal destructivo) | H-24.4 |
| `e` | Regla propuesta | Editar y aprobar | H-24.5 |
| `n` / `N` | Regla propuesta | Siguiente / anterior | H-24.6 |
| `o` | Regla propuesta | Abrir las fuentes (`derived_from`) en Memoria | H-24.2 |
| `enter` | Otros cambios | Abrir el recuerdo del cambio | H-23.4 |
| `S` | Cualquiera | Simular y lanzar sueño | H-25 |

### Métricas (`6`)

| Tecla | Panel | Acción | Historia |
| --- | --- | --- | --- |
| `←` `→` | Cualquiera | Cambiar rango (7, 30, 90 días) | H-26.5 |
| `E` | Cualquiera | Exportar CSV | H-27 |

## 4. Teclas reservadas

No se asignan en el MVP para dejarlas libres a futuro: `i` (insertar recuerdo), `m` (mover / reasignar tarea), `w` (ventana dividida), `:` (línea de comandos), `ctrl+r` (recargar forzado).

## 5. Conflictos revisados

| Tecla | Usos | Por qué no chocan |
| --- | --- | --- |
| `g` | Olvidar (Memoria) · grafo (Tareas) | Vistas distintas; olvidar siempre abre modal |
| `c` | Contexto (Memoria) · centrar (Red) | Vistas distintas |
| `x` | Quitar filtro (Memoria, panel Filtros) · rechazar (Sueño) | Vistas distintas; rechazar abre modal |
| `e` | Editar recuerdo (Memoria) · editar regla (Sueño) | Misma acción conceptual |
| `o` | Abrir en editor (Memoria) · abrir fuentes (Sueño) | Vistas distintas |
| `f` | Filtros de recuerdos (Memoria) · filtro de pizarra (Tareas) | Misma acción conceptual |
| `l` | Ver en la red | Solo es flecha si `vim_keys = true` y en ese caso pasa a `L` |
