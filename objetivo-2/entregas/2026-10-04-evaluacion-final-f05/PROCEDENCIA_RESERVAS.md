# Procedencia de las particiones reservadas

2026-10-04, Colombia. Declaración exigida por el [protocolo EF-01](../../PROTOCOLO_EVALUACION_FINAL_OE2.md) y por las [instrucciones de la evaluación final](../../INSTRUCCIONES_EVALUACION_FINAL_OE2.md) **antes de calcular desempeño** sobre las particiones reservadas: test (`geo-test-01`, `geo-test-02`, `geo-test-03`) y generalization (`geo-gen-01`) de `dataset-v2`. Se registró en la rama de entrega antes de iniciar la inferencia.

La revisión del historial la hicieron Daniel Pinto y Reinaldo Cárdenas sobre los repositorios `muografia-documentada`, `muography-thesis` y `muography-dl-reconstruction`, los registros de SC3 y RunPod y las entregas citadas.

## 1. Uso en los ocho modelos evaluados

Ninguno de los ocho modelos congelados se entrenó, validó ni seleccionó con datos de test o de generalización.

- **`unet_original` y `cgan_original`** (piloto al 5 %, mejor época 5; entrega `c054225`):
  - El contrato [contrato-datos-v1.json](../../evidencias/contrato-datos-v1.json) contiene 123 archivos, y los únicos shards incluidos son de train (12 geometrías) y val (3).
  - El lector `MuographyPairs` rechaza cualquier otra partición.
  - La lista de descarga del pod no incluye archivos `geo-test` ni `geo-gen`.
- **B1–B3, C0 y C1** (ensayo E1; entrega `804ce85`):
  - Parten del `best.pt` cGAN `e54d51f7…`.
  - Sus configuraciones declaran `train_split: train`, `selection_split: val` y `reserved_splits_allowed: false`.
  - La lista de descarga de los pods tiene 31 archivos (30 shards train/val y el checkpoint inicial), ninguno reservado. Lo mismo vale para las continuaciones previas C0/C1 y R1–R3 (`dac99d1`, `f6518ff`).
- **Validación:** todas las selecciones de época y todos los ensayos de ajuste se hicieron sobre val.

## 2. Exposición histórica de las mismas escenas

Sí hubo exposición previa de estas cuatro geometrías, en una etapa anterior del proyecto.

- **Datos:** `dataset-v1.0` de `muography-thesis`, congelado el 2026-08-31. Se generó con una campaña Geant4 de 114 vistas, con las mismas particiones, la misma semilla de catálogo (20260805) y las mismas fracciones. Las cuatro geometrías tienen la misma huella que en el catálogo actual: son **las mismas escenas**, simuladas antes de las correcciones del OE1, así que las imágenes no son idénticas a las de `dataset-v2`.
- **Modelos evaluados entonces:**
  - el cWGAN-GP final de la Fase C, con la misma arquitectura `unet_dc_5` y `patch_critic_70`;
  - las bases U-Net L1 (`e19`);
  - el filtro clásico congelado.
- **Momento:** un pase único sobre test (trabajo SLURM 29819, SC3 `felix`, 2026-09-05), después de congelar el protocolo v1.1 ese mismo día a las 18:53. Los resultados están en `muography-thesis` `b7b5183`:
  - SSIM 0,9057 / 0,8080 / 0,7933 / 0,7798 (etapa 20);
  - factor de reducción 31,26× frente a 27,59× de la clásica (etapa 22);
  - AUC del detector z de 0,483 (diagnóstico del 2026-09-24).
  - La partición de generalización se reportó como descriptiva.
- **Validez actual:** esos resultados no son válidos con el código corregido, y sus modelos no forman parte de esta evaluación.

## 3. Decisiones de diseño posiblemente influidas

- **Arquitecturas:** `unet_dc_5` y `patch_critic_70` se eligieron con validación (ensayos E16/E17, 1–5 de septiembre), antes de abrir test.
- **Influencia indirecta:** el OE2 actual reutilizó esas arquitecturas. Además, el equipo y la dirección conocían los resultados históricos sobre test. No puede descartarse que ese conocimiento influyera en decisiones posteriores, como la comparación U-Net frente a cGAN o el uso de la fracción del 5 %.
- **Cambios después de abrir test, en la evaluación histórica:**
  - un ajuste del denominador de 24 a 18 celdas, que es un cambio de reporte;
  - una corrección del código de ROI (`316eb2e`) cuya posición respecto de la apertura de test no puede establecerse, porque no hay un registro versionado del acceso.

## 4. Inspecciones visuales y de integridad

- **Inspecciones visuales históricas:**
  - una galería de diez figuras de predicciones sobre test (`muography-thesis` `61f6651`);
  - los informes de avance a la dirección del 14 y el 24 de septiembre.
- **Inspecciones del OE1:**
  - el cierre del OE1 presenta referencias de `geo-test-03` (vista 5) y `geo-gen-01` (vista 0);
  - la evaluación de calidad de la campaña (bordes e indicador de roca) recorrió las 114 vistas, incluidas las reservadas;
  - las superposiciones de ROI de `geo-gen-01` de la etapa 19 muestran opacidad derivada de la geometría, no conteos.
- **Accesos de integridad, sin entrenamiento ni selección de modelos:**
  - la generación de los 9.120 pares;
  - la conversión a `dataset-v2`;
  - las huellas de contenido, la copia y la verificación en Drive (P-05);
  - la reproducción independiente de la dirección.

## 5. Incertidumbre declarada

- **Manuscrito:** se revisó la versión de trabajo del manuscrito (capítulos 3 a 5, contenido del OE1). Incluye el catálogo de las cuatro geometrías reservadas y la tabla de excepciones del indicador de roca, con `geo-test-03` en las vistas 1 y 5. Son datos de calidad de las referencias, sin resultados de modelos sobre las particiones reservadas.
- **Actividad no registrada:** no puede verificarse la actividad fuera de los repositorios y registros citados.

## 6. Conclusión

Los ocho modelos no usaron las particiones reservadas para entrenamiento ni para selección. Sin embargo, esas mismas escenas ya se evaluaron e inspeccionaron en una etapa anterior del proyecto, con modelos de la misma arquitectura, y esos resultados fueron conocidos por el equipo y la dirección. Por lo tanto, **la evaluación final EF-01 se presentará como una evaluación descriptiva sobre datos potencialmente expuestos, no como una evaluación confirmatoria independiente.** Esta declaración no modifica las particiones, los modelos ni las métricas del protocolo.
