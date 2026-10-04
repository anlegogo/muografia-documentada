# Verificación de pesos e inferencia del piloto al 5 %

Fecha: 2026-10-03. Entrega estudiantil: [oe2/piloto-f05, fddd072](https://github.com/anlegogo/muografia-documentada/tree/fddd072172ebc6efa91708036c9b2775ea54b86b). Esta revisión complementa y actualiza la [revisión inicial c054225](REVISION_PILOTO_C054225.md).

## Resultado y alcance

Se descargaron y verificaron independientemente los dos checkpoints seleccionados del piloto, U-Net L1 y cWGAN-GP. Ambos corresponden a la época 5. Se repitió la inferencia sobre los 360 pares de validación al 5 % por método: 720 predicciones en total, con tres geometrías, seis vistas por geometría y veinte realizaciones por vista.

Las métricas reproducen la entrega dentro de las tolerancias declaradas. La U-Net conserva la ventaja en SSIM y PSNR. Esto verifica los resultados de validación de esta semilla; no demuestra superioridad física, generalización ni cierre del OE2. No se entrenaron modelos ni se abrieron imágenes de test/generalization.

## Integridad y procedencia

La [carpeta de pesos publicada por los estudiantes](https://drive.google.com/drive/folders/18pOGXzN2lEhKfxJlpcC4GuTujkNyA-ix) incluye un reporte estudiantil de descarga de ocho archivos. La comprobación independiente de esta revisión abarca los dos mejores checkpoints; no se extiende por inferencia a los otros seis.

| Checkpoint | Bytes | SHA-256 |
|---|---:|---|
| U-Net, best.pt | 246595774 | `734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a` |
| cGAN, best.pt | 279758342 | `e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0` |

Coinciden configuración, identidad de configuración, normalización, manifiesto de datos e identidad de implementación guardados en ambos checkpoints. Se cargó estrictamente el estado completo del generador con `weights_only=True` y una lista explícita de tipos NumPy permitidos. Todas las predicciones resultaron finitas.

Manifiesto fijado: `80db70d75e5ef2c40955881a87dd46b767137c24cb72dc1aa458a71c1efd8b03`.
Implementación: `f2dcc640e5b2917bab9b0876b4b46371961e0fa7c67703c3818c4693fc0b263a`.
La distribución de datos es la corregida y aceptada en el OE1. Las filas se contrastaron por geometría, vista y realización, no solo por posición agregada.

## Reproducción numérica

| Método | SSIM medio | PSNR medio (dB) | Máxima diferencia absoluta SSIM frente al CSV | Máxima diferencia PSNR (dB) |
|---|---:|---:|---:|---:|
| Entrada sin red, revisión anterior | 0,751812 | 24,1677 | 0 | 0 |
| U-Net L1, inferencia independiente | 0,843671 | 32,9037 | 6,881 × 10⁻⁷ | 9,286 × 10⁻⁵ |
| cWGAN-GP, inferencia independiente | 0,822791 | 31,1041 | 3,837 × 10⁻⁶ | 1,777 × 10⁻⁴ |

Tolerancias por imagen fijadas para el contraste CPU/GPU: diferencia SSIM menor que 10⁻⁴ y PSNR menor que 0,01 dB. Se satisfacen en todas las imágenes de ambos métodos. No se exige identidad bit a bit entre plataformas. Los valores completos están en la [evidencia de inferencia](evidencias/verificacion-pesos-f05.json).

Entorno independiente: Python 3.12.14, PyTorch 2.6.0+cpu, NumPy 2.3.5, scikit-image 0.26.0; dos hilos, lote cuatro, algoritmos deterministas. La entrega usó GPU y NumPy 2.4.4. Las diferencias numéricas observadas son pequeñas frente a las tolerancias; no se comparan tiempos CPU/GPU.

## Exploración regional

Se inspeccionaron las 18 vistas mediante figuras de referencia, predicción media de las veinte realizaciones y residuos. Los promedios se usaron solo para inspección visual; las métricas anteriores se calcularon por imagen. Se conservan indicios de bandas en U-Net y textura en cGAN. La apariencia visual por sí sola no demuestra preservación de señales.

Como diagnóstico reproducible se dividió cada vista en cuatro bandas iguales de 64 filas, de menor a mayor elevación. Son bandas de coordenadas, no máscaras físicas de roca, cielo o anomalía. Para cada predicción se invirtió la normalización antes de sumar cuentas:

```text
T(c) = log(1+c) / [s + log(1+c)],  s = 8,239329427901795
c(z) = exp[s·z/(1-z)] - 1
sesgo relativo = [media de la suma predicha en la banda − suma de referencia] / suma de referencia
```

| Banda de elevación | U-Net: sesgo medio de cuentas | cGAN: sesgo medio de cuentas |
|---|---:|---:|
| Cuarto inferior | +4,48 % | +5,09 % |
| Segundo cuarto | +3,91 % | +9,18 % |
| Tercer cuarto | +4,31 % | +12,69 % |
| Cuarto superior | +3,60 % | +13,41 % |

Cada cifra es el promedio no ponderado de los sesgos relativos de las 18 vistas. No equivale al sesgo del total acumulado de cuentas. Estos resultados motivan una evaluación de calibración; no constituyen un criterio de aceptación física fijado previamente.

### Zona que motivó la alerta visual

Se examinó de forma exploratoria una zona de geo-val-01, vista 0: fila 62 y columna 132, índices desde cero y origen inferior. Se comparó la media de un disco de radio cuatro píxeles con un anillo de radios ocho a doce. La selección parte de una figura anterior y es posterior a observar resultados; no constituye una prueba confirmatoria ni una ROI de anomalía validada.

El contraste normalizado centro menos anillo es +0,017086 en la referencia, +0,019065 en promedio para U-Net y −0,001222 para cGAN. U-Net mantiene contraste positivo en 20/20 realizaciones; cGAN presenta contraste negativo en 11/20. Las realizaciones comparten referencia y no son veinte escenarios independientes.

Por tanto, no se sostiene que la U-Net seleccionada produzca un punto oscuro en esa zona. El punto más evidente de la inspección inicial correspondía a época 10; esta revisión reproduce época 5 y no reevalúa los pesos de época 10. Tampoco se concluye que hayan desaparecido todos los artefactos. Los valores regionales completos y la definición de la zona están en la [evidencia exploratoria](evidencias/revision-regional-f05.json).

## Estado de pendientes y siguiente decisión

| Pendiente | Estado vigente |
|---|---|
| P04a: distribución | Resuelta la disponibilidad e integridad independiente de los dos mejores pesos necesarios para esta revisión. Los otros seis archivos cuentan con verificación estudiantil, no independiente aquí. |
| P04b: inferencia | Resuelto para los 360 pares de validación al 5 % y los dos checkpoints seleccionados. No incluye auditoría interna de los estados de reanudación de los otros checkpoints. |
| P04c: regiones y artefactos | Avance exploratorio sobre las 18 vistas; falta una evaluación con regiones justificadas por geometría y criterios establecidos antes de comparar ajustes. |
| P04d: campaña principal | Pendiente. El aporte del componente adversario aún no se ha demostrado. No se habilitan automáticamente los 24 entrenamientos propuestos. |

El siguiente paso es fijar máscaras y medidas de conservación de contraste y cuentas sobre train/val, establecer criterios explícitos y valorar si el componente adversario requiere un ajuste acotado. Los datos y pesos actuales permiten avanzar en ese análisis sin nuevas simulaciones Geant4. La selección final debe preceder al uso de las particiones reservadas. El OE1 continúa cerrado y el OE2 abierto.

## Reproducción y archivos grandes

La [herramienta de inferencia](herramientas/verificar_pesos_piloto.py) parametriza las rutas del procedimiento ejecutado. La [herramienta regional](herramientas/explorar_predicciones_piloto.py) genera el JSON y tres figuras, una por geometría, con las seis vistas. Las predicciones NPY y los pesos permanecen fuera de Git.

Ejemplo desde la raíz del repositorio, con las rutas de los pesos sustituidas por las descargas verificadas:

```powershell
python objetivo-2/herramientas/verificar_pesos_piloto.py --repo . --unet trabajo/pesos/unet-best.pt --cgan trabajo/pesos/cgan-best.pt --entrega trabajo/revision-c054225/objetivo-2/entregas/2026-10-03-piloto-f05 --datos trabajo/drive-2026-10-03 --salida trabajo/revision-pesos-f05
python objetivo-2/herramientas/explorar_predicciones_piloto.py --datos trabajo/drive-2026-10-03 --predicciones trabajo/revision-pesos-f05 --salida trabajo/revision-pesos-f05
```

La carpeta de entrega del primer comando contiene configuraciones y CSV de c054225, contrastados en la revisión inicial; el enlace nuevo de pesos procede de fddd072. El procedimiento numérico se ejecutó por separado para U-Net y cGAN; su versión unificada con argumentos se comprobó mediante la ayuda CLI, sin repetir otras 720 inferencias. El script regional parametrizado sí se ejecutó y sus tres figuras fueron inspeccionadas.

Durante esta revisión la copia local presentó fallos de lectura del sistema de archivos y un índice Git ilegible. Se utilizó un entorno aislado y se recuperaron los tres módulos necesarios del commit 86cb6eb; no se modificó la implementación científica. La evidencia se publica mediante la conexión GitHub, conservando el árbol remoto como base. No se declara reparada la copia local.
