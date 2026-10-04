# Instrucciones del ajuste de cuentas al 5 %

**Actualización posterior — 2026-10-03:** el ensayo U-Net de esta guía ya fue ejecutado y su entrega a6aa6b8 fue [revisada independientemente](REVISION_AJUSTE_A6AA6B8.md). Ajuste-01 y Ajuste-02 verificados; Ajuste-03 completado, con resultado de compromiso y sin aceptación física. Los estados de preparación y comandos siguientes se conservan como antecedente y reproducción; no constituyen un encargo de repetir el ensayo. La [propuesta cGAN](PROPUESTA_CONTINUACION_CGAN_F05.md) aún requiere integración y pruebas.


Fecha de revisión: 2026-10-03, Colombia.

## Propósito y estado

El ensayo comprueba si una penalización regional permite conservar mejor las cuentas de roca y anomalías sin deteriorar cielo, bordes, contraste ni calidad de imagen. Ambas variantes continúan la misma U-Net durante cinco épocas: A conserva la pérdida original; B añade el término regional. El [diseño científico](DISENO_AJUSTE_CUENTAS_F05.md) fija datos, semillas, presupuesto y criterios antes del entrenamiento.

**Ajuste-01 verificado; Ajuste-02 verificado en CPU y pendiente en GPU; Ajuste-03 pendiente.** El ejecutor y la evaluación están implementados. La [evidencia local](evidencias/integracion-ajuste-v1.json) contiene identidades, versiones y resultados. No constituye aceptación CUDA ni demuestra mejora científica. El OE2 permanece abierto.

Se completaron 13 controles funcionales, nueve de pérdida y ocho geométricos. Cuatro ejecuciones de la red completa verificaron igualdad exacta de parámetros, optimizador, estados aleatorios y predicciones entre entrenamiento continuo y recuperado. La batería suma 16 actualizaciones; una ejecución preliminar adicional sumó cuatro. No se ejecutó el piloto de cinco épocas.

Se prepararon 90 mapas de máscaras para 12 geometrías train y tres val; las 78 máscaras regionales de la validación anterior conservan sus huellas. Se verificaron 30 archivos de datos/metadatos. El evaluador se contrastó con 720 predicciones anteriores: reproduce exactamente 468 cifras regionales y los 24 contrastes, con 23 combinaciones comunes válidas. Estas predicciones son una prueba de regresión del evaluador, no resultados del nuevo ensayo. Test y generalization permanecieron sin abrir.

## Preparación

Actualizar la rama de trabajo con esta implementación de main y registrar el commit utilizado. Conservar los archivos originales y las entregas anteriores. Todos los comandos se ejecutan desde la raíz del repositorio, en Bash, dentro del entorno Python elegido para la GPU. No se presupone un gestor de colas concreto.

Entorno local verificado: Python 3.12.14, PyTorch 2.6.0+cpu, NumPy 2.3.5, SciPy 1.18.1, scikit-image 0.26.0, matplotlib 3.11.1, filelock 3.16.1, SymPy 1.13.1, mpmath 1.3.0 y networkx 3.4.2. La ejecución estudiantil debe emplear PyTorch con CUDA compatible con el equipo, no la distribución CPU. Mantener el mismo entorno, dispositivo, código y datos durante las cuatro pruebas y el piloto; el ejecutor registra su identidad y rechaza cambios incompatibles. La igualdad CPU/GPU no se presupone.

Los JSON efectivos son [ejecucion-A.json](configuraciones/ajuste-cuentas-v1/ejecucion-A.json) y [ejecucion-B.json](configuraciones/ajuste-cuentas-v1/ejecucion-B.json). El nuevo ejecutor los consume directamente; no se pasan al motor histórico. Los archivos spec.json conservan el diseño anterior.

Preparar rutas absolutas reales. DATA corresponde a la distribución ya verificada; PESOS corresponde al best.pt original de U-Net, no a cGAN ni a una prueba técnica. Su SHA-256 debe ser 734bc5dc1aa4cdc16a3fa0b6de2d58da7575c5bd0b1fe342bc266283f0e8e57a. Elegir directorios nuevos para MASCARAS y SALIDAS; no reutilizar resultados de otro ensayo.

```bash
set -e
DATA="/ruta/distribucion-verificada"
PESOS="/ruta/unet-best.pt"
MASCARAS="/ruta/trabajo/mascaras-ajuste-v1"
SALIDAS="/ruta/trabajo/ajuste-cuentas-v1"
python objetivo-2/herramientas/datos_ajuste.py --datos "$DATA" --salida "$MASCARAS"
```

El manifiesto registra geometrías, reglas, soporte de regiones, código y huellas de datos y máscaras. Las regiones son aproximaciones geométricas nominales mediante rayos centrales; no son trayectorias individuales simuladas. Se incluyen máscaras de entrenamiento propias y el caso homogéneo sin anomalías.

## Comprobación técnica en GPU

Se usan ocho pares train y ocho val previamente fijados, lote cuatro y dos épocas. Para cada variante se ejecuta una referencia continua y otra interrumpida al terminar la primera época, que luego se recupera. Son cuatro ejecuciones y 16 actualizaciones en total. No se cambia el lote, la semilla ni la precisión para conseguir que la prueba pase.

```bash
for RAMA in A B; do
  python objetivo-2/herramientas/ejecutar_ajuste.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-continua"
  python objetivo-2/herramientas/ejecutar_ajuste.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --parar-tras 1
  python objetivo-2/herramientas/ejecutar_ajuste.py --rama "$RAMA" --etapa tecnica --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/tecnica/$RAMA-recuperada" --reanudar
done

python objetivo-2/herramientas/revisar_ajuste.py --A-continua "$SALIDAS/tecnica/A-continua" --A-recuperada "$SALIDAS/tecnica/A-recuperada" --B-continua "$SALIDAS/tecnica/B-continua" --B-recuperada "$SALIDAS/tecnica/B-recuperada" --exigir-gpu --salida "$SALIDAS/aceptacion-gpu.json"
```

La comprobación debe terminar sin error y declarar aceptación GPU. Se exigen estados y predicciones idénticos entre ejecución continua y recuperada de cada variante, inicialización y orden compartidos entre A/B, valores finitos y archivos coherentes. No se exige que A y B terminen con los mismos pesos. La aceptación técnica no depende de que mejore SSIM en estas ocho muestras.

Conservar las cuatro carpetas y checkpoints: el piloto vuelve a auditarlos. Si se trasladan, regenerar la aceptación con las rutas correctas. El archivo de aceptación local CPU no habilita el piloto. Para reproducir solo las comprobaciones CPU puede añadirse --cpu-test a las ejecuciones técnicas y omitirse --exigir-gpu al revisor; esto no sustituye el paso CUDA.

## Continuaciones de cinco épocas

Si se obtiene aceptación GPU y el tiempo/memoria medidos son compatibles con los recursos disponibles, proceder con ambas variantes. Cada una parte otra vez de los pesos originales, con Adam nuevo; no continúa los pesos de las pruebas técnicas. Son 1.440 pares train, 360 val y 1.800 actualizaciones por variante, 3.600 en total.

```bash
for RAMA in A B; do
  python objetivo-2/herramientas/ejecutar_ajuste.py --rama "$RAMA" --etapa piloto --datos "$DATA" --mascaras "$MASCARAS" --pesos "$PESOS" --salida "$SALIDAS/piloto/$RAMA" --aceptacion-gpu "$SALIDAS/aceptacion-gpu.json"
done
```

Se conserva la quinta época adicional como resultado principal, aunque otra época tenga mejor SSIM. No hay parada temprana ni búsqueda de hiperparámetros. last.pt es el checkpoint final cuando summary.json declara completed y epoch igual a cinco. El ejecutor no permite este piloto mediante --cpu-test.

Si hay una interrupción, repetir el comando de esa rama con --reanudar y las mismas rutas. Se recupera desde la última época completa, incluidos optimizador y estados aleatorios. Para solicitar parada ordenada, crear un archivo STOP dentro de su carpeta; se detiene al cerrar una época. Retirar ese archivo antes de reanudar. No mezclar estados de A y B.

Una pérdida no finita, error de memoria, identidad incompatible o fallo de determinismo exige detenerse y entregar el error. No cambiar silenciosamente parámetros para continuar. Si solo falla la exportación tras completar el entrenamiento, repetir su comando con --exportar, sin --reanudar: se reconstruyen predicciones y registros sin pasos adicionales de optimización.

## Evaluación y entrega

Con ambas variantes completas:

```bash
python objetivo-2/herramientas/evaluar_ajuste.py --datos "$DATA" --mascaras "$MASCARAS" --control "$SALIDAS/piloto/A" --regional "$SALIDAS/piloto/B" --etapa piloto --salida "$SALIDAS/comparacion-piloto.json"
python objetivo-2/herramientas/visualizar_ajuste.py --datos "$DATA" --mascaras "$MASCARAS" --control "$SALIDAS/piloto/A" --regional "$SALIDAS/piloto/B" --etapa piloto --salida "$SALIDAS/figuras-piloto"
```

La evaluación compara entrada, A y B en idénticos pares y regiones. Informa Q por geometría y global, sesgos, errores de cuentas, contraste, SSIM y PSNR. Las figuras incluyen todas las vistas con escalas comunes. La clasificación es descriptiva: mejora concordante, compromiso o ausencia de mejora del indicador principal; no certifica densidad, significación estadística ni aceptación física.

Publicar en la rama de entrega un informe que indique commit, equipo, versiones, comandos, tiempos, incidencias y conclusión, junto con:

- Manifiesto de máscaras y aceptación GPU; identity.json, history.json, summary.json, last-session.json y exports.json de las pruebas y del piloto.
- indices-val.json, comparación completa y figuras de las 18 vistas, sin selección de ejemplos favorables.
- Enlaces de Drive a los cuatro checkpoints técnicos y a los dos finales, y a las predicciones finales, con tamaños y SHA-256. Mantener los binarios fuera de Git.

Las rutas del informe deben permitir localizar cada archivo. No reemplazar la evidencia anterior bajo el mismo nombre. Se revisará la entrega antes de ampliar a otras fracciones, semillas o particiones. Este trabajo utiliza los datos existentes: no exige nuevas simulaciones Geant4.

## Incidencias y alcance de la revisión local

La copia Git original mantiene un índice ilegible; la revisión se completó en una copia aislada y se publica mediante la conexión GitHub, sin reparar ese índice. Se incorporaron dependencias de Adam únicamente al entorno aislado. El primer intento detectó tipos numéricos mixtos en betas; la conversión explícita a flotantes conserva los valores científicos y las ejecuciones posteriores finalizaron correctamente.

La revisión acredita integración, entrenamiento corto y recuperación en CPU. Permanecen pendientes la comprobación CUDA y el ensayo A/B completo; sus resultados pueden confirmar o refutar la hipótesis. El cierre del OE1 permanece sin cambios.
