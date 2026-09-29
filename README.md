# Muografía: documentación y seguimiento académico

Réplica local selectiva del material de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega, UIS / GOTS. Esta primera incorporación se limita al **objetivo específico 1 (OE1): simulación y generación de datos**.

**Estado:** datos y código incorporados; integridad verificable; validación física pendiente de cierre. No se ha ejecutado una nueva campaña Geant4.

**Avance de revisión:** se reprodujeron en memoria los 9.120 pares y se identificaron defectos geométricos en seis escenarios. Consultar el [diagnóstico](objetivo-1/DIAGNOSTICO_GEOMETRIAS.md), la [revisión de datos](objetivo-1/REVISION_DATOS.md) y las [instrucciones listas para SC3](objetivo-1/INSTRUCCIONES_ESTUDIANTES.md).

## Por dónde comenzar

**Seguimiento del 29 de septiembre:** [primera entrega revisada con observaciones](objetivo-1/REVISION_ENTREGA_2026-09-29.md). El encargo vigente es [presentar el diseño del siguiente ensayo](objetivo-1/DISENO_SIGUIENTE_ENSAYO_OE1.md) antes de ampliar las simulaciones. Los resultados recibidos permanecen en la rama de estudiantes, sin fusionar.

1. [Índice de documentación](docs/INDICE.md).
2. [Alcance del OE1](objetivo-1/ALCANCE.md).
3. [Matriz de cumplimiento y evidencia](objetivo-1/MATRIZ_CUMPLIMIENTO.md).
4. [Guía de los materiales recibidos](objetivo-1/README.md).
5. [Pendientes y condiciones de cierre](objetivo-1/PENDIENTES.md).

## Organización

| Carpeta | Función |
|---|---|
| `docs/` | Procedencia, decisiones y reglas documentales. |
| `objetivo-1/originales/` | Material recibido, conservado byte por byte con sus rutas de trabajo. |
| `objetivo-1/inventario/` | Selección y huellas de cada archivo incorporado. |
| `objetivo-1/evidencias/` | Verificaciones de nuestra revisión, separadas de las afirmaciones de los autores. |
| `herramientas/` | Verificación local de integridad, sin regenerar datos. |

Los binarios NPZ y los logs están incluidos en esta copia local, pero excluidos del historial Git. Una futura copia desde Git debe restaurarlos desde el paquete indicado en [procedencia](docs/PROCEDENCIA.md) y comprobar sus huellas. No se han incluido redes, pesos, entrenamientos ni evaluaciones de OE2/OE3.

La organización documental no equivale a una validación científica. Consultar [cambios](CHANGELOG.md) antes de interpretar el estado del trabajo.
