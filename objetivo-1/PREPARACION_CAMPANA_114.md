# Preparación de la campaña de 114 vistas

2026-10-02, Colombia. Se completan las siete actividades locales autorizadas después de revisar los histogramas `ccbdce0`. No se ejecutó transporte nuevo. El alcance idealizado ya está adoptado; **el manifiesto de 344 M es un candidato preparado, no una orden de envío ni una garantía de calidad**. Esta guía sustituye las tareas inmediatas de la guía del piloto, cuyo resultado ya fue recibido.

## 1. Calidad de las referencias

Se propone el siguiente protocolo de evaluación, explícito antes de producir la campaña:

- Integridad: exactamente 114 referencias compatibles, 19 geometrías y seis vistas, con N y semillas del manifiesto, uint32, sin saturación, procedencia y entorno verificables. Un error técnico impide aceptar la vista.
- Bordes: intervalo completo dentro de ±1 punto porcentual para cada una de las 15 regiones por vista. Se conserva el método de intervalos binomiales y Bonferroni, con α por vista = 0,05/114; cada vista reparte ese valor entre sus 16 probabilidades. La familia completa tiene cobertura simultánea al menos 95 % bajo las hipótesis de historias independientes y una llegada como máximo por primario. No se afirma potencia del 80 % para la campaña por haberla usado en la planificación del piloto.
- Roca: indicador de suficiencia descriptiva propuesto de al menos 90 % de las ROI de 4 × 4 píxeles con 100 cuentas o más. ROI predefinidas por columna nominal entre 30.000 y 100.000 g/cm². Se reportan además mediana, percentil 10 y número de regiones. No es precisión por píxel, criterio para toda la roca ni garantía sobre tasas verdaderas. Cien cuentas representan aproximadamente 10 % de ruido relativo de conteo en esa región, sin incluir incertidumbre de modelo.
- No se seleccionan regiones después de ver sus conteos. No se eliminan vistas difíciles, no se recortan valores ni se aumenta N hasta obtener aceptación. Si hay insuficiencia, conservar el resultado y revisar el alcance de calidad antes de cerrar el conjunto. Una futura ampliación requeriría un plan separado.

La regla de roca es una propuesta de calidad para las referencias del producto; no se atribuye al objetivo original ni se presenta como decisión previamente aprobada por la dirección.

## 2. Elección de presupuesto e incertidumbre

| N por vista | Primarios en 114 vistas | Horas-núcleo estimadas | Horas ideales con 96 núcleos |
|---:|---:|---:|---:|
| 211 M | 24.054 millones | 3.641 | 37,9 |
| 344 M | 39.216 millones | 5.936 | 61,8 |

Estimación basada en 191,63 horas-núcleo asignadas en el piloto, no en tiempos medidos de todo el catálogo; no incluye espera en cola. [Presupuesto calculado](evidencias/preparacion-campana-114/presupuesto.json).

Con las tasas de las ROI del piloto, una proyección binomial de una nueva realización da una fracción media de regiones con ≥100 cuentas de 62,4–64,0 % con 211 M y 89,7–91,1 % con 344 M. Este cálculo trata las tasas estimadas como conocidas. Al propagar intervalos marginales simultáneos conservadores para las 1.464 tasas, los límites son amplios: aproximadamente 64,1–100 % para la fracción media a 344 M. No son límites de la fracción que necesariamente se observará. La evidencia no garantiza un mínimo del 90 %.

La multiplicación directa de las cuentas observadas daba 89,75–93,03 %; no modelaba una nueva fluctuación del conteo. Ambos cálculos son de planificación. [Comparación reproducible](evidencias/preparacion-campana-114/comparacion-estadistica.json).

**Recomendación:** mantener 344 M como candidato de presupuesto fijo si se prioriza mejorar las referencias, aceptando que algunas vistas pueden no alcanzar la meta descriptiva. No aprobar las 114 vistas bajo la promesa de que todas alcanzarán 90 %; si ese mínimo es imprescindible, esta evidencia no basta para garantizarlo. El número aumenta el cómputo 63 % y reduce el ruido relativo esperado aproximadamente 22 % frente a 211 M.

## 3. Representatividad geométrica

Se compararon los 19 conos con marcha de rayos de 2 m, usando el mismo clasificador nominal del piloto. La densidad del edificio es 2,65 g/cm³ en todos. `geo-train-06` tiene el menor radio (509,7 m) y el menor percentil 90 de columna nominal en rayos de roca (212.689 g/cm²). Los mayores valores corresponden a `geo-val-01` (295.740), `geo-train-07` (286.730), `geo-train-04` (284.080) y `geo-test-01` (283.020).

El piloto no es el caso de mayor espesor nominal del catálogo. Este indicador no demuestra el orden de transmisión real: no incluye anomalías, espectro ni dispersión, y se calcula sobre toda la roca nominal, no solo la banda de ROI de calidad. Las anomalías y las seis direcciones sí deben conservarse en Geant4.

Se prepararon máscaras para las 19 geometrías. El cono homogéneo es circular, por lo que la máscara nominal es común a sus seis vistas; esto no supone que los conteos o las anomalías sean simétricos. Hay entre 150 y 244 ROI por geometría. Todos los bordes tienen soporte. Las cifras, geometrías y huellas están en [plan.json](evidencias/preparacion-campana-114/plan.json).

## 4. Evaluación de la campaña

[evaluar_campana_114.py](../herramientas/evaluar_campana_114.py) verifica manifiesto, receta, hashes de máscaras, N, semillas, geometría, binario, tablas y compatibilidad de configuración antes de evaluar. Informa vistas faltantes, errores técnicos, bordes y suficiencia descriptiva de roca por separado. Nunca declara validación física o autorización de producción.

La sensibilidad retrospectiva del piloto a α=0,05/114 da 89 de 90 regiones equivalentes; una queda inconclusa. **No revoca la aceptación original del piloto**, cuyo criterio era para seis vistas, ni demuestra fallo físico. Explica por qué no deben extenderse sin ajuste sus intervalos a una familia mayor.

Una salida técnica completa no significa aceptación científica; deben examinarse también los indicadores de bordes y roca. Se prohíbe cambiar la regla tras conocer qué vistas incumplen.

## 5. Plan operativo y posible aprovechamiento del piloto

El [manifiesto candidato](evidencias/preparacion-campana-114/manifiesto-114-344M.csv) contiene 1.026 bloques: nueve por vista, aproximadamente 38,22 M por bloque. Total 39.216 M de primarios. Se asignaron semillas nuevas sin coincidencias con el piloto. [Preflight offline satisfactorio](evidencias/preparacion-campana-114/preflight.json).

Se conserva la [receta operativa verificada](contratos/receta-operativa-siete-actividades.json), incluido el ejecutable reportado y el entorno de transporte. No se modifica el lanzador que ya funcionó en SC3: se debe usar el envoltorio `python-oe1` de la entrega, porque resolver el enlace del Python del entorno virtual pierde sus paquetes. La identidad del plan depende de rutas, intérprete, manifiesto, ficha y herramientas. Utilizar directorios nuevos y conservarlos durante toda la ejecución.

**Reutilización evaluada:** completar las seis vistas de 211 a 344 M requeriría 133 M adicionales por vista, sin cambiar receta, con semillas nuevas. Ahorraría 1.266 M de primarios y aproximadamente 191,6 horas-núcleo (3,2 % del total). Sin embargo, los CSV fusionados no sustituyen a los 36 bloques y sus recibos en la cadena de publicación. El lanzador no acepta recibos de un manifiesto diferente ni debe reutilizarse la raíz del piloto para otra campaña.

El candidato preparado opta por una campaña nueva, conservando el piloto como evidencia independiente. No se suman sus histogramas a las nuevas referencias ni se contabilizan dos veces. Así se evitan cambios en los recibos y en la definición de la evaluación confirmatoria. La alternativa de aprovechamiento queda cuantificada, pero no se instruye copiar o renombrar recibos para forzar su aceptación. No se modifica retrospectivamente el piloto.

## 6. Ensayo de empaquetado terminado

Se generaron seis archivos, cada uno con una referencia y 80 realizaciones: **480 pares**, cuatro fracciones (0,5; 0,1; 0,05; 0,01), veinte realizaciones por fracción y semilla maestra 20260805. Todos pertenecen a `train`, sin repartir variantes de una geometría entre particiones.

Se comprobaron formas, uint32, identidad de referencias, ausencia de conteos reducidos mayores que su referencia y regeneración exacta con las mismas semillas. Se registraron también los desvíos agregados frente a la media binomial. [Inventario](evidencias/preparacion-campana-114/inventario-480-pares.json) · [Verificación](evidencias/preparacion-campana-114/verificacion-480-pares.json).

Los binarios locales están en `trabajo/paquete-piloto-480/`, excluidos de Git; los inventarios sí están versionados. Se regeneran desde los NPZ de `ccbdce0`, sin SC3. No forman parte de las 114 referencias finales y comparten el ruido de su referencia finita.

## 7. Instrucciones para estudiantes

1. Incorporar `main` en su rama y revisar este protocolo. Conservar el piloto, su entorno y sus recibos. No repetirlo.
2. Antes de enviar, dejar constancia del acuerdo sobre 344 M, el coste, la meta descriptiva de roca y el tratamiento de resultados insuficientes. La autorización dada para preparar estas siete actividades no se interpreta como autorización para consumir SC3.
3. Verificar la receta y los hashes en el árbol de trabajo, usar el envoltorio `python-oe1` ya probado y definir raíces nuevas para esta campaña. Ejecutar el preflight y el lanzador sin `--enviar`; revisar el informe, el intérprete, los cupos y las rutas.
4. Con el presupuesto acordado, usar el mismo comando con `--enviar`, hasta cuatro trabajos de 24 núcleos. El lanzador realiza una pasada: repetirlo cuando haya cupos; conservar `.operacion`. Si falla un trabajo, conciliar su estado y preservar la evidencia antes de un reintento; nunca borrar registros para forzar envíos.
5. Concluido el N fijo, fusionar y evaluar las 114 vistas. Un resultado incompleto o insuficiente se reporta tal cual; no se corrigen imágenes para hacerlas pasar ni se añade transporte automáticamente.
6. Exportar y auditar las 114 referencias. Solo tras la revisión de su calidad, formar los 9.120 pares y entregar inventario, hashes, tiempos reales, logs y ficha final. Los datos deben quedar recuperables; el informe debe distinguir piloto, campaña y derivados.

### Comandos operativos

Desde la raíz de la réplica actualizada en SC3, sustituir rutas por las reales:

```bash
set -euo pipefail
PY="$HOME/oe1-trabajo/entorno/python-oe1"
PLAN="$PWD/objetivo-1/evidencias/preparacion-campana-114"
RECETA="$PWD/objetivo-1/contratos/receta-operativa-siete-actividades.json"
REF="$PWD/objetivo-1/evidencias/preparacion-siete-actividades/cielo-ideal-margen-5.json"
ARBOL="$HOME/oe1-trabajo/produccion-receta"
TEMPORAL="$HOME/muography-scratch/oe1-114-344M-intentos"
SALIDA="$HOME/muography-scratch/oe1-114-344M-publicados"
FUSION="$HOME/muography-scratch/oe1-114-344M-fusion"
IMAGENES="$HOME/muography-scratch/oe1-114-344M-imagenes"

"$PY" herramientas/preparar_campana_angular.py "$PLAN/manifiesto-114-344M.csv" --informe "$HOME/preflight-114-344M.json"
"$PY" herramientas/lanzar_campana_angular.py \
  --manifiesto "$PLAN/manifiesto-114-344M.csv" --arbol "$ARBOL" \
  --temporal "$TEMPORAL" --salida "$SALIDA" --receta "$RECETA" \
  --python "$PY" --threads 24 --max-trabajos 4
# El comando anterior solo consulta/planifica. --enviar requiere el acuerdo indicado.
```

Con todos los bloques completos, en destinos nuevos y conservando stdout, stderr y códigos de salida:

```bash
"$PY" herramientas/fusionar_bloques_angular.py --manifiesto "$PLAN/manifiesto-114-344M.csv" --salida "$SALIDA" --destino "$FUSION"
"$PY" herramientas/evaluar_campana_114.py --fusion "$FUSION" --plan "$PLAN/plan.json" --receta "$RECETA" --referencia "$REF" --salida "$HOME/evaluacion-114-344M.json"
"$PY" herramientas/preparar_imagen_angular_v1.py "$FUSION"/*/*_hist.csv --salida "$IMAGENES"
"$PY" herramientas/empaquetar_angular_v1.py "$IMAGENES" --informe "$HOME/inventario-114-344M.json"
# Tras revisar calidad: añadir --salida NUEVO_PAQUETE para generar los pares.
```

### Reproducción local

`PILOTO` es `datos/sc3/piloto-v2` extraído de la entrega `ccbdce0`. `HELPER` es `scripts/comun.py` de esa entrega (hash registrado en el plan). No se necesita nueva simulación:

```bash
python herramientas/preparar_campana_114.py --helper "$HELPER" --salida NUEVO_PLAN
python herramientas/comparar_presupuesto_114.py --fusion "$PILOTO/fusion" --salida NUEVA_COMPARACION.json
python herramientas/empaquetar_angular_v1.py "$PILOTO/imagenes" --geometrias geo-train-06 --informe NUEVO_INVENTARIO.json --salida NUEVO_PAQUETE_PILOTO
python -m unittest discover -s herramientas -p 'test_*angular*.py' -v
```

Validación realizada: **106 pruebas satisfactorias**, incluyendo campaña vacía, manifiesto/máscara alterados, presupuesto, semillas y binario incorrectos. El caso sintético de una vista comprueba el flujo del evaluador; no representa resultados físicos de campaña. Se verificaron las 114 combinaciones, 1.026 semillas únicas y ausencia de coincidencias con el piloto; la reproducción del análisis binomial coincide con la evidencia guardada. Se corrigió durante la preparación una consulta de hashes que omitía la extensión `.json` del catálogo; la generación final pasó el control de integridad.
