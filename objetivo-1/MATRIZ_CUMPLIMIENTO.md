# Matriz de cumplimiento del OE1

Estado consolidado: 2026-10-03, después de revisar `f395570`, la entrega `cb57145` y la copia de Drive. «Verificado» se limita a la evidencia indicada; no equivale a validación experimental ni a calificación académica. Esta versión sustituye los avisos de preparación y recepción ya resueltos; la cronología se conserva en la [bitácora](BITACORA.md) y Git.

| ID | Aspecto | Estado y evidencia vigente | Pendiente real |
|---|---|---|---|
| OE1-01 | Escenarios volcánicos | **Verificado** el catálogo de 19 geometrías y su trazabilidad a las 114 referencias. Representatividad **parcial**, acotada a conos idealizados. | Valoración académica de representatividad: P-04. |
| OE1-02 | Simulación Monte Carlo | **Verificado** el registro de 1.026 filas completadas y la coherencia de receta, semillas, conteos y referencias a 344 M por vista. | No se exige repetir transporte; conservar límites de la verificación, que no reejecuta Geant4 localmente. |
| OE1-03 | Niveles de conteo | **Verificado** el contenido regenerado de los 9.120 pares; 342 huellas coincidentes, cuatro fracciones y veinte realizaciones. | Ninguna generación adicional requerida para esta comprobación. |
| OE1-04 | Organización y trazabilidad | **Verificado** el inventario de 477 archivos, particiones por geometría y ficha técnica. [Ficha final](FICHA_CONJUNTO_OE1.md). | P-05 resuelto: 753 archivos recuperados y verificados. [Revisión de Drive](REVISION_DISTRIBUCION_DRIVE.md). |
| OE1-05 | Calidad y alcance físico | **Verificado** el criterio de 1.710 bordes y la estadística de roca desde los píxeles; 107/114 vistas alcanzan la meta. Las siete excepciones se conservan. Interpretación física **parcial**. | Incorporar limitaciones y justificar representatividad en el informe: P-04. |
| OE1-06 | Reproducción independiente | **Verificado** el posproceso desde 114 histogramas, identidad CSV/NPZ y regeneración de pares con NumPy 2.4.4. | No afirmar segunda ejecución independiente de Geant4. De dataset-v2 solo se comprobó integridad y contenido distribuido, sin auditar el conversor ni entrenar redes. |

El producto de datos está técnicamente respaldado bajo el alcance idealizado. La [síntesis para el informe](SINTESIS_RESULTADOS_OE1.md) y las figuras están preparadas. El cierre académico depende de integrar y valorar esa justificación; no se asigna un porcentaje global arbitrario ni se ordena otra campaña.

Evidencia: [revisión directa](REVISION_DATOS_F395570.md), [ejecución](REVISION_CAMPANA_E037D09.md), [criterios A-01 a A-08](DEFINICION_PRODUCTO_OE1.md#lista-única-de-criterios-de-cierre) y [pendientes consolidados](PENDIENTES.md).
