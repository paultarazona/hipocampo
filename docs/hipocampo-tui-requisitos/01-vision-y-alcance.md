# 01 · Visión y alcance

## 1. Problema

Hipocampo trabaja en segundo plano: los hooks inyectan memoria, el sueño consolida y los agentes coordinan tareas sin que nadie mire. Eso es bueno para el consumo de tokens, pero deja al desarrollador a ciegas:

- No sabe **qué recibió** su agente en una sesión, ni por qué.
- No sabe si la memoria **ayuda o estorba** (recuerdos dudosos, ruido, errores repetidos).
- No ve **qué hacen los otros agentes** sobre el mismo flujo de tareas.
- Tiene que aprobar reglas del sueño con `hipo review`, sin el contexto de dónde salieron.

## 2. Objetivo

Una TUI que muestre, en una sola terminal y solo con el teclado, el estado completo de la memoria de tus proyectos y de los agentes que la usan, y que permita las pocas acciones humanas que el sistema necesita: aprobar reglas, marcar dudosos, olvidar y liberar tareas.

**Medida de éxito del MVP:** un desarrollador puede responder estas cinco preguntas en menos de 30 segundos cada una, sin salir de la TUI:

1. ¿Qué memoria recibió mi agente en esta sesión y cuántos tokens costó?
2. ¿Por qué apareció (o no apareció) este recuerdo?
3. ¿De dónde salió esta regla y quién la validó?
4. ¿Qué está haciendo cada agente y qué tareas quedan?
5. ¿Qué cambió en el último ciclo de sueño y qué falta aprobar?

## 3. Usuarios

| Persona | Contexto | Lo que más usa |
| --- | --- | --- |
| **Dev individual** | Trabaja con Claude Code y Codex en sus repos, a veces en paralelo | Resumen, detalle de recuerdo, revisión del sueño |
| **Dev con clientes** | Mezcla repos propios (modo `repo`) y de clientes (modo `home`) | Vista de proyectos, cambio rápido de proyecto |
| **Investigador** | Evalúa si la memoria funciona; compara condiciones | Métricas, red de memoria, trazabilidad |
| **Orquestador futuro** | No es humano: leerá los mismos datos por el núcleo | Nada de la TUI; por eso la TUI no guarda estado propio |

## 4. Relación con el cliente web

El spec v1.0 define `hipo ui` (navegador). Esta TUI cubre las mismas seis vistas.

**Recomendación:** en el MVP, la fase 6 entrega `hipo tui` en lugar de `hipo ui`. Razones: el flujo del usuario ya vive en la terminal, no necesita servidor local ni token, y se puede abrir por SSH. El cliente web queda para después del MVP, reutilizando el mismo paquete de consultas (`internal/tui/query`, ver 09).

## 5. Alcance del MVP

**Entra:**

- Comando `hipo tui` dentro del mismo binario `hipo`.
- Seis vistas: Resumen, Memoria, Red, Tareas, Sueño, Métricas.
- Cambio entre todos los proyectos del registro.
- Actualización en vivo de la pizarra, agentes y tareas.
- Acciones humanas: aprobar, rechazar o editar reglas propuestas; marcar dudoso; olvidar; liberar lease vencido; lanzar `hipo sleep --dry-run` y `hipo sleep`.
- Búsqueda de texto sobre recuerdos (FTS5).
- Funciona sin Ollama, sin color y en terminales de 100×30 o más.

**No entra en el MVP:**

- Crear recuerdos a mano desde la TUI (eso es `hipo record`).
- Editar `config.toml` desde la TUI.
- Reclamar tareas en nombre de un agente (`task claim` lo hacen los agentes).
- Mouse (se acepta scroll si la terminal lo envía, pero nada depende de él).
- Gráficos de alta resolución (sixel, kitty graphics).
- Varios proyectos a la vez en pantalla dividida.

## 6. Principios de diseño

1. **Solo lectura por defecto.** Toda acción que escribe pide confirmación, pasa por el núcleo y queda con `source.agent: human`.
2. **Nunca bloquear a los agentes.** La TUI abre `index.db` en solo lectura, no toma locks de archivos y nunca hace esperar a un hook.
3. **Sin estado propio.** Lo único que guarda la TUI es la preferencia de vista y filtros, en `~/.hipocampo/tui.toml`. Todo lo demás se lee del almacén.
4. **Explicar, no solo mostrar.** Cada número importante (activación, fatiga, deriva) se puede abrir para ver de dónde sale.
5. **Teclado primero.** Toda acción tiene tecla; la tecla está escrita en pantalla o en `?`.
6. **Degradar con elegancia.** Si algo falta (Ollama, índice, color, espacio), la vista lo dice y sigue funcionando con lo que hay.
7. **Mismo vocabulario que el spec.** `active`, `suspect`, `proposed`, `lease`, `L0/L1/L2`: sin traducir los nombres del modelo de datos.

## 7. Glosario

| Término | Significado |
| --- | --- |
| Almacén | Repositorio git pequeño con la memoria de un proyecto (`.memory/`) |
| Activación (A) | Puntaje que decide si un recuerdo entra a la ventana del agente. A ≥ 1.2 se inyecta; A ≥ 0.5 va al índice L1 |
| L0 / L1 / L2 | Capas de la memoria de trabajo: siempre, índice de títulos, detalle bajo demanda |
| Fatiga (F) | Medida 0–1 de degradación de una sesión; umbrales 0.5, 0.7, 0.85 |
| Lease | Permiso temporal (30 min) de un agente sobre una tarea; se renueva con checkpoint |
| Pizarra | Estado compartido de coordinación: tareas, leases y `live/events.jsonl` |
| Sueño | Proceso offline de 9 pasos que consolida la memoria |
| Proposed | Regla creada por el sueño que espera aprobación humana |
| Suspect | Recuerdo dudoso: el código cambió o hay contradicción |
| Contexto actual | Rama, archivos y comandos recientes de una sesión; alimenta el término C de la activación |
