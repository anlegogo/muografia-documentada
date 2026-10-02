# Verificación y reproducción del OE1

**Estado consolidado:** consultar [cadena local preparada](CADENA_LOCAL_OE1.md). Lectura, representación, ROI y empaquetado nuevos implementados; las descripciones de pasos pendientes anteriores en esta página son históricas. Validación física y producción final aún abiertas.

## Verificar la copia recibida

Desde la raíz de esta réplica, con Python 3.9 o superior:

```powershell
python herramientas/verificar_integridad.py
```

Usa solo la biblioteca estándar. Comprueba presencia, tamaños y SHA-256 de todos los archivos incorporados, las huellas de los 19 shards contra el manifiesto de autores, 114 vistas contra sus metadatos, totales de campaña y ausencia de geometrías repetidas entre particiones. Escribe únicamente `objetivo-1/evidencias/verificacion-local.json`. No ejecuta simulaciones ni modifica datos. No verifica la corrección física.

## Entorno científico

El transporte requiere Geant4 y compilador C++17/CMake; SC3 declara Geant4 11.4.2. Docker recibido usa v11.3.2 y no se ha validado como reproducción exacta. Los análisis Python importan NumPy, SciPy, Matplotlib y scikit-image; el módulo de datos incluye soporte opcional de PyTorch. No se copia el requirements global de entrenamiento como requisito obligatorio del OE1.

El entorno de auditoría existente está fuera de esta réplica, en `../tmp/muography-audit-venv/`. La verificación de integridad no depende de él. No se ha creado ni probado una instalación científica autónoma nueva.

## Regeneración futura en una copia de trabajo

Crear una copia separada del contenido de `originales/`. Los siguientes comandos son los puntos de entrada recibidos y **sobrescriben resultados en esa copia**; no ejecutarlos dentro de los originales preservados.

```powershell
# En la raíz de la copia de trabajo:
$env:MUOGRAPHY_ENGINE = 'geant4'
python scripts/analysis/build_dataset.py
python scripts/analysis/partition_freeze.py
```

La construcción calcula además estadísticas base sobre las geometrías disponibles. `partition_freeze.py` escribe un nuevo manifiesto; conservar el recibido para comparar, y no presentar el nuevo sello como el congelamiento histórico.

Para Geant4 consultar CMake, Docker y scripts SC3 incluidos. El script histórico `make_sc3_bundle.sh` presupone que las rutas `scripts/…` están en la raíz del historial Git original: no se puede ejecutar directamente desde esta selección anidada. Requiere preparación de un entorno de ejecución independiente. Los scripts SC3 dependen de módulos y rutas del clúster.

En la incorporación inicial solo se verificó la copia. En la revisión posterior se regeneraron en memoria los 9.120 pares, sin escribir sobre los originales: véase [revisión de datos](REVISION_DATOS.md). No se han regenerado campañas Geant4. Los faltantes y diferencias de entorno están en [pendientes](PENDIENTES.md).

La herramienta `auditar_oe1.py` requiere NumPy; el comparador del piloto también. El ejecutor SLURM necesita Bash y el entorno Geant4 de SC3. Consultar las [instrucciones](INSTRUCCIONES_ESTUDIANTES.md) antes de ejecutar.

Controles pequeños de las herramientas nuevas: `python herramientas/test_herramientas_oe1.py`. Utilizan datos sintéticos de prueba; no ejecutan Geant4. La sintaxis del ejecutor puede comprobarse con `bash -n herramientas/ejecutar_piloto_oe1.sbatch`; pasar esa comprobación no acredita compatibilidad con la configuración de SC3.
