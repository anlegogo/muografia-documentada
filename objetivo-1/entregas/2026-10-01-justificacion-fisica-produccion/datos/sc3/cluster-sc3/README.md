# Operación en el clúster SC3 (UIS)

Guía operativa del paquete de simulación en SC3. Al clúster viaja SOLO el
paquete de despliegue (`scripts/make_sc3_bundle.sh`) — nunca el repositorio
completo ni los documentos del proyecto.

## Topología y reglas de la plataforma

- Acceso en dos saltos: `ssh usuario@toctoc.sc3.uis.edu.co` → `ssh guane`.
- `guane` es el **frontend**: gestión de archivos, edición y compilaciones
  ligeras. Todo trabajo intensivo va por SLURM.
- Geant4 preinstalado como módulo: `module load geant4/11.4.2`
  (siempre `module purge` antes — ver `env.sh`).
- `/home/$USER`: código, scripts y resultados finales.
  `/scratch/<GRUPO>` (BeeGFS): organizado por grupo de investigación, solo el
  admin crea el directorio. **Sin backup y con purga automática.** Con el
  diseño actual (histogramas, ~300 MB de campaña) NO es necesario: `env.sh`
  usa `$HOME/muography-scratch` por defecto y adopta `/scratch/<GRUPO>`
  automáticamente si existe.
- Particiones: `legacy` (guane01–08, por defecto), `amd`, `fat`, `gpu_titan`.
  Esta carga es CPU-bound → `legacy`/`amd`.
- QoS estudiantil: máx. 1 hora y 1 nodo por trabajo. Verificar la QoS real:
  `sacctmgr show assoc user=$USER format=user,account,qos%40`.

## Flujo

```
[local] scripts/make_sc3_bundle.sh          # empaqueta commit actual
[local] scp sc3-deploy.tar.gz sc3-guane:
[guane] tar -xzf sc3-deploy.tar.gz -C muography-sim && cd muography-sim
[guane] source cluster/sc3/env.sh
[nodo ] srun -p legacy -N1 -n1 -c4 -t 00:40:00 bash -lc \
          'source cluster/sc3/env.sh && cmake -S simulation/geant4_app -B build_sc3 && cmake --build build_sc3 -j4'
[nodo ] sbatch cluster/sc3/smoke_test.sbatch          # humo: 1e5 eventos
[guane] sacct -j <jobid> --format=Elapsed,MaxRSS      # s/evento y memoria
```

Campaña (NO lanzar sin aprobación — ver runbook en `docs/reports/`):

```
[guane] python3 cluster/sc3/submit_missing.py --events-per-view <N> \
            --events-per-block <B> --max-submit 20        # idempotente
[guane] python3 cluster/sc3/merge_blocks.py --blocks-per-view <K>
[local] rsync -av "sc3-guane:muography-scratch/campaign-merged/" data/campaign-geant4/
        # (o la ruta de /scratch/<GRUPO>/... si el admin creó el dir de grupo)
[local] python simulation/geant4_app/tools/csv_to_npz.py ...   # por vista
```

## Diseño de bloques (checkpointing)

Un **bloque** = (geometría, vista, índice) con semilla propia derivada y
presupuesto de eventos dimensionado para terminar en <50 min (margen sobre el
muro de 1 h). El bloque se publica de forma atómica con su `block.sha256`;
`submit_missing.py` re-somete solo faltantes o corruptos. Ningún corte de
SLURM pierde más que el bloque en curso.

Derivación de semillas (reproducible, sin numpy):
`seed = 20260805·10⁶ + geo_idx·10⁴ + vista·10³ + bloque`.

## Notas

- `smoke_test.sbatch` y `campaign_block.sbatch` traen `--mail-type`
  comentado: completar el correo institucional antes de usarlo.
- La conversión eventos↔días de exposición se calibra con la tasa de EcoMug
  restringida a la ventana angular (ver runbook, paso de calibración).
- Los resultados finales SIEMPRE terminan respaldados fuera del clúster; si
  se usa el scratch de grupo, copiarlos a `/home` antes de la purga.
