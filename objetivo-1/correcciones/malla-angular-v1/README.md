# Corrección propuesta: malla azimutal v1

2026-10-01, Colombia. Preparada por el director a partir del trabajo de los estudiantes. **Implementada y probada localmente en Python; compilación C++ y ejecución Geant4 pendientes. No habilita producción definitiva.**

## Cambio concreto

Se conserva la apertura azimutal de −30° a +30° y se divide en **256 intervalos de 0,234375°**. Los centros quedan entre −29,8828125° y +29,8828125°. Cada celda incluye su borde izquierdo y excluye el derecho; el último borde +30° se acepta en la última celda. Ángulos fuera de la apertura y valores no finitos se rechazan.

El generador ya muestrea uniformemente esa apertura: su fórmula no necesita cambiar. Cambian la asignación de dirección a columna en Geant4 y los centros que usa el surrogate. La malla de elevación conserva su convención histórica de centros, declarada por separado. Esta corrección aborda la [discrepancia azimutal](../../CONTROL_MUESTREO_ANGULAR.md), no la aceptación física del plano de 600 m.

También cambia el ancho azimutal usado en las tasas: de 60/255 a 60/256. Para las tablas históricas de cielo abierto, constantes en azimut, los pesos de fila se multiplican por **255/256**. La suma pasa de 36.175.379,99 a **36.034.069,911914065**, una disminución del 0,390625 %. Es consistencia con la convención de área efectiva existente; no certifica que esa suma equivalga físicamente a 30 días. Las probabilidades relativas de las filas, espectros y razón de carga se conservan.

## Entregables y protección de lo histórico

- [Parche revisable](correccion.patch), sobre el commit exacto `d8ca7499df6a8ec69eeb73843a245e0661c38220` del repositorio de estudiantes. Diez archivos nuevos o modificados; no altera geometrías, datos históricos ni resultados del ensayo.
- [Manifiesto de verificación](verificacion.json), con huellas antes/después y del parche.
- [Resultado de seis pruebas locales](pruebas-locales.txt).

El parche incorpora un encabezado C++ común para el contador y su prueba independiente; actualiza metadatos, surrogate y constructor de tablas; incluye un conversor de tablas auditadas y las pruebas Python. Los metadatos identifican `az-edges-v1`.

El ejecutable nuevo exige tablas con esa versión y apertura. El conversor exige las tres huellas históricas conocidas y un directorio nuevo: rechaza entradas modificadas, doble conversión y sobrescritura. El constructor desde surrogate exige una vista nueva con metadatos de la malla y exposición convencional de 30 días.

El modo de transporte de listas congeladas OE1 queda **rechazado expresamente en este prototipo**, porque las máscaras ROI y sus formatos no están versionados para la nueva malla. Usar los ejecutables históricos para reproducir A/B. No aplicar el parche a una rama de entrega congelada ni reutilizar máscaras, mapas de opacidad, figuras o histogramas como si sus centros fueran los nuevos. Las herramientas auxiliares de representación y empaquetado deben adoptar estos metadatos antes de producción; este parche no certifica toda esa cadena.

## Qué comprobamos aquí

1. Centros azimutales nuevos y elevación conservada.
2. 1.048.576 direcciones uniformes: **4.096 en cada una de las 256 columnas**, sin déficit en los extremos.
3. La función real de conteos del surrogate, bajo flujo constante controlado, integra el ancho total de 60°.
4. Conversión de tablas, preservación exacta del espectro y rechazo de sobrescritura/doble escalado.
5. Rechazo de metadatos históricos por el constructor de tablas.
6. Lectura correcta de una vista nueva sintética con metadatos compatibles.

Se comprobó `git apply --check`, se aplicó en una copia de archivos base y se verificaron las diez huellas resultantes. La primera comprobación byte a byte encontró conversión CRLF de Git en Windows; se repitió en carpeta nueva con `core.autocrlf=false` y todas las huellas coincidieron. Python 3.12.14, NumPy 2.4.4; el surrogate importa SciPy. No se encontró compilador C++ en PATH ni entorno Geant4 local: su prueba está preparada, **no ejecutada**.

## Aplicación y verificación por los estudiantes

En una copia limpia del repositorio fuente, crear una rama de propuesta desde el commit indicado. Guardar este parche fuera de la copia y sustituir `RUTA_AL_PARCHE` por su ruta real:

```bash
git switch -c propuesta/malla-angular-v1 d8ca7499df6a8ec69eeb73843a245e0661c38220
git -c core.autocrlf=false apply --check RUTA_AL_PARCHE
git -c core.autocrlf=false apply RUTA_AL_PARCHE
python scripts/analysis/test_angular_grid_v1.py -v
python scripts/analysis/convertir_tablas_azimut.py scripts/simulation/geant4_app/tables scripts/simulation/geant4_app/tables-az-edges-v1
c++ -std=c++17 -I scripts/simulation/geant4_app/include scripts/simulation/geant4_app/tests/test_azimuth_grid.cc -o test_azimuth_grid
./test_azimuth_grid
```

La prueba C++ usa el mismo encabezado que Geant4 y comprueba límites, centros, bordes, valores inválidos y el millón de direcciones. Ambas pruebas deben pasar antes de compilar el simulador. En el entorno Geant4 11.4.2 documentado de SC3:

```bash
cmake -S scripts/simulation/geant4_app -B build-az-edges-v1
cmake --build build-az-edges-v1 -j 2
mkdir -p results/angular-v1-smoke
if build-az-edges-v1/muography_sim --geometry scripts/simulation/geometry_catalog/geometries/geo-train-01.json --view 0 --tables scripts/simulation/geant4_app/tables-az-edges-v1 --seed 2026100107 --events 1000 --threads 1 --out results/angular-v1-smoke > results/angular-v1-smoke/run.log 2>&1; then
  printf "0\n" > results/angular-v1-smoke/exit_code.txt
else
  run_status=$?
  printf "%s\n" "$run_status" > results/angular-v1-smoke/exit_code.txt
fi
```

Esta única corrida de **1.000 primarios** comprueba integración del programa: terminación satisfactoria, ausencia de errores, histograma 256×256, conteos enteros no negativos con suma ≤1.000, y metadatos de nueva malla y número generado. No exigir columnas uniformes después del transporte ni interpretar 1.000 eventos como una prueba física de precisión. Conservar comando, versiones, huella del ejecutable, tablas, log e histograma. Reportar fallos antes de ampliar N.

Después de la revisión de esa entrega: adaptar consumidores/ROI y validar el plano de conteo y la exposición. Solo entonces decidir qué vistas regenerar. Los resultados A/B históricos permanecen válidos para su protocolo anterior; la nueva malla requiere una versión distinta del conjunto de datos.

## Revisión automática de la entrega

Quedó preparado el [revisor de la corrida](../../../herramientas/revisar_smoke_angular.py). En una carpeta nueva de entrega conservar los cuatro archivos de salida: `geo-train-01_view0.meta.json`, `geo-train-01_view0_hist.csv`, `run.log` y `exit_code.txt`. El bloque anterior captura el código real inmediatamente al terminar el simulador. No escribir cero manualmente para reemplazar una ejecución fallida ni reutilizar la carpeta de una corrida anterior.

Desde la raíz de **muografia-documentada**, usando Python estándar:

```console
python herramientas/revisar_smoke_angular.py RUTA_ENTREGA --salida revision-angular.json
python -m unittest discover -s herramientas -p test_revisar_smoke_angular.py -v
```

El revisor comprueba identidad del caso, semilla, un hilo, 1.000 primarios generados y transportados, versión y parámetros de malla, dimensiones del histograma, conteos enteros no negativos, coincidencia de su suma con metadatos, código de salida y marca de finalización. Señala patrones conocidos de error del log y registra SHA-256 de los cuatro archivos. El informe de salida debe ser nuevo; se rechaza sobrescribirlo. Devuelve código 0 si esos controles pasan y 1 si requieren revisión.

[Ocho pruebas del revisor](pruebas-revisor-smoke.txt) verifican una entrega sintética conforme y casos de error: malla antigua, número de eventos incorrecto, valores no enteros/negativos, histograma truncado, terminación fallida, advertencia Geant4 y log ausente. **No son una entrega de los estudiantes ni una ejecución de Geant4.**

Un resultado conforme solo acredita coherencia de los archivos presentados. La compilación, versiones reales, código utilizado, huella del ejecutable, tablas y ausencia de otros errores del log deben revisarse por separado. La aceptación física y el plano de 600 m continúan pendientes; este control no declara cerrado el OE1.
