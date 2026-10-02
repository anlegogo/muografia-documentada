# Control local del muestreo angular

**Corrección preparada:** [malla azimutal v1](correcciones/malla-angular-v1/README.md). Parche separado, seis pruebas Python satisfactorias; compilación C++ y verificación de integración en Geant4 pendientes.

Revisión del director: 2026-10-01, Colombia. **Estado: verificado para el generador y su discretización sin transporte; validación física parcial.** Continúa la [preparación de producción](PREPARACION_PRODUCCION_OE1.md). No requiere SC3 ni modifica código o datos originales.

## Resultado

Se identificó una diferencia entre la distribución horizontal nominal que origina las tablas y la distribución que produce el generador al asignar direcciones a píxeles. Las dos columnas extremas reciben aproximadamente la mitad de la probabilidad nominal; las otras 254 reciben aproximadamente un 0,392 % más. La probabilidad total se conserva: **no es una pérdida del 50 % de todos los muones**.

Esto es una propiedad de los intervalos angulares de la fuente, antes del transporte. No demuestra que las imágenes finales tengan exactamente esos porcentajes: dispersión, absorción y aceptación espacial modifican las direcciones y los conteos. No se deben corregir los histogramas históricos multiplicando sus columnas por estos cocientes.

## Derivación reproducible

El [generador](originales/scripts/simulation/geant4_app/src/PrimaryGeneratorAction.cc) muestrea azimut relativo uniforme entre −30° y +30°. El [contador](originales/scripts/simulation/geant4_app/src/SteppingAction.cc) utiliza 256 centros incluidos ambos extremos y redondea al centro más cercano. Son las mismas expresiones revisadas en el código de etapa 2 `d8ca749`; el modo de lista reproduce las direcciones congeladas, no vuelve a muestrearlas durante A/B.

La separación de centros es 60°/255. Cada celda interior tiene ese ancho; la intersección de cada celda extrema con el soporte del generador tiene la mitad. Por ello:

| Columna | Probabilidad nominal uniforme | Probabilidad del generador | Cociente |
|---|---:|---:|---:|
| Primera o última | 1/256 | 1/510 | 0,5019608 |
| Cualquiera de las 254 interiores | 1/256 | 1/255 | 1,0039216 |

La referencia nominal se obtiene de [build_generator_tables.py](originales/scripts/analysis/build_generator_tables.py): verifica que el mapa de cielo abierto sea constante por azimut y suma las 256 columnas en cada peso de fila. El [surrogate](originales/scripts/simulation/surrogate/imaging.py) asigna a todos esos centros el mismo ancho azimutal al calcular el ángulo sólido. No hay un factor de media celda en sus columnas extremas.

Se comprobaron las probabilidades mediante intersección analítica de intervalos y una cuadratura independiente de **1.044.480 direcciones**, sin números aleatorios. Coinciden con error máximo 1,39 × 10⁻¹⁷. La distancia de variación total respecto de 256 columnas equiprobables es 0,00389093: un 0,3891 % de masa de probabilidad redistribuida. No es un porcentaje de error en la transmisión del volcán.

En elevación, el generador elige una fila con los pesos tabulados y añade medio paso a ambos lados del centro. Su soporte es aproximadamente **1,9117645° a 47,0882355°**, aunque los centros se anuncien entre 2° y 47°. Esto es coherente con interpretar esos números como centros, no como límites estrictos. El redondeo decimal de las tablas produce diferencias minúsculas: probabilidad fuera de las celdas de aproximadamente 1,0 × 10⁻⁸ y diferencia máxima por fila de 1,95 × 10⁻⁸. No se equiparan esos efectos diminutos con la diferencia azimutal de las columnas extremas.

## Decisión que esta revisión permite preparar

Antes de producción se debe declarar una única convención de **centros, bordes y dominio angular**, y aplicarla al cálculo de tasas, a la generación y al histograma:

- Si se conservan los centros actuales y celdas completas, el dominio azimutal sería aproximadamente −30,117647° a +30,117647°. Cambiaría el soporte de la fuente y exige revisar la normalización y el significado de la apertura declarada.
- Si se conservan límites estrictos de −30° a +30°, las celdas de borde tienen menor ancho, o debe redefinirse la malla de centros y bordes. Los pesos por columna deben corresponder a esa elección.

Son alternativas de diseño, no correcciones ya aplicadas. El área efectiva, la proyección angular y la justificación del plano de 600 m siguen siendo cuestiones distintas. El resultado no invalida la comparación A/B realizada con primarios compartidos ni cambia su intervalo; limita la afirmación de que ambos motores comparten *exactamente* la misma distribución angular discretizada.

Si se cambia fuente, malla o aceptación, deberá revisarse la compatibilidad de **las 114 vistas**, incluidas las 78 inicialmente candidatas a reutilización. El alcance de 36 vistas era condicional a mantener la definición del conteo. No se ha ordenado repetir toda la campaña.

## Evidencia y reproducción

- [Resultado y huellas de fuentes](evidencias/muestreo-angular/auditoria-angular.json).
- [Probabilidades de las 256 columnas](evidencias/muestreo-angular/probabilidades-azimut.csv).
- [Herramienta de auditoría](../herramientas/auditar_muestreo_angular.py).

Desde la raíz de la réplica, con Python y NumPy:

```console
python herramientas/auditar_muestreo_angular.py --salida objetivo-1/evidencias/muestreo-angular
```

La herramienta implementa explícitamente las constantes y reglas leídas en el código y guarda las huellas de las fuentes históricas. Si esas fuentes cambian, hay que revisar las constantes y el modelo del control; no es un intérprete automático de C++. No prueba la respuesta de Geant4 ni la aceptación de un detector real. P-04 permanece abierto, con una discrepancia concreta ya cuantificada.
