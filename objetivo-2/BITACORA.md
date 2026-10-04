# Bitácora del OE2

## 2026-10-03 — Revisión inicial autorizada por la dirección

- Actividad: revisión del código publicado por los estudiantes y diagnóstico local de compatibilidad con dataset-v2. Se conserva la autoría estudiantil de la implementación y simulación; la revisión se incorpora como seguimiento de la dirección.
- Entradas: repositorio original b88fa576494cb8a664c46b8c94c5918c5097d616, contraste de entrenamiento con 3315f82 y distribución Drive de 2026-10-03. Consulta de actualización documental 800ab86 en la rama estudiantil de la réplica, sin fusión.
- Procedimiento: inspección de arquitectura, pérdidas, lector, checkpoints, configuración y registros; ejecución de `herramientas/revisar_base.py` según el comando del [informe](README.md).
- Evidencia: [JSON](evidencias/revision-2026-10-03.json), con huellas y entorno. Comparados 7.200 pares de 90 vistas; forward de generador/crítico satisfactorio; reproducidas dependencia de referencia y discrepancia de GP.
- Incidencias de revisión: primeras consultas de archivos de entrenamiento se hicieron desde la réplica documental y no encontraron esos archivos; se corrigió la ruta al repositorio original. Primera ejecución del diagnóstico falló por exigir igualdad exacta a cero en aritmética float32; se adoptó tolerancia de 1e-8 para GP teóricamente nulo y 1e-5 relativo para su valor analítico. La repetición terminó con código cero. No se modificó la implementación estudiantil para obtener ese resultado.
- Límites: sin entrenamiento, sin inferencia sobre test/generalization, sin validación de GPU ni nueva evaluación de pesos históricos. El cierre del OE1 no cambia.
- Resultado: OE2-P01 a OE2-P04 pendientes, con criterios de cierre y orden propuesto. La siguiente actividad es una corrección versionada y una prueba breve antes de consumir recursos de SC3.

## 2026-10-03 — Corrección autorizada de los tres puntos

- Se creó una implementación derivada de b88fa57, conservando originales y atribución estudiantil. Se corrigieron pérdidas, lector, contrato de normalización y recuperación de checkpoints.
- P01–P03 resueltos para el entrenamiento sobre la distribución fijada; [documentación v1](CORRECCIONES_V1.md) y [evidencia](evidencias/correcciones-v1.json). Preparación: 90 vistas/7.200 pares comparados; escala calculada únicamente con train.
- Primera ejecución: 16 controles satisfactorios. Tras comprobar portabilidad, se fijaron finales LF en manifiesto y fuentes, se normalizaron saltos de línea al identificar código y se añadió una prueba de independencia de la referencia a través del lector. Repetición final: 17 controles satisfactorios, incluida reanudación exacta.
- Incidencias: la consulta adicional al repositorio citado como muography-thesis no pudo ejecutarse mediante gh porque ese ejecutable no está disponible. El convertidor histórico permanece no recuperado; la verificación independiente contra paquetes fuente evita depender de su ejecución para integrar los datos. La ayuda CLI emitió un aviso de caché de fuentes de Matplotlib sin permisos en el perfil de Windows; terminó correctamente y no afectó los controles numéricos.
- Se separó selección del mejor SSIM sin redondear del umbral de paciencia. Los resultados son pruebas técnicas CPU de dos pasos, sin apertura de imágenes reservadas y sin conclusión de calidad.
- Siguiente paso: protocolo OE2-P04 y prueba GPU, antes del entrenamiento prolongado.

## 2026-10-03 — Diseño del piloto OE2-P04

- Autorización de la dirección para preparar protocolo, configuraciones y comandos SC3. Se fijó comparación al 5 % entre U-Net L1 y cWGAN-GP, semilla 2026100301, lote 4 y normalización v1.
- Dos etapas: comprobación técnica de dos épocas con parada/reanudación deliberada, y piloto de hasta 30 épocas con 1.440 pares train/360 val, paciencia 8 y validación por época.
- Se añadieron ejecutor externo y resumen de registros; no se modifica la implementación corregida ni su identidad. Se registra baseline sin red, entorno, memoria CUDA y tiempos.
- Evidencia: [resumen técnico local](evidencias/protocolo-piloto-local.json), [protocolo](PROTOCOLO_PILOTO_F05.md) e [instrucciones](INSTRUCCIONES_PILOTO_SC3.md). Ambos métodos se ejecutan y reanudan en CPU para verificar comandos; esta comprobación no aprueba GPU ni calidad.
- Próximo paso: estudiantes ejecutan A en SC3 y, si pasa, B con autonomía dentro de los límites definidos. Se requiere revisión de resultados antes de ampliar a otras fracciones y repeticiones.
- Resultado local: veinte controles no GPU satisfactorios entre ambos métodos; se comprobó el rechazo de la entrega CPU como aceptación GPU y la coherencia de las cuatro configuraciones. Las dos redes aún empeoran el SSIM de entrada después de cuatro actualizaciones; se registra expresamente sin convertir la prueba técnica en evidencia de calidad. [Verificación del protocolo](evidencias/verificacion-protocolo-v1.json).

## 2026-10-03 — Revisión de entrega c054225

- Se consultó origin y se identificó la nueva rama oe2/piloto-f05. Se extrajo únicamente su entrega para revisión, sin fusión ni modificación de originales.
- Se comprobaron 110 huellas contra objetos Git, configuraciones y registros de cuatro ejecuciones; se reprodujo el baseline de 360 pares y la estadística del CSV. Evidencia: [revisión-c054225.json](evidencias/revision-c054225.json).
- Incidencias del procedimiento: la primera verificación de identidad usó codificación predeterminada de Windows y falló; UTF-8 explícito coincide con la identidad del ejecutor Linux. La extracción local convirtió a CRLF 67 archivos y produjo discrepancias aparentes de huella; los 110 objetos originales Git coinciden. Se mantuvieron los archivos recibidos y se añadió verificación directa del commit.
- Resultado: evidencia técnica GPU RunPod coherente; se inspeccionaron tres figuras. Pendientes P04a–d documentados en la [revisión](REVISION_PILOTO_C054225.md). No se descargaron pesos inexistentes en la entrega ni se repitió inferencia; no se abrieron imágenes reservadas.

## 2026-10-03 — Pesos publicados y revisión independiente

- Se revisó el enlace de la entrega fddd072 y se descargaron los dos mejores checkpoints. Coinciden tamaños, SHA-256, configuraciones, contrato y época seleccionada (5).
- Se reprodujeron 360 predicciones por modelo en CPU, dentro de tolerancias frente al CSV. Se inspeccionaron las 18 vistas y se calculó una exploración regional; no se abrieron imágenes reservadas. [Informe y límites](REVISION_PESOS_PILOTO_F05.md).
- Incidencia local: fallos de lectura e índice Git ilegible; se completó el cálculo en un entorno aislado y la publicación mediante GitHub. No se reparó ni se reconstruyó el índice local.
- P04b resuelto para inferencia de validación y P04a cubierto para los dos mejores pesos. P04c avanza como exploración; P04d continúa pendiente. No se autorizó ni se lanzó la campaña principal.

## 2026-10-03 — Evaluación con regiones geométricas

- Por autorización de la dirección se avanzó en el diagnóstico regional usando datos y pesos ya recibidos. Se fijaron máscaras y medidas sin seleccionar píxeles desde predicciones; la validación ya observada se declara exploratoria.
- Se verificaron geometrías y shards, ocho pruebas analíticas y 2.304 rayos por integración numérica. Se produjeron 18 mapas de regiones, 234 registros región/método y 24 contrastes; figura inspeccionada. [Informe, evidencia y comandos](EVALUACION_GEOMETRICA_PILOTO_F05.md).
- Resultado: reducción de error y conservación de cuentas no son equivalentes. Se documentan sesgos por región y cocientes indefinidos por cero cuentas, sin pseudoconteos ni exclusión silenciosa.
- Incidencias: lectura local fallida, control de contraste cero y contador NumPy no serializable. Procedimientos corregidos y ejecutados completos en entorno aislado; Git local no reparado.
- P04c: diagnóstico geométrico verificado, aceptación física parcial. P04d: diseñar ajuste acotado antes de ampliar. Sin nuevas simulaciones, entrenamiento ni acceso a test/generalization.

## 2026-10-03 — Diseño del ajuste acotado de cuentas

- Se atendió la autorización de la dirección para preparar el siguiente ensayo. Se fijaron control y variante regional, datos, pesos iniciales, semilla, cinco épocas y evaluación pareada. [Diseño y estados](DISENO_AJUSTE_CUENTAS_F05.md).
- Se implementó el componente de pérdida regional y se verificaron nueve casos matemáticos. Se comprobó gradiente regional y total finito sobre los 20.543.809 parámetros con dos pares de entrenamiento; cero pasos de optimizador y pesos idénticos al checkpoint.
- Incidencias: utilidad de gradientes dependiente de SymPy ausente, sustituida por diferencias finitas explícitas; lectura de geometría corregida a UTF-8. Verificaciones finales satisfactorias.
- Estado: diseño/componentes verificados. Ajuste-01 integración, Ajuste-02 CPU/GPU con recuperación y Ajuste-03 piloto pareado pendientes. No se presenta el componente como ejecutor de entrenamiento ni se requiere nueva simulación Geant4.

## 2026-10-03 — Integración y recuperación del ajuste A/B

- Por autorización de la dirección se completaron lector, máscaras train/val, ejecutor, recuperación, auditor GPU, evaluación regional y figuras. Se conservan el diseño científico, el código histórico y las entregas estudiantiles. [Guía vigente](INSTRUCCIONES_AJUSTE_CUENTAS_F05.md).
- Se verificaron 90 mapas, 30 archivos de datos/metadatos y conservación de las 78 máscaras regionales val previas. Trece controles funcionales, nueve de pérdida y ocho geométricos satisfactorios. Las cuatro ejecuciones técnicas de red completa reproducen exactamente estados y predicciones al recuperar; 16 actualizaciones de la batería y cuatro preliminares. [Evidencia consolidada](evidencias/integracion-ajuste-v1.json).
- La regresión del evaluador usa 720 predicciones anteriores: diferencia cero en 468 valores regionales y reproducción de 24 contrastes. No son resultados de un nuevo piloto. Se generaron figuras técnicas y se inspeccionó su presentación.
- Incidencias: índice Git original ilegible, dependencias de Adam ausentes y betas con tipos mixtos. Se utilizó copia aislada, dependencias locales y conversión explícita a flotantes; la batería definitiva pasó. No se reparó el índice original.
- Ajuste-01 verificado; Ajuste-02 CPU verificado/GPU pendiente; Ajuste-03 pendiente. No se ejecutó piloto de cinco épocas ni se abrieron imágenes test/generalization. Próximo paso: comprobar CUDA y ejecutar A/B con aceptación técnica; no se declara mejora física ni cierre del OE2.
