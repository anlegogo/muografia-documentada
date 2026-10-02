# Regiones de análisis con la malla nueva

**Integración posterior:** disponible el [analizador de conteos por región](ADAPTACION_LECTURA_ANGULAR.md#análisis-integrado-de-regiones-candidatas), con controles de compatibilidad. Las regiones conservan su estado de candidatas.

2026-10-01, Colombia. **Estado: regiones geométricas candidatas calculadas y contrastadas; no son máscaras congeladas de un nuevo ensayo.** Continúa la [adaptación de lectura](ADAPTACION_LECTURA_ANGULAR.md).

Una región de análisis selecciona los píxeles desde los cuales se observa una zona concreta del modelo. Al cambiar los ángulos centrales de los píxeles se debe volver a calcular esa selección, en lugar de copiar la máscara anterior.

## Avance local

La herramienta [preparar_roi_angular_v1.py](../herramientas/preparar_roi_angular_v1.py) calcula la longitud de intersección de cada rayo central con la zona común al conducto y al cuerpo denso de **geo-train-06**, para sus seis vistas. Usa intersecciones analíticas de un cilindro vertical finito y un elipsoide; no reutiliza la función de los estudiantes para producir los resultados. Está limitada mediante SHA-256 a esta geometría auditada.

Los rayos rectos parten del detector a 1.000 m del eje y altura 1,5 m, tienen 3.000 m de longitud máxima, y usan las coordenadas de `az-edges-v1`. Se marca el píxel cuando la longitud dentro de la intersección es al menos 20 m, conservando ese criterio geométrico previo sin optimizarlo a partir de conteos. **No simula trayectorias dispersadas ni cuenta detecciones.** No aplica a las otras geometrías ni resuelve sus recortes o prioridades de materiales.

Se generan NPZ con mapa de longitudes, máscara booleana, centros y bordes explícitos, junto con un resumen versionado y huellas. Solo se crean directorios nuevos. No se exporta una máscara textual que pueda confundirse con la ROI congelada de A/B; el ejecutable angular sigue rechazando aquel modo de listas hasta completar su versionado.

| Vista | Píxeles nuevos | Píxeles recalculados con centros antiguos | Celdas que cambian |
|---|---:|---:|---:|
| 0 | 193 | 194 | 1 |
| 1 | 181 | 181 | 0 |
| 2 | 164 | 162 | 2 |
| 3 | 161 | 162 | 1 |
| 4 | 182 | 182 | 0 |
| 5 | 181 | 181 | 0 |

La tercera columna es un **recálculo analítico con centros antiguos**, no la máscara histórica congelada. Esta última tiene 195 píxeles en vista 0. El recálculo antiguo difiere de ella en la celda `[23,133]`, cuya longitud analítica es 19,6805995 m: está por debajo del umbral de 20 m, pero figura incluida en la máscara congelada. Por tanto, la diferencia 195 → 193 no se atribuye íntegramente al cambio angular: una celda difiere por el recálculo geométrico y otra por los nuevos centros. No se modifican retrospectivamente la máscara ni el criterio estadístico del ensayo ya ejecutado.

## Verificación

- Ocho pruebas con cuerdas de longitud conocida: diámetro, tapas del cilindro, origen interior, rayo que se aleja, rayo fuera del volumen, tangencia, límite impuesto por el elipsoide, rechazo de direcciones no unitarias y orientación de las seis vistas (algunos casos se agrupan en una prueba).
- Contraste de **393.216 rayos** con `crossing_reference.py` de estudiantes, versión recibida `d8ca749`, mediante su formulación de mínima distancia. Las seis máscaras coinciden exactamente; diferencia máxima de longitudes **1,33 × 10⁻¹⁰ m**. Es un contraste de geometría analítica, no una ejecución de Geant4.
- Comparación de la ROI histórica con su huella congelada, sin cambiarla.

[Resumen por vista](evidencias/roi-angular-v1-resumen.json), [contraste independiente y máscara histórica](evidencias/roi-angular-v1-contraste.json), [pruebas locales](evidencias/pruebas-roi-angular-v1.txt).

## Reproducción

Desde la raíz de la réplica, con Python y NumPy:

```console
python herramientas/preparar_roi_angular_v1.py --metadatos-malla RUTA/geo-train-01_view0.meta.json --salida NUEVA_CARPETA
python -m unittest discover -s herramientas -p test_roi_angular_v1.py -v
```

El metadato de la entrega angular se usa **solo como plantilla de malla**, no como geometría ni como conteos. La herramienta lee geo-train-06 del catálogo conservado y registra su huella; los 750 conteos de geo-train-01 no participan en este cálculo. Los NPZ derivados pueden regenerarse con el comando y se mantienen fuera de los originales.

Para repetir el contraste: construir segmentos `[origen, origen + 3000 × dirección]` con `rays`, evaluar `crossing_reference.model(segmentos)["len"]` y comparar con `length_z_m`; aplicar en ambos el umbral `>=20`. La huella de esa referencia externa está registrada en la evidencia. No se trata de un resultado inferido únicamente de la cantidad de píxeles.

## Qué sigue pendiente

Integrar las máscaras nuevas en los consumidores de la malla y fijar su uso antes de cualquier análisis nuevo; mantener bloqueada la mezcla con las máscaras históricas. El empaquetado definitivo todavía requiere comprobar versiones de todas las vistas. La aceptación del plano de 600 m y la normalización temporal continúan pendientes. Este avance no exige otra corrida SC3, no aumenta la estadística del ensayo y no cierra el OE1.
