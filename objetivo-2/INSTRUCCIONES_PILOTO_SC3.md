# Ejecución del piloto OE2 en SC3

## Propósito

Se comparará la U-Net con la cGAN al 5 % de estadística. Primero se comprueba que ambas funcionen en la GPU y puedan reanudarse. Después se entrenan hasta 30 épocas para observar su aprendizaje y medir el costo de una campaña mayor. No se requieren nuevas simulaciones de muones.

## Preparación

Actualizar una copia limpia de la rama `main` de `anlegogo/muografia-documentada` y registrar `git rev-parse HEAD` y `git status --short`. Si existen cambios locales, conservarlos en su rama y usar una copia limpia para el piloto. Ejecutar desde la raíz del repositorio, dentro de una asignación GPU conforme a las reglas de SC3. Este documento no presupone nombre de partición, cuenta, módulo o comando del planificador.

Activar un entorno con PyTorch compatible con CUDA y la GPU asignada. Las [versiones CPU verificadas](requirements-cpu-verificado.txt) son una referencia de bibliotecas, no un paquete CUDA para instalar ciegamente. Guardar `python --version`, `python -m pip freeze` y la salida de `nvidia-smi`. Registrar la versión CUDA real del entorno; la indicada por el controlador no sustituye a `torch.version.cuda`.

En los comandos Bash siguientes, reemplazar `/ruta/datos-oe1` por la carpeta que contiene `dataset-v2/` y `pares/`, y `/ruta/resultados-oe2` por almacenamiento persistente con espacio para checkpoints. No usar una ruta temporal que desaparezca al terminar el trabajo.

```bash
export OE2_DATA=/ruta/datos-oe1
export OE2_OUT=/ruta/resultados-oe2
mkdir -p "$OE2_OUT"
```

## A. Prueba técnica con interrupción y reanudación

Ejecutar los cuatro comandos en orden. Si uno falla, detenerse y guardar su salida; no continuar con los siguientes como si la prueba hubiera pasado.

```bash
python objetivo-2/herramientas/ejecutar_piloto.py --config tecnica-unet --data-root "$OE2_DATA" --out-root "$OE2_OUT" --stop-after-epoch 1
python objetivo-2/herramientas/ejecutar_piloto.py --config tecnica-unet --data-root "$OE2_DATA" --out-root "$OE2_OUT" --resume auto
python objetivo-2/herramientas/ejecutar_piloto.py --config tecnica-cgan --data-root "$OE2_DATA" --out-root "$OE2_OUT" --stop-after-epoch 1
python objetivo-2/herramientas/ejecutar_piloto.py --config tecnica-cgan --data-root "$OE2_DATA" --out-root "$OE2_OUT" --resume auto
python objetivo-2/herramientas/resumir_piloto.py --stage tecnica --out-root "$OE2_OUT" --output "$OE2_OUT/resumen-tecnico.json"
```

La primera ejecución de cada método debe terminar con `stop_file`; es la interrupción prevista. La segunda debe completar la época 2. Para avanzar, el resumen debe indicar `technical_checks_passed: true` y `local_cpu_check_only: false`. No utilizar `--cpu-test` ni `--allow-cpu-test` en la entrega GPU.

## B. Piloto completo al 5 %

Si A pasa, ejecutar ambos métodos desde cero. Puede hacerse uno después del otro en la misma GPU. No es necesario pedir otra autorización para esta etapa ya prevista. No deben ejecutarse dos trabajos simultáneos que escriban en el mismo directorio de un método.

```bash
python objetivo-2/herramientas/ejecutar_piloto.py --config piloto-unet --data-root "$OE2_DATA" --out-root "$OE2_OUT"
python objetivo-2/herramientas/ejecutar_piloto.py --config piloto-cgan --data-root "$OE2_DATA" --out-root "$OE2_OUT"
python objetivo-2/herramientas/resumir_piloto.py --stage piloto --out-root "$OE2_OUT" --output "$OE2_OUT/resumen-piloto.json"
```

El límite es 30 épocas, con parada temprana. Si se agota el tiempo del trabajo, reanudar el método con el mismo comando agregando `--resume auto`; se recupera el último checkpoint de época completa. Una época interrumpida puede repetirse. No cambiar épocas, lote, semilla o configuración para reanudar. Si existe una incompatibilidad se debe conservar el mensaje y reportarla.

Para una parada voluntaria ordenada, crear un archivo llamado `STOP` dentro del directorio del método mientras está ejecutándose. El motor termina la época y guarda el estado; esto no es una parada inmediata. No esperar al último segundo de la asignación para solicitarla.

## Qué entregar

Crear una entrega en una rama propia y registrar:

- Commit utilizado, fecha, GPU, entorno, identificadores de trabajos SC3 y comandos reales.
- Salida estándar y errores completos de cada ejecución, incluso las interrumpidas.
- `resumen-tecnico.json`, `resumen-piloto.json` y, por cada uno de los cuatro directorios, `record/`, `metrics.jsonl`, `summary.json`, `piloto-entorno.json`, `piloto-sesiones.jsonl` y `baseline-entrada.json`.
- Figuras `samples/` generadas durante el piloto y observaciones sobre estructuras, bordes o patrones anómalos. No seleccionar únicamente los ejemplos favorables.
- Enlace accesible a `checkpoints/last.pt` y `best.pt`, con SHA-256, tamaño y correspondencia exacta con cada ejecución. Los pesos grandes se comparten por Drive o almacenamiento acordado, no se incorporan como binarios pesados a Git.
- Tabla con mejor época, SSIM del modelo y de entrada, diferencia, tiempo total, tiempo por época y memoria máxima por método. El resumen aporta varios de estos valores; completar duración y recursos reportados por SC3.

Si un método empeora la entrada, también se reporta. La finalidad del piloto es orientar la decisión siguiente. No iniciar todavía las otras fracciones ni los 24 entrenamientos principales.
