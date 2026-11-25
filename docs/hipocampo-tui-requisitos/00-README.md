# Hipocampo TUI · Requisitos v1.0

Paquete de requisitos del cliente de terminal de Hipocampo (`hipo tui`). Se basa en el spec técnico v1.0, en los 13 diagramas y en los 3 mockups de la TUI.

## Cómo leer este paquete

| # | Archivo | Qué contiene | Para quién |
| --- | --- | --- | --- |
| 01 | `01-vision-y-alcance.md` | Para qué existe la TUI, quién la usa, qué entra y qué no en el MVP, principios | Todos |
| 02 | `02-historias-de-usuario.md` | 29 historias en 8 épicas, cada una con prioridad y criterios de aceptación | Producto, desarrollo, QA |
| 03 | `03-pantallas-y-navegacion.md` | Las 6 vistas, sus paneles, modales, tamaños de terminal y mapa de navegación | Diseño, desarrollo |
| 04 | `04-mapa-de-teclas.md` | Todas las teclas por vista, reglas para evitar choques | Desarrollo, QA |
| 05 | `05-contrato-de-datos.md` | Qué muestra cada panel, de dónde lo lee, cómo lo calcula y cada cuánto refresca | Desarrollo |
| 06 | `06-estados-especiales.md` | Vacío, carga, error, sin Ollama, terminal chica, conflictos | Desarrollo, QA |
| 07 | `07-requisitos-no-funcionales.md` | Rendimiento, compatibilidad, accesibilidad, seguridad, concurrencia | Desarrollo, QA |
| 08 | `08-plan-de-pruebas.md` | Niveles de prueba, fixtures, snapshots, matriz de terminales, checklist manual | QA, desarrollo |
| 09 | `09-arquitectura-tui.md` | Paquetes, modelo de estado, mensajes, lectura del núcleo, estilos | Desarrollo |
| 10 | `10-backlog-y-entregas.md` | Orden de implementación en 4 hitos y definición de hecho | Todos |
| — | `matriz-trazabilidad.csv` | Historia → vista → panel → diagrama → sección del spec → pruebas | QA, producto |
| — | `mockups/` | Las 3 pantallas de referencia en SVG | Todos |
| — | `fuentes.md` | Documentación externa citada | Desarrollo |

## Convenciones

- **IDs.** Historias `H-NN`, criterios `H-NN.k`, requisitos no funcionales `RNF-NN`, estados especiales `EE-NN`, pruebas `P-NN`.
- **Prioridad (MoSCoW).** *Must*: sin esto no hay MVP. *Should*: entra en el MVP si el hito lo permite. *Could*: después del MVP.
- **Criterios** en formato *Dado / Cuando / Entonces*. Un criterio sin "Dado" aplica siempre.
- **Valores numéricos** (umbrales, pesos, plazos) salen de `config.toml` del spec v1.0. La TUI **nunca** los codifica: los lee de la configuración del proyecto.
- **Glosario** al final de `01-vision-y-alcance.md`.

## Estado

| Campo | Valor |
| --- | --- |
| Versión | 1.0 (borrador para revisión) |
| Fecha | 2026-11-06 |
| Depende de | Hipocampo spec técnico v1.0 |
| Decisión pendiente | Si la TUI reemplaza al cliente web `hipo ui` en la fase 6 del MVP o conviven (ver 01, sección 4) |
