# Entrega: malla azimutal v1, corrida de integración de 1.000 primarios

2026-10-01. Procedimiento: [instrucciones del director](../../correcciones/malla-angular-v1/README.md), sin cambios ni ampliaciones.

## Código

- Repositorio `Dp100131/muography-dl-reconstruction`, rama `propuesta/malla-angular-v1` creada desde `d8ca7499df6a8ec69eeb73843a245e0661c38220`.
- Commit `0dea8e1e1f8ad1e52ee2024e4c6c968748214a32`: parche del director aplicado con `git -c core.autocrlf=false apply` (huella del parche `8af72133…6be8ce`) y tablas convertidas a `tables-az-edges-v1`. Las diez huellas resultantes coinciden con `verificacion.json`. No se modificó otro archivo.

## Pruebas previas

| Prueba | Resultado | Evidencia |
|---|---|---|
| `test_angular_grid_v1.py` (Python 3.13.5, local) | 6/6 OK | [pruebas-python.txt](pruebas-python.txt) |
| `test_azimuth_grid` (GCC 14.2.0, SC3): límites, centros, bordes, valores inválidos, 1.048.576 direcciones | PASS | [prueba-cpp.txt](prueba-cpp.txt) |
| Conversión de tablas | escala de filas 0,99609375; suma 36.034.069,911914065 | `tables-az-edges-v1/meta.json` en la rama de código |

## Corrida

- Compilación en `guane` con `gnu14/14.2.0` + `geant4/11.4.2` (`cmake --build -j 2`), sin errores.
- SLURM **30616**, partición `legacy`, nodo `guane01`, 1 CPU, estado `COMPLETED 0:0`, 5 s. Script: [smoke_angular_v1.sbatch](smoke_angular_v1.sbatch); salida: [slurm-30616.out](slurm-30616.out); [sacct-30616.txt](sacct-30616.txt).
- Comando: [corrida/comando.txt](corrida/comando.txt) (geo-train-01, vista 0, semilla 2026100107, 1.000 eventos, 1 hilo). Entorno: [corrida/entorno.txt](corrida/entorno.txt). Huellas de ejecutable (`a29e5277…a76e008b`), geometría y tablas: [corrida/entradas.sha256](corrida/entradas.sha256).

## Criterios

| Criterio | Resultado | Evidencia |
|---|---|---|
| a. 1.000 muones completados | Cumple: `RUN DONE … events=1000`, `events_transported=1000`, `ecomug_draws_total=1000`, código de salida 0 | `run.log`, `meta.json`, `exit_code.txt` |
| b. Nueva malla utilizada | Cumple: `azimuth_convention=az-edges-v1`, `n_az=256`, `az_step_deg=0.234375` (60/256), bordes `[-30, 30]`, primer centro −29,8828125 | `meta.json` |
| c. Conteos coherentes | Cumple: histograma 256×256, suma = 750 = `detected_in_bins` = `detected` del log | `hist.csv`, `meta.json`, `run.log` |

Revisor automático (`herramientas/revisar_smoke_angular.py`): **24 controles, 0 fallidos**, código 0. Informe: [revision-angular.json](revision-angular.json). Las ocho pruebas del revisor también pasan.

Alcance: corrida de integración. No evalúa uniformidad por columna tras el transporte, precisión física, plano de 600 m ni exposición.

Huellas de todos los archivos de la entrega: [SHA256SUMS](SHA256SUMS).
