# Verificación local del complemento OE3-C1

2026-10-04, Colombia. Preparación de la dirección. Configuración SHA-256 `9b37bf59180a2625782dd54484de3c7189f3121ef886cda6f0298b929e87f9ef`.

## Comprobaciones ejecutadas

- Ocho pruebas analíticas: cocientes, fondo sin duplicación, invariancia de escala, nulos, signo, dispersión entre realizaciones, soporte y mínimo de fracción sin suponer monotonía ni ignorar PSNR.
- Dos pruebas del flujo con una red identidad sintética: exportación, reutilización sin otra inferencia, rechazo de corrupción e identidad incompatible y detención cuando falta la prueba técnica. Esta red es un instrumento de prueba; no es un modelo científico del estudio.
- Verificación de fuentes EF-01, cuatro paquetes de datos, ocho pesos, registro C2 y 32 matrices originales con sus recibos. Se reutilizan 3.840 predicciones al 5 %.
- Inferencia real de cGAN original en CPU: dos ejecuciones continuas idénticas bit a bit; diferencia máxima respecto de cuatro predicciones conservadas al 5 % de **2,3543834686279297 × 10⁻⁶**, menor que la tolerancia técnica 10⁻⁴. Cuatro imágenes por cada fracción nueva presentan forma válida, finitud e inversión admisible. No se calcularon métricas científicas de esas doce salidas técnicas.
- Evaluación local completa del bloque 5 %: 4.320 registros de imagen, 1.134 regionales, 54 contrastes, 9.774 filas de métricas locales y 540 registros de señal entre realizaciones. Los resúmenes históricos de SSIM, PSNR, Q y contraste de EF-01-C2 se reprodujeron exactamente, con diferencia numérica máxima cero.

Hay 8.688 filas locales con geometría suficiente; los soportes comunes al 5 % conservan 43 combinaciones anomalía/vista para SNR, 46 para CNR y 46 para contraste de cuentas. Son soportes específicos de esta fracción, no los soportes definitivos de la evaluación conjunta. Los casos excluidos y los denominadores nulos permanecen en las tablas. No se sustituyen por ceros.

Entorno local: Python 3.12.14, NumPy 2.3.5, PyTorch 2.6.0+cpu y scikit-image 0.26.0. Las pruebas y sus comandos portables se encuentran en la [guía de ejecución](INSTRUCCIONES_COMPLEMENTO_OE3.md).

## Evidencia conservada

- [Prueba real de cGAN en CPU](evidencias/complemento-v1/smoke-cpu-cgan.json).
- [Comprobación local y huellas](evidencias/complemento-v1/verificacion-local.json).
- [Resumen del bloque 5 %](evidencias/complemento-v1/baseline-f05/resultado.json).
- [Métricas locales por realización](evidencias/complemento-v1/baseline-f05/metricas_locales.csv).
- [Señal entre realizaciones](evidencias/complemento-v1/baseline-f05/snr_repeticiones.json).
- [Inventario del bloque 5 %](evidencias/complemento-v1/baseline-f05/inventario.json).

## Pendientes y límites

La ejecución científica de las tres fracciones nuevas y la comprobación CUDA de cada modelo están pendientes. La evaluación completa de cuatro fracciones todavía no se ha ejecutado; se ha probado su cálculo de métricas con datos reales al 5 % y la regla de fracción mínima mediante casos analíticos. No se presentan estas verificaciones como una aceptación GPU.

Los estudiantes deben ejecutar `smoke`, `infer` y finalmente `evaluate`, siguiendo la guía. Son 11.520 predicciones adicionales con pesos congelados; no hay entrenamiento ni nuevas simulaciones. Al recibirlas se verificarán las huellas y se revisarán los resultados y exclusiones antes de concluir.

El referente sin red al 50 % es una decisión operativa posterior a los resultados conocidos, fijada para este complemento; no era un umbral numérico de la propuesta. Las métricas locales son descriptivas y el contraste de cuentas no reconstruye opacidad física. Por ello, esta preparación no cierra automáticamente OE3-P02, P03, P05 o P06. El informe final continúa aplazado.
