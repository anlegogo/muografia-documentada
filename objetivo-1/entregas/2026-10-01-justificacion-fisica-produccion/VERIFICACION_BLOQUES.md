# Verificación de los dos bloques existentes con las herramientas de la dirección

2026-10-02. Se atiende la instrucción de [CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md](../../CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md): aplicar las herramientas a los dos bloques existentes, guardar los informes de fusión y de exportación, comprobar las cifras 200.000 / 69.995 / 130.190 y documentar la versión utilizada.

**No se simularon muones nuevos.** Las herramientas se usaron sin modificar.

## Resultado

| Magnitud | Esperado | Obtenido | Fuente |
|---|---:|---:|---|
| Primarios transportados | 200.000 | **200.000** | `revision-fusion.json`, `events` |
| Registros con E_cin > 3 GeV | 69.995 | **69.995** | `counts`; también la exportación (`total`) |
| Registros de todas las energías | 130.190 | **130.190** | `all_energy_counts`; metadato `detected_all_energies` |

Las tres cifras coinciden. La fusión se ejecutó **sin `--aceptar-crlf`**, sobre los bytes originales de SC3: las cuatro huellas de salida declaradas por los bloques coinciden exactamente (`crlf_to_lf_verified=false`). Como comprobación independiente, sumar directamente los CSV versionados de ambos bloques da también 69.995 (imagen con corte) y 130.190 (sin corte). La media de energía de todos los registros es 17,8362621 GeV, igual a la reportada por la dirección. El metadato fusionado conserva `exposure_days=-1`.

La publicación verificada de las filas 108 y 109 devolvió `published` en ambos casos, y la repetición de la fila 108 devolvió `already_verified`. Las huellas de los bloques de origen antes y después de la ejecución son idénticas.

## Ejecución

- **SLURM:** trabajo 30631, partición `legacy`, nodo guane01, 2 CPU, COMPLETED 0:0, 5 s (2026-10-02 09:45:41–09:45:46, hora de Colombia). [sacct](datos/sc3/verificacion-c4b6e4c/sacct-30631.txt).
- **Comando de lanzamiento:** `srun -p legacy -N1 -n1 -c2 -t 00:10:00 --job-name=oe1-verificacion bash verificar_bloques.sh`. [Script](verificacion/verificar_bloques.sh) y [copia ejecutada](datos/sc3/verificacion-c4b6e4c/verificar_bloques.sh).
- **Entorno:** `~/muography-train/venv/bin/python`, con Python 3.13.13 y NumPy 2.5.2. Módulos cargados por defecto en el nodo: gnu14/14.2.0, openmpi5/5.0.7, entre otros. No se carga Geant4, porque no se simula. [entorno.txt](datos/sc3/verificacion-c4b6e4c/salidas/entorno.txt).
- **Herramientas:** `herramientas/` del commit `c4b6e4c` de `main`, copiadas con `git archive` sin cambios. Huellas SHA-256: `fusionar_bloques_angular.py` ac456164…, `publicar_bloque_angular.py` 15dcd116…, `preparar_imagen_angular_v1.py` 61e2e4e6… y `configuracion_angular.py` 35099a36…, todas iguales a las de Git. [Lista completa](datos/sc3/verificacion-c4b6e4c/salidas/herramientas.sha256).
- **Manifiesto:** `/home/dapintoo/oe1-trabajo/produccion-v1/manifiesto-prueba.csv`, SHA-256 `1d0594c3…`, idéntico al blob versionado en `datos/sc3/prueba-integracion/`.
- **Bloques:** `/home/dapintoo/muography-scratch/oe1-v1-prueba/geo-train-06/view0/block0000` (fila 108, semilla 20261001090000) y `block0001` (fila 109, semilla 20261001090001), con 100.000 primarios cada uno. Huellas de imagen con corte: 3c21b65e… y a8be45a3…; sin corte: 146f932b… y 0af78c87…. [Lista completa antes](datos/sc3/verificacion-c4b6e4c/salidas/bloques.sha256) y [después](datos/sc3/verificacion-c4b6e4c/salidas/bloques-despues.sha256).

Comandos ejecutados (rutas absolutas en los archivos `*.comando.txt`):

```bash
python herramientas/fusionar_bloques_angular.py --manifiesto manifiesto-prueba.csv --salida ~/muography-scratch/oe1-v1-prueba --destino salidas/fusion
python herramientas/preparar_imagen_angular_v1.py salidas/fusion/geo-train-06/geo-train-06_view0_hist.csv --salida salidas/imagenes
python herramientas/publicar_bloque_angular.py --manifiesto manifiesto-prueba.csv --fila 108 --origen ~/muography-scratch/oe1-v1-prueba --destino ~/muography-scratch/oe1-v1-prueba-publicados-c4b6e4c
python herramientas/publicar_bloque_angular.py --manifiesto manifiesto-prueba.csv --fila 109 --origen ~/muography-scratch/oe1-v1-prueba --destino ~/muography-scratch/oe1-v1-prueba-publicados-c4b6e4c
python herramientas/publicar_bloque_angular.py --manifiesto manifiesto-prueba.csv --fila 108 --origen ~/muography-scratch/oe1-v1-prueba --destino ~/muography-scratch/oe1-v1-prueba-publicados-c4b6e4c
```

## Informes conservados

En [datos/sc3/verificacion-c4b6e4c/salidas/](datos/sc3/verificacion-c4b6e4c/salidas/), con los bytes producidos en SC3 (la regla `-text` de `.gitattributes` se incorporó antes de añadirlos):

- [revision-fusion.json](datos/sc3/verificacion-c4b6e4c/salidas/fusion/revision-fusion.json) y la vista fusionada (imagen d145db02…, metadatos 4e1eb966…). La matriz coincide con la fusión anterior de la entrega y con la reportada por la dirección.
- [revision-exportacion.json](datos/sc3/verificacion-c4b6e4c/salidas/imagenes/revision-exportacion.json) y el NPZ exportado (7ae38f69…).
- Los recibos de publicación (`publicacion-*.stdout.json`), la salida de error de cada paso (todas vacías), los códigos de salida y [las huellas de los bloques publicados](datos/sc3/verificacion-c4b6e4c/salidas/publicados.sha256).

## Observación T-01: finales de línea

La revisión de la dirección encontró 181 de 200 huellas de controles que no coinciden con los bytes versionados. [verificar_huellas_git.py](scripts/verificar_huellas_git.py) compara cada huella declarada en los seis manifiestos `salidas.sha256`/`salida.sha256` de la entrega con el contenido almacenado en el objeto Git, sin pasar por la copia de trabajo. En el commit `f9a77ef`, **las 204 entradas coinciden con su blob** ([informe](resultados/huellas-git-sc3.json)).

Los bytes versionados son, por tanto, los de SC3. El desajuste aparece cuando se extrae la rama con conversión de finales de línea (`core.autocrlf`). Lo confirma la huella del manifiesto de prueba: el informe de la dirección registra `aeef224c…` (copia con CRLF), mientras que el blob y SC3 tienen `1d0594c3…`. La regla `-text` que la dirección añadió en `main`, ya fusionada en la rama, evita la conversión en extracciones futuras de estos archivos.
