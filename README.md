# Muografía: documentación y seguimiento académico

**Adaptación local:** [lector y exportador angular](objetivo-1/ADAPTACION_LECTURA_ANGULAR.md) probado con los 750 conteos reales; pendientes ROI, consumidores finales y aceptación física.

**Actualización de entrega:** [corrida angular revisada](objetivo-1/REVISION_MALLA_ANGULAR_2026-10-01.md): 1.000 primarios y 750 registros, 24 controles del revisor y 31 contrastes satisfactorios. Integración técnica respaldada en SC3; aceptación física y compatibilidad del conjunto final pendientes. Las instrucciones y estados anteriores se conservan como historial.

**Corrección preparada:** [malla azimutal v1](objetivo-1/correcciones/malla-angular-v1/README.md). Parche separado, seis pruebas Python satisfactorias; compilación C++ y verificación de integración en Geant4 pendientes.

**Nuevo control local:** [muestreo angular](objetivo-1/CONTROL_MUESTREO_ANGULAR.md). Se cuantifica una diferencia en las columnas de borde entre el muestreo de la fuente y la distribución nominal. Resolver la convención angular antes de fijar qué referencias reutilizar.

**Preparación actual:** [alcance de producción y decisiones de normalización](objetivo-1/PREPARACION_PRODUCCION_OE1.md). Inventario verificado de 114 referencias; 36 candidatas a regenerar y 78 de reutilización condicionada. Primero resolver la definición del observable y la receta de producción.

Réplica local selectiva del material de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega, UIS / GOTS. Esta primera incorporación se limita al **objetivo específico 1 (OE1): simulación y generación de datos**.

**Estado:** datos y código incorporados; etapa 1 ejecutada por los estudiantes en SC3 y análisis reproducido localmente. La validación física sigue pendiente; no se ha repetido la campaña de 114 vistas.

**Avance de revisión:** se reprodujeron en memoria los 9.120 pares y se identificaron defectos geométricos en seis escenarios. Consultar el [diagnóstico](objetivo-1/DIAGNOSTICO_GEOMETRIAS.md), la [revisión de datos](objetivo-1/REVISION_DATOS.md) y las [instrucciones listas para SC3](objetivo-1/INSTRUCCIONES_ESTUDIANTES.md).

## Por dónde comenzar

**Paso actual:** [auditoría completa de etapa 2](objetivo-1/AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md). Verificados los 85 archivos, las 27 listas y los 55 registros completos; conteos e intervalo reproducidos. Resultado estadístico inconcluso. Preparar producción B resolviendo entorno, normalización y alcance; las precisiones de interpretación E2-01/E2-02/E2-04 quedan documentadas. OE1 y P-01…P-04 siguen abiertos.

**Ejecución recibida:** etapa 2 realizada en SC3 por los estudiantes y [auditada íntegramente](objetivo-1/AUDITORIA_COMPLETA_ETAPA_2_2026-10-01.md); no se añaden corridas ni se inicia producción definitiva con esta revisión. Se preservan las entregas en sus ramas y los diseños congelados.

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
