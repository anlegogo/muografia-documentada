# Acuerdo y condiciones de ejecución de la campaña de 114 vistas

2026-10-02 (Colombia). Constancia previa al envío, conforme al paso 2 de la sección 7 de [PREPARACION_CAMPANA_114.md](../../PREPARACION_CAMPANA_114.md). Se registra antes de enviar cualquier trabajo de la campaña.

## Acuerdo

Acordado con la dirección el 2026-10-02, en el grupo de comunicación del proyecto, tras recibir los resultados del piloto ([RESULTADOS_PILOTO_V2.md](RESULTADOS_PILOTO_V2.md)) y la prueba en la partición `amd`:

- **N fijo de 344 millones de primarios por vista** para las 114 vistas (19 geometrías × 6 vistas). Se usa el [manifiesto candidato](../../evidencias/preparacion-campana-114/manifiesto-114-344M.csv) sin cambios: 1.026 bloques, nueve por vista, de unos 38,22 millones cada uno, con semillas nuevas. SHA-256 `f5180881a003336fa5515e5ce74d2e056ca93a7f457db97c4931e2fc33f19a4a`.
- **Meta descriptiva de roca:** que al menos el 90 % de las ROI de roca evaluadas alcance 100 cuentas.
- **Resultados insuficientes:** una vista que quede por debajo de la meta se conserva y se reporta. No se aumenta N ni se descartan imágenes para alcanzarla, ni se modifica la regla de evaluación tras conocer los resultados.
- **Coste:** 39.216 millones de primarios. Equivalen a unas 5.936 h-núcleo de `legacy` según el piloto ([presupuesto.json](../../evidencias/preparacion-campana-114/presupuesto.json)). En `amd`, con la tasa medida, se estiman unas 2.100 h-hilo.
- **Partición `amd`:** acordada para completar la campaña en unas 10–12 horas de reloj, en lugar de las ~60 horas de `legacy`.

## Desvíos operativos respecto de la guía

La guía indica no modificar el lanzador y usar trabajos de 24 núcleos. Para ejecutar en `amd` se aplicaron los siguientes cambios, que no alteran la receta física, el manifiesto, el worker, el script SLURM ni la ficha:

| Cambio | Motivo | Evidencia |
|---|---|---|
| El lanzador acepta `--particion`, `--tiempo` y `--memoria`. Sin esas opciones genera el mismo comando `sbatch` que antes. Las tres quedan registradas en cada comando planificado y fuera de la identidad de campaña | La partición estaba fija en `legacy`, y `amd` asigna por defecto 1,5 GB por núcleo (96 GB para 64 hilos), lo que impedía compartir los nodos | Commits `bdfd4ba` y siguiente |
| **64 hilos por trabajo**, `--particion amd`, `--tiempo 00:15:00`, `--memoria 8G` | Un bloque de 38,22 M tarda unos 2 min en `amd` con 64 hilos. El consumo medido en `legacy` es de unos 200 MB por trabajo (`MaxRSS`, trabajos 30643 y 30683) | [prueba-amd](datos/sc3/prueba-amd/) |
| Prueba de portabilidad | El mismo bloque de 5 M dio histogramas con corte, sin corte y de generación idénticos byte a byte en `legacy` con 24 hilos (30683, 112,9 s) y en `amd` con 64 (30684, 14,9 s) | `1426aa2` |

Procesadores, según `lscpu`: `legacy` usa Intel Xeon E5645 (12 núcleos físicos y 24 hilos por nodo); `amd` usa AMD EPYC 9554 (exadell) y 9534 (smexa), con 128 núcleos físicos y 256 hilos por nodo.

**Pendiente declarado:** las pruebas unitarias del lanzador modificado no se ejecutaron. Sustituyen esa verificación el plan sin `--enviar`, `sbatch --test-only` y la prueba de portabilidad, que se hizo con el lanzador modificado.

## Ejecución

- Réplica en SC3 extraída con `git archive` del commit que contiene este documento. No se edita durante la campaña.
- Raíces nuevas: `~/muography-scratch/oe1-114-344M-{intentos,publicados}`. El piloto y sus recibos se conservan sin cambios.
- Intérprete: el envoltorio `~/oe1-trabajo/entorno/python-oe1` (D-01).
- Una pasada del lanzador por minuto mientras haya filas pendientes. Se detiene si aparece una fila en `blocked_prior_attempts` o si el lanzador termina con error. Un fallo se concilia con `sacct` antes de cualquier reintento; no se borran registros.
- Al terminar: fusión, evaluación con `evaluar_campana_114.py`, exportación e inventario, con los comandos de la guía. Los 9.120 pares se forman solo después de revisar la calidad.
