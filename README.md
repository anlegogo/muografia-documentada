# Muografía: documentación y seguimiento académico

**Estado del OE1 — 2026-10-03: cumplido y cerrado por decisión de la dirección bajo el alcance idealizado adoptado.** Datos, distribución, justificación e informe específico completos. [Registro de cierre](objetivo-1/CIERRE_OE1.md). No se requieren nuevas corridas para este alcance; no se declara aprobada la tesis completa.

| Documento | Contenido |
|---|---|
| [Informe de cierre del OE1](objetivo-1/manuscrito/README.md) | Informe con figuras integradas, nomenclatura, formulación matemática y justificación. |
| [Ficha del conjunto](objetivo-1/FICHA_CONJUNTO_OE1.md) | Datos, campos, receta, particiones, versiones, límites y reproducción. |
| [Síntesis de resultados y figuras](objetivo-1/SINTESIS_RESULTADOS_OE1.md) | Texto para el informe y tres figuras exportables en PNG/PDF. |
| [Definición y criterios de cierre](objetivo-1/DEFINICION_PRODUCTO_OE1.md) | Alcance adoptado y evidencia de A-01 a A-08. |
| [Matriz de cumplimiento](objetivo-1/MATRIZ_CUMPLIMIENTO.md) | Aspectos verificados y límites de la conclusión. |
| [Pendientes](objetivo-1/PENDIENTES.md) | P-01 a P-05 resueltos dentro del alcance aceptado. |
| [Revisión directa f395570](objetivo-1/REVISION_DATOS_F395570.md) | 477 huellas, evaluación desde píxeles y reproducción de 9.120 pares. |
| [Distribución verificada](objetivo-1/REVISION_DISTRIBUCION_DRIVE.md) | Descarga independiente, integridad y procedimiento reproducible. |
| [Índice documental](docs/INDICE.md) | Herramientas, protocolos y revisiones anteriores. |

La campaña contiene 19 escenarios idealizados con seis vistas, 344 millones de primarios por vista y 39.216 millones en total. Cumplen el criterio 1.710 regiones de borde; 107/114 vistas alcanzan la meta descriptiva de roca. Se conservan las siete excepciones y el 94,944 % global de ROI con al menos 100 cuentas no sustituye los indicadores individuales.

## Datos y versiones

El conjunto corregido de `f395570` se distingue del catálogo histórico conservado en `objetivo-1/originales/`. Los históricos no se convierten en referencias finales por renombrarlos. Las entregas estudiantiles permanecen en su rama; esta documentación las revisa sin fusionarlas automáticamente.

`objetivo-1/evidencias/` contiene las verificaciones; `objetivo-1/figuras/` los gráficos; `herramientas/` los procedimientos reproducibles. Los archivos grandes de trabajo local se guardan en `trabajo/`, fuera del historial Git. Consultar [procedencia](docs/PROCEDENCIA.md), [ficha actual](objetivo-1/FICHA_CONJUNTO_OE1.md) y [versiones locales](requirements-oe1-local.txt).

La cronología permanece en el [registro de cambios](CHANGELOG.md), la [bitácora](objetivo-1/BITACORA.md) y los informes fechados. Se retiraron de esta entrada los avisos de preparación y recepción ya superados. No se certifica un detector real.

## Apertura del OE2 — revisión inicial

Por autorización expresa de la dirección se incorpora la [revisión de la implementación estudiantil](objetivo-2/README.md). Existe una cWGAN-GP reutilizable y se comprobó la compatibilidad de 7.200 pares de entrenamiento/validación. La penalización del crítico, la normalización y la identidad de los datos se corrigieron en una [implementación derivada v1](objetivo-2/CORRECCIONES_V1.md), con 17 controles y reanudación exacta en una prueba técnica de entrenamiento. El OE2 permanece pendiente de protocolo y entrenamiento prolongado; no se declara desempeño final.
