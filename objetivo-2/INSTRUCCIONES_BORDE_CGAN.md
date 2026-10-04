# Instrucciones para ejecutar el ensayo de borde E1

**Estado: preparación local completa y verificada; pendiente de nueva aceptación GPU.** El trabajo delegado es comprobar esta versión en GPU y, si las tres parejas pasan, completar las seis continuaciones sin esperar otra aprobación entre parejas. No ampliar épocas, fracciones ni semillas. Consultar el [diseño](DISENO_BORDE_CGAN.md).

## Qué se busca

El ajuste anterior conservó mejor el total del borde, pero no la distribución entre píxeles. Se comparan C0, con el ajuste regional, y C1, que añade el término espacial de peso 0,629. Una prueba técnica correcta permite entrenar; no demuestra mejora de las imágenes.

## Preparación

Actualizar la copia de main que contiene esta guía y crear una rama de entrega, por ejemplo oe2/borde-cgan-f05, conservando cambios y entregas anteriores. Registrar el commit con git rev-parse HEAD. No modificar configuraciones ni fuentes.

Usar el entorno PyTorch/CUDA de las últimas entregas y sus dependencias. Si se usan tres GPU, deben coincidir modelo y entorno. Cada pareja conserva su GPU en técnica y piloto.

Definir rutas reales y una salida nueva, desde la raíz del repositorio:

~~~bash
set -euo pipefail
export DATA=/ruta/insumos
export MASKS=/ruta/mascaras-ajuste-v1
export WEIGHTS=/ruta/cgan-original-epoca5.pt
export OUT=/ruta/ensayo-borde-e1
COMMON=(--datos "$DATA" --mascaras "$MASKS" --pesos "$WEIGHTS" --raiz "$OUT")
~~~

El checkpoint es el original de época 5; no uno de R1–R3 ni de la prueba técnica. El código comprueba su SHA. DATA contiene dataset-v2/shards con los treinta archivos train/val; MASKS contiene el manifiesto y las quince máscaras. No se necesitan test/generalization.

## 1. Pruebas técnicas

Con una GPU, ejecutar en secuencia:

~~~bash
for PAR in B1 B2 B3; do
  python objetivo-2/herramientas/orquestar_borde_cgan.py \
    "${COMMON[@]}" --fase tecnica --pareja "$PAR"
done
~~~

Por pareja se ejecutan C0 y C1 continuas y sus equivalentes interrumpidas al terminar época 1 y recuperadas hasta época 2. Se comparan G, D, ambos optimizadores, RNG, historial y predicciones. Solo se genera aceptacion-gpu.json si la igualdad es exacta.

Con tres GPU, ejecutar una pareja por terminal: B1 con CUDA_VISIBLE_DEVICES=0, B2 con CUDA_VISIBLE_DEVICES=1 y B3 con CUDA_VISIBLE_DEVICES=2. Conservar esa asignación para el piloto.

Si una prueba falla, no iniciar pilotos ni relajar la igualdad; conservar y reportar el log. La raíz debe ser compartida entre los procesos para verificar las tres aceptaciones.

## 2. Cinco épocas por variante

Las tres aceptaciones GPU nuevas deben existir antes del primer piloto. El orquestador vuelve a auditar sus artefactos y rechaza las aceptaciones antiguas o CPU.

~~~bash
for PAR in B1 B2 B3; do
  python objetivo-2/herramientas/orquestar_borde_cgan.py \
    "${COMMON[@]}" --fase piloto --pareja "$PAR"
done
~~~

Con tres GPU, ejecutar cada pareja en su terminal con la misma asignación. Dentro de cada pareja se ejecuta C0 y después C1. Ambas parten de los pesos originales, con optimizadores nuevos. La selección es siempre la quinta época adicional.

Si el piloto se interrumpe después de guardar una época, repetir el comando de esa pareja: se recupera el estado compatible. Una variante completa se verifica y se omite. Para detener ordenadamente puede crearse STOP dentro de su carpeta; retirarlo antes de reanudar.

Si únicamente falló una exportación después de completar las cinco épocas, usar ejecutar_borde_cgan.py con los mismos argumentos de datos, pesos, máscaras, pareja, rama, etapa piloto, salida y aceptación, añadiendo --exportar y sin --reanudar. Después repetir el orquestador.

Un fallo de identidad, memoria o valores no finitos exige detener nuevos lanzamientos y reportar. La prueba técnica requiere carpeta nueva; no se recupera automáticamente como un piloto. Conservar los fallos previos.

Registrar tiempos y memoria de la prueba GPU antes del piloto. No hay duración garantizada: el límite son seis variantes de cinco épocas. Si los recursos no alcanzan, conservar el estado recuperable y reportar, sin cambiar el protocolo.

## 3. Evaluación y síntesis

Con las seis variantes terminadas, evaluar las tres parejas en secuencia sobre la misma GPU:

~~~bash
export CUDA_VISIBLE_DEVICES=0
for PAR in B1 B2 B3; do
  python objetivo-2/herramientas/orquestar_borde_cgan.py \
    "${COMMON[@]}" --fase evaluacion --pareja "$PAR"
done
python objetivo-2/herramientas/orquestar_borde_cgan.py \
  "${COMMON[@]}" --fase sintesis
~~~

Conservar las carpetas en sus rutas originales hasta completar la síntesis y el inventario: los informes enlazan esas rutas. Si se trasladan, repetir la evaluación hacia una salida nueva y conservar los informes anteriores.

Las salidas deben ser nuevas. Se conservan entrada, modelo inicial, C0 y C1; figuras de todas las vistas, tablas regionales y anomalías. La síntesis exige las tres parejas y los nueve controles del diseño. No elegir solo la mejor semilla.

## 4. Entrega

~~~bash
python objetivo-2/herramientas/inventariar_entrega_borde.py \
  --raiz "$OUT" --mascaras "$MASKS" --etapa piloto \
  --salida "$OUT/inventario-entrega.json"
~~~

El inventario vuelve a auditar los artefactos y produce una síntesis independiente.

- En la rama: informe, commit ejecutado, entorno/GPU y asignación por pareja, comandos, tiempos/memoria, incidencias, aceptaciones, identidades, historiales, resúmenes, exportaciones, índices, logs, comparaciones, anomalías, figuras, síntesis e inventario.
- En Drive: 18 checkpoints, 21 arreglos de predicciones y caché completa; 55 archivos contando el manifiesto de máscaras. Conservar las rutas relativas y no incorporar checkpoints a Git.
- En el informe: enlaces accesibles a Drive, tamaños y SHA-256 del inventario. Una carga parcial no constituye entrega terminada.

Un resultado científico desfavorable no autoriza cambiar el coeficiente o excluir parejas. Completar y reportar el bloque. La concordancia descriptiva no concede aceptación física ni habilita abrir reservas o ampliar la campaña.

## Reproducción local CPU

El orquestador acepta --cpu-test solo en la fase técnica. Ejecutar B1, B2 y B3 en una raíz nueva con esa opción. Después evaluar cada pareja con evaluar_borde_cgan.py, --etapa tecnica --dispositivo cpu y C0-continua/C1-continua como control/regional. Resumir con resumir_borde_cgan.py --etapa tecnica.

~~~bash
python objetivo-2/herramientas/test_integracion_borde_cgan.py -v
python objetivo-2/herramientas/test_orquestacion_borde_cgan.py -v
python objetivo-2/herramientas/test_artefactos_borde_cgan.py \
  --raiz /ruta/pruebas-cpu --datos "$DATA" --mascaras "$MASKS" \
  --pesos "$WEIGHTS" --salida /ruta/controles-cpu.json
~~~

El control de artefactos necesita las doce ejecuciones técnicas y verifica recuperación, rechazos y exportación sin reentrenar. El inventario admite --etapa tecnica sin confundirla con el piloto. Los bloques Bash se proporcionan para Linux/GPU; las interfaces Python equivalentes se verificaron localmente en Windows/CPU.

