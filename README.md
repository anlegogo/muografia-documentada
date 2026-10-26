# Muografía por transmisión asistida por aprendizaje profundo

Repositorio de código, evidencia experimental y documentación del trabajo de grado **«Reconstrucción muográfica por transmisión asistida por aprendizaje profundo mediante mejora predictiva de imágenes de baja estadística para exploración volcánica»**, del programa de Ingeniería de Sistemas de la Universidad Industrial de Santander (UIS), vinculado al Grupo de Óptica y Tratamiento de Señales (GOTS).

| Responsabilidad | Integrantes |
|---|---|
| Autores | Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega |
| Director | Andrés Leonardo González Gómez |
| Codirector | Jaime Enrique Meneses Fonseca |

## Propósito y alcance

La muografía por transmisión estudia la estructura interna de objetos extensos a partir de los muones cósmicos que los atraviesan. Cuando se registran pocos eventos, las imágenes presentan fluctuaciones de conteo que dificultan su interpretación. Este trabajo estudia si el aprendizaje profundo permite mejorar esas imágenes en escenarios volcánicos sintéticos, tomando como referencia imágenes con mayor estadística.

El repositorio reúne los datos documentados, las implementaciones, los procedimientos de evaluación y el informe académico. Permite examinar el método, consultar sus resultados y reproducir distintos niveles del análisis, desde figuras basadas en métricas archivadas hasta inferencia con modelos entrenados.

**Resultado principal:** U-Net y la red generativa adversaria condicional mejoraron la similitud de imagen, pero también alteraron los conteos regionales. **No se demostró un factor de reducción de adquisición frente al referente sin red al 50 % bajo el criterio adoptado, ni se reconstruyó opacidad cuantitativa.** Estos resultados delimitan el alcance del método en los escenarios y condiciones estudiados.

## Guía de consulta

- **Comprender el estudio:** consultar el [informe en PDF](informe-final/latex/main.pdf), versión archivada el 4 de octubre de 2026, o los capítulos de [metodología, resultados, discusión y conclusiones en Markdown](informe-final/README.md).
- **Consultar las fuentes del informe:** acceder al [proyecto LaTeX](informe-final/latex/README.md) y al [paquete para Overleaf](informe-final/latex/Trabajo_de_Grado_Muografia_corregido.zip).
- **Explorar los resultados:** revisar las tablas de este README y sus enlaces a las evaluaciones completas.
- **Reproducir el análisis:** comenzar por la ejecución rápida sin GPU y continuar, si se dispone de los insumos, con la evaluación de predicciones y modelos.
- **Examinar la trazabilidad:** consultar el [índice documental](docs/INDICE.md), la [procedencia de los materiales](docs/PROCEDENCIA.md) y el [registro de cambios](CHANGELOG.md).

Las carpetas se organizan por objetivo específico: **OE1**, generación del conjunto sintético; **OE2**, desarrollo y evaluación de modelos; **OE3**, comparación entre estadísticas de conteo y análisis de reducción de adquisición.

| Ruta | Contenido |
|---|---|
| `objetivo-1/` | Simulación, datos sintéticos, receta, correcciones y auditorías de integridad |
| `herramientas/` | Análisis, empaquetado y controles del conjunto sintético |
| `objetivo-2/implementacion/` | Implementación derivada de entrenamiento y evaluación |
| `objetivo-2/herramientas/` | Pilotos, ajustes, inferencia y evaluación final al 5 % |
| `objetivo-3/herramientas/` | Curvas de conteos, métricas locales y evaluación multifracción |
| `objetivo-*/evidencias/` | Informes, tablas, inventarios y huellas de las revisiones |
| `objetivo-*/entregas/` y `objetivo-1/originales/` | Materiales originales y versiones históricas para trazabilidad |
| `trabajo/` | Destino local recomendado para insumos y salidas; excluido de Git |

## Método y conjunto de datos

El flujo experimental comprende simulación de transporte con Geant4 y una fuente basada en Guan/EcoMug, construcción de imágenes de conteos direccionales, adelgazamiento binomial y aprendizaje supervisado. La implementación de aprendizaje utiliza **Python/PyTorch**. Se comparan una U-Net y una red generativa adversaria condicional de Wasserstein con penalización de gradiente (**cWGAN-GP**, identificada como cGAN en las tablas y archivos).

El [conjunto sintético documentado](objetivo-1/FICHA_CONJUNTO_OE1.md) contiene:

- 19 geometrías cónicas idealizadas, seis vistas por geometría y 114 referencias de 256 × 256 píxeles.
- 344 millones de primarios por vista y 39.216.000.000 en toda la campaña.
- Fracciones de conteos 1 %, 5 %, 10 % y 50 %, con veinte realizaciones por fracción: 9.120 pares.
- Partición por geometría: 12 de entrenamiento, 3 de validación, 3 de prueba y 1 de generalización. Todas las vistas y realizaciones de una geometría permanecen juntas.

Se evaluaron ocho modelos: `unet_original`, `cgan_original` y seis continuaciones cGAN `B1_C0`, `B1_C1`, `B2_C0`, `B2_C1`, `B3_C0`, `B3_C1`. Se entrenaron o continuaron al 5 %; la evaluación posterior en otras fracciones **no equivale a entrenamiento multifracción**.

## Resultados obtenidos

### Calidad de imagen y sesgo regional al 5 %

Valores de la [evaluación con corrección numérica C2](objetivo-2/evidencias/ef01-c2/resultados.json), redondeados para lectura. El índice de similitud estructural (**SSIM**) y la relación señal-ruido de pico (**PSNR**) comparan cada imagen con la referencia de alta estadística; valores mayores indican mayor similitud según estas métricas. **Q** resume sesgo regional de cuentas y no es error de densidad; un valor menor es preferible.

| Partición | Método | SSIM ↑ | PSNR [dB] ↑ | Q [%] ↓ |
|---|---|---:|---:|---:|
| Prueba | Entrada sin red | 0,764308 | 24,257520 | 1,8321 |
| Prueba | U-Net original | 0,854477 | 33,073913 | 22,3881 |
| Prueba | cGAN original | 0,834162 | 31,169869 | 14,5661 |
| Generalización | Entrada sin red | 0,750185 | 23,903636 | 1,0927 |
| Generalización | U-Net original | 0,845414 | 32,883414 | 26,5053 |
| Generalización | cGAN original | 0,825228 | 31,047417 | 16,9586 |

La prueba comprende tres geometrías y 360 imágenes por método; generalización, una geometría y 120 imágenes. Las veinte realizaciones de una vista no son geometrías independientes. La tabla muestra las bases originales; los seis modelos adicionales y sus compromisos están en las [tablas completas de los ocho modelos](objetivo-2/manuscrito/TABLAS_OE2.md). Una mejora de SSIM/PSNR no acredita conservación regional de cuentas.

### Reducción de conteos y alcance

- La cGAN original al 5 % superó SSIM y PSNR de la entrada sin red al 10 % en las 24 vistas y 480 correspondencias evaluadas; Q empeoró en las 24 vistas. La razón 2:1 es una **comparación descriptiva de conteos**, no un factor físico aceptado.
- La evaluación multifracción incluyó los ocho modelos en cuatro fracciones. Se reutilizaron 3.840 predicciones al 5 % y se añadieron 11.520, contenidas en 96 matrices nuevas.
- Ninguna de las 768 comparaciones modelo/fracción/vista satisfizo conjuntamente SSIM y PSNR del referente sin red al 50 %. El mínimo aceptado y el factor de reducción quedan **no demostrados**, no iguales a cero o a uno.
- Se calcularon la relación señal-ruido local (SNR), la relación contraste-ruido (CNR) y el contraste de cuentas; no se demostró conservación uniforme de las anomalías ni una inversión cuantitativa de opacidad.

El criterio de comparación (*benchmark*) exige alcanzar simultáneamente SSIM y PSNR del referente sin red al 50 %, usando medias de veinte realizaciones por vista. Se definió después de conocer resultados históricos y antes de las inferencias multifracción; no constituye un umbral prospectivo independiente. Fuentes: [comparación descriptiva](objetivo-3/RESULTADO_EXPERIMENTAL_OE3.md), [evaluación multifracción](objetivo-3/REVISION_COMPLEMENTO_OE3_C1.md) y [definición del criterio y alcance de las conclusiones](objetivo-3/CIERRE_OE3.md).

En la evaluación del conjunto sintético, 1.710 regiones de borde cumplieron el criterio adoptado y 107/114 vistas alcanzaron la meta descriptiva de roca. Se conservan las siete excepciones en la [ficha del conjunto](objetivo-1/FICHA_CONJUNTO_OE1.md).

## Preparación del entorno

Los comandos deben ejecutarse desde la raíz del repositorio. Para clonar se requiere Git y, mientras el repositorio sea privado, acceso autorizado:

```bash
git clone https://github.com/anlegogo/muografia-documentada.git
cd muografia-documentada
git rev-parse HEAD
git status --short
python -m venv .venv
```

Activación:

- Linux/Bash: `source .venv/bin/activate`
- Windows/PowerShell: `.\.venv\Scripts\Activate.ps1`

Los ejemplos se comprobaron en un entorno con Python 3.12.14, NumPy 2.4.4, Matplotlib 3.11.1, SciPy 1.18.1, scikit-image 0.26.0 y PyTorch 2.6.0+cpu. Se utilizó un entorno existente; **no se verificó una instalación nueva desde cero**.

Para análisis y figuras:

```bash
python -m pip install -r requirements-oe1-local.txt
```

Para las pruebas y evaluadores de aprendizaje, añadir:

```bash
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install scikit-image==0.26.0 filelock==3.32.3
```

Estas instrucciones preparan CPU. El entrenamiento e inferencia GPU requieren una instalación de PyTorch compatible con CUDA y el equipo; no instalar la variante CPU para una corrida GPU. Conservar `python --version`, `python -m pip freeze`, versión CUDA y dispositivo junto a cada ejecución. Los [requisitos CPU históricos](objetivo-2/requirements-cpu-verificado.txt) no son un entorno universal ni incluyen Geant4.

## Ejecución rápida: sin GPU ni datos externos

### Regenerar una figura desde las métricas archivadas

```bash
python objetivo-3/herramientas/figura_curvas.py --curves objetivo-3/evidencias/curvas-v1/curvas.json --models objetivo-2/evidencias/ef01-c2/resultados.json --output-dir trabajo/reproduccion-readme/curvas
```

Produce `curvas-exposicion.svg` y `curvas-exposicion.png` en el destino indicado. Este comando se comprobó sobre los archivos versionados de la base `e6f139e`. **Representa métricas ya calculadas**: no repite inferencia ni prueba de nuevo su validez física. Las líneas son descriptivas y los puntos de las redes corresponden al 5 %; no deben interpretarse como las predicciones multifracción del complemento.

### Ejecutar controles pequeños

```bash
python objetivo-2/herramientas/test_controles_contraste_v2.py
python objetivo-3/herramientas/test_comparar_exposiciones_oe3.py
python objetivo-3/herramientas/test_complemento_oe3.py
```

Estos tres archivos agrupan 16 pruebas de controles de contraste, comparaciones y métricas locales. Su ejecución fue satisfactoria en el entorno documentado; no requieren pesos ni simulación Geant4.

Las cinco pruebas adicionales del evaluador EF-01 necesitan el módulo de métricas en `PYTHONPATH`. En Linux/Bash:

```bash
PYTHONPATH=objetivo-2/implementacion/scripts/evaluation python objetivo-2/herramientas/test_evaluacion_final_oe2.py
```

En Windows/PowerShell:

```powershell
$env:PYTHONPATH = 'objetivo-2/implementacion/scripts/evaluation'
python objetivo-2/herramientas/test_evaluacion_final_oe2.py
```

Estas cinco pruebas se comprobaron con la ruta indicada y requieren permiso de escritura en la carpeta temporal del sistema. Si aparece `ModuleNotFoundError: No module named 'metrics'`, comprobar que `PYTHONPATH` apunte a la carpeta de evaluación y que el comando se ejecute desde la raíz del repositorio.

## Reproducción con datos y pesos externos

Clonar este repositorio **no descarga todos los datos, pesos ni predicciones**. Se deben recuperar las distribuciones indicadas en los documentos siguientes y verificar sus tamaños y SHA-256. Las auditorías enlazadas documentan verificaciones realizadas en octubre de 2026; la disponibilidad actual de cada distribución externa debe comprobarse antes de iniciar la reproducción.

| Insumo | Referencia y ubicación esperada |
|---|---|
| Datos OE1 | [Ficha y recuperación](objetivo-1/FICHA_CONJUNTO_OE1.md), [distribución verificada](objetivo-1/REVISION_DISTRIBUCION_DRIVE.md). Para inferencia: `DATA/dataset-v2/shards/`, cuatro shards test/gen y sus metadatos |
| Pesos originales | [Evaluación final: preparación](objetivo-2/INSTRUCCIONES_EVALUACION_FINAL_OE2.md) |
| Seis pesos B1–B3 | [Índice de artefactos E1](objetivo-2/INDICE_ARTEFACTOS_E1.md) |
| JSON de rutas de pesos | Copia local de [pesos-evaluacion-final-ejemplo.json](objetivo-2/configuraciones/pesos-evaluacion-final-ejemplo.json), con ocho rutas reales |
| Predicciones al 5 % | [Distribución y revisión C2](objetivo-2/REVISION_EVALUACION_FINAL_C2.md): 32 NPY, recibos, identidades y `completed.json`; aproximadamente 1,01 GB solo en matrices |
| Predicciones multifracción | [Complemento OE3](objetivo-3/INSTRUCCIONES_COMPLEMENTO_OE3.md) y [auditoría](objetivo-3/REVISION_COMPLEMENTO_OE3_C1.md): 96 NPY adicionales, aproximadamente 3,02 GB |

Usar directorios nuevos de salida y conservar fuentes, finales de línea, protocolos y manifiestos: los ejecutores verifican sus huellas. No reemplazar hashes para sortear discrepancias.

### Reevaluar las predicciones al 5 % con la corrección C2

Con los insumos anteriores, adaptar las cuatro rutas absolutas del comando:

```bash
python objetivo-2/herramientas/controles_contraste_v2.py --repo . --data /ruta/insumos --weights /ruta/pesos-evaluacion.json --predictions /ruta/evaluacion-final-f05 --report /ruta/nueva/revision-c2 --registry-in objetivo-2/evidencias/ef01-c2/controles.json
```

Genera el informe `evaluacion-final.json`, tablas y registro de controles usando los índices C2, sin entrenar modelos. La [documentación de la corrección C2](objetivo-2/REVISION_EVALUACION_FINAL_C2.md) describe el procedimiento y la evidencia de la reevaluación completa realizada en octubre de 2026. La ejecución rápida anterior no reproduce esa evaluación completa.

### Repetir inferencia o entrenamiento

- **Inferencia al 5 %:** seguir [preflight, infer y evaluate de EF-01](objetivo-2/INSTRUCCIONES_EVALUACION_FINAL_OE2.md). Para citar contrastes finales, aplicar después el corrector C2 anterior.
- **Inferencia multifracción:** seguir [OE3-C1](objetivo-3/INSTRUCCIONES_COMPLEMENTO_OE3.md), que exige datos, ocho pesos, predicciones completas al 5 % y registro C2. Ejecutar `preflight`, `smoke`, `infer` y finalmente `evaluate`, sin cambiar pesos o fracciones.
- **Entrenamiento desde cero:** seguir [piloto U-Net/cGAN](objetivo-2/INSTRUCCIONES_PILOTO_SC3.md), incluidas interrupción/reanudación y comprobación técnica antes de las 30 épocas máximas. El ejecutor requiere CUDA salvo prueba CPU explícita. El piloto no reproduce por sí solo las seis continuaciones; sus protocolos están en el [índice](docs/INDICE.md).
- **Datos reducidos:** la [ficha OE1](objetivo-1/FICHA_CONJUNTO_OE1.md#recuperación-y-reproducción) incluye comandos para evaluar histogramas y regenerar pares. Fijar NumPy 2.4.4 para la reproducción local de contenido documentada.
- **Transporte Geant4:** consultar [receta efectiva](objetivo-1/contratos/receta-operativa-siete-actividades.json) y [reproducción OE1](objetivo-1/REPRODUCCION.md). Se reportó Geant4 11.4.2, GCC 14.2.0 y FTFP_BERT en SC3. No se ofrece aquí una ejecución portátil de toda la campaña ni se certifica reconstrucción local exacta del binario de producción. Los scripts de clúster necesitan adaptación y no deben ejecutarse dentro de los originales preservados.

## Limitaciones y uso de los resultados

1. **Escenarios sintéticos e idealizados.** No son imágenes medidas en volcanes ni validación de un detector real. La fuente híbrida, transporte solo de primarios, cielo ideal y plano computacional de registro limitan la interpretación instrumental.
2. **Exposición convencional.** Las fracciones expresan conteos relativos. Las etiquetas de días no son tiempos calibrados de adquisición física; 5 % no demuestra automáticamente una reducción de 20 veces.
3. **Dependencia estadística.** Las referencias contienen ruido y las realizaciones reducidas derivan de esas referencias. Las vistas y realizaciones no sustituyen una mayor diversidad de geometrías.
4. **Reservas potencialmente expuestas.** Aunque los ocho modelos no se entrenaron ni seleccionaron con test/gen según la declaración recibida, las mismas escenas se conocían de una etapa anterior. La evaluación es descriptiva, no confirmatoria independiente. Véase [procedencia de reservas](objetivo-2/entregas/2026-10-04-evaluacion-final-f05/PROCEDENCIA_RESERVAS.md).
5. **Calidad visual y fidelidad física distintas.** Persisten sesgos regionales y compromisos entre métricas. No se acredita preservación general de detectabilidad ni reconstrucción de densidad/opacidad.
6. **Benchmark posterior y rejilla limitada.** El resultado negativo aplica al criterio y fracciones evaluados; no demuestra imposibilidad para cualquier modelo. No se interpoló un factor favorable.
7. **Materiales de producción.** El [diagnóstico de opacidad nominal](objetivo-3/OPACIDAD_NOMINAL_Y_ALCANCE.md) registra una discrepancia entre la densidad nominal 0,048 g/cm³ y el reemplazo por G4_AIR para valores menores de 0,05 en el constructor conservado. No se acredita la densidad efectiva del binario ejecutado.
8. **Reproducción condicionada.** Las distribuciones externas, versiones y huellas son necesarias. Pasar pruebas unitarias no equivale a repetir la campaña, el entrenamiento o la validación física.

## Procedencia, atribución y licencia

Los registros distinguen la generación de datos, el entrenamiento, las evaluaciones y las correcciones numéricas. Para citar resultados deben identificarse la versión del conjunto, el modelo y el protocolo de evaluación. Los valores de versiones anteriores no deben combinarse con los del conjunto corregido y C2. La trazabilidad puede consultarse en [procedencia](docs/PROCEDENCIA.md) y en las síntesis de [datos](objetivo-1/CIERRE_OE1.md), [modelos](objetivo-2/CIERRE_OE2.md) y [evaluación de adquisición](objetivo-3/CIERRE_OE3.md).

El repositorio no incluye actualmente un archivo de licencia general en su raíz. El acceso al contenido no implica una autorización general de reutilización; deben consultarse los permisos correspondientes y conservarse las atribuciones y condiciones de los componentes de terceros. Las distribuciones externas de datos y pesos tienen permisos de acceso propios.

