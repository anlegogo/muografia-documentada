# Segundo ensayo OE1 — etapa 2, protocolo v1.1

**Diseño: 1 de octubre de 2026, Colombia.** Preparado por solicitud del director tras revisar la etapa 1 y el complemento R2-01. Diseño fijado para implementación y ejecución por Daniel y Reinaldo en SC3, sujeto a las condiciones técnicas de arranque de este documento. No se ha ejecutado esta etapa. La [versión 1.0](PROTOCOLO_SEGUNDO_ENSAYO_OE1.md) se conserva como antecedente sin modificar.

## 1. Pregunta y decisión que permite

¿Cuánto cambia la probabilidad de detección en la región angular congelada `R_int` de `geo-train-06`, vista 0, al sustituir A por B con primarios de la fuente representativa original? A contiene el defecto y sirve de comparación histórica; B es la candidata para producir datos corregidos. A no es una referencia de verdad física.

La etapa 1 verificó contratos y el complemento mostró el mecanismo con 12 muones dirigidos. Ahora se estima el efecto con muones de la fuente original, sin dirigirlos al solape ni seleccionar energías de 10 TeV. **No se combinan estos resultados con etapa 1, pruebas técnicas o R2-01.**

La conclusión principal corresponde a una ROI, una vista y una geometría. No demuestra equivalencia de imágenes completas, de otras geometrías, ni de las 114 vistas. Permite cuantificar este caso y orientar la regeneración. Un efecto pequeño no convierte en correcta la geometría A.

## 2. Configuración congelada

- Geant4 11.4.2, entorno SC3, FTFP_BERT y parámetros de fuente, detector, cortes y secundarios de la etapa 1. Un hilo por proceso. Sin cambios de instrumentación.
- A2: commit `fdaef4b8aad259f17043ef0fc6fdccc295e3b8e2`; SHA ejecutable `a07d83c443120bb0a7e0d32d73ad8f1c1fa7e7cba771e9fc8331f7218b0728f5`.
- B2: commit `9bb43f3b620b5e6d62e4b5ea79647dff44c6f3cd`; SHA ejecutable `ae76186647e7cc90796a9504cfa8bc763fc959484c2f78bf647cbe321f996852`.
- Catálogos, tablas y máscara exactamente iguales a los insumos congelados de etapa 1. Máscara `R_int.mask.txt`, SHA `e76dcbe5926f9f4aeb61c556729d15c64124cd50a8577dca6beee9ffa317c5fd`. Conservar orientación, bins y dimensiones.
- Caso principal `geo-train-06`, vista 0, región 3D de intersección de primitivas originales 0 y 1. Control `geo-train-01`, vista 0, sin región 3D de solape; usar la misma máscara angular exclusivamente como control.
- Generación mediante `--write-primaries` de los binarios existentes. Congelar listas y metadatos antes de transportar; compartir exactamente la misma lista A/B. Guardar todos los muones, incluidos no detectados.
- Registrar commit de scripts de preparación/ejecución/análisis y su diferencia respecto a etapa 1. El comparador anterior tiene supuestos de N, semillas y manifiesto específicos de etapa 1: debe adaptarse y probarse; no usarlo sin cambios ni silenciar controles para conseguir `OK`.

## 3. Tamaño fijo, bloques e identidades

| Componente | Listas nuevas | Primarios por lista | Variantes | Corridas | Transportes |
|---|---:|---:|---|---:|---:|
| Principal geo-train-06 | 24 | 1.000.000 | A y B | 48 | 48.000.000 |
| Control geo-train-01 | 3 | 100.000 | A y B | 6 | 600.000 |
| Repetición exacta A/A del primer control | 0 | 100.000 | A | 1 | 100.000 |
| **Total** | **27** | — | — | **55** | **48.700.000** |

El tamaño inferencial principal es **N = 24.000.000 pares**, no 48 millones de observaciones independientes. Hay 24.300.000 primarios distintos contando los controles. Un bloque es una réplica nueva con semilla propia; se agrupan sumando transiciones, sin usar la desviación entre bloques como intervalo de confianza.

El [manifiesto de 55 corridas](ensayos/etapa-2-v1.1/corridas.csv) fija caso, vista, réplica, N, semilla de fuente y transporte. Principal: réplicas 101–124, fuente 2026100101–2026100124 y transporte 1026100101–1026100124. Control: réplicas 201–203, fuente 2026100201–2026100203 y transporte 1026100201–1026100203. No se reutilizan semillas de desarrollo. Dentro de cada lista IDs 0…N−1; la clave global es caso/vista/réplica/id.

La repetición `geo-train-01-r201-AA` debe usar **la misma lista, réplica, semilla y variante A** del original. `AA` solo identifica la carpeta/corrida, no un nuevo valor de `--variant`. No aporta tamaño estadístico.

## 4. Margen operativo y relación con niveles de conteo

Se adopta, antes de datos nuevos, el margen operativo propuesto por los estudiantes:

`M = sqrt(98) / 36.174.382 = 2,736603748 × 10⁻⁷ por primario = 0,273660375 cuentas por millón`.

Los 98 conteos de la ROI y 36.174.382 primarios provienen de la imagen histórica de referencia de geo-train-06/vista 0, documentados en la [entrega de etapa 1](https://github.com/anlegogo/muografia-documentada/blob/3a4977030a4193098ee66057fbd3c63603d7fa76/objetivo-1/entregas/2026-09-30-segundo-ensayo-etapa-1/RESULTADOS_ETAPA_1.md), sección 6. Son una escala fija de comparación, no una certificación de la geometría histórica ni de su equivalencia a 30 días reales.

**Justificación y límite:** se elige una desviación estándar de conteo Poisson de la ROI de referencia como resolución operativa para esta comparación. Es una elección de diseño, no una ley física ni un umbral de desempeño de redes neuronales. Si el cambio neto a estadística completa es M, en una imagen reducida a fracción f su cambio esperado es f·sqrt(98), y su relación con el ruido Poisson sqrt(f·98) es sqrt(f): 0,707; 0,316; 0,224; 0,100 para f=0,5; 0,1; 0,05; 0,01. Así se conecta el criterio con los niveles de conteo del OE1.

Esta motivación supone conteo Poisson a nivel de adquisición y reducción independiente. Los pares reducidos comparten referencia; no son réplicas independientes. El criterio afecta al **conteo neto de la ROI**: puede ocultar redistribución entre píxeles, por lo que los mapas y transiciones de bin se examinan aparte. No se modifica M tras ver resultados ni se infiere de la ausencia de discordancias del piloto.

## 5. Observable e incertidumbre

Para cada par, `Y_A,Y_B = 1` si el muón se detecta en R_int, y 0 en caso contrario. Definir n00, n01, n10 y n11; su suma debe ser N. `Delta = (n01−n10)/N`. Mostrar la estimación y el intervalo en probabilidad y en cuentas por millón.

Se fija un método conservador válido para conteos escasos, también sin discordancias:

1. Para p01 y p10 calcular intervalos binomiales exactos Clopper–Pearson bilaterales al **97,5 %** por separado: [L01,U01] y [L10,U10].
2. Construir `[L01−U10, U01−L10]` para Delta. Por la desigualdad de unión, los dos intervalos contienen simultáneamente sus parámetros con probabilidad al menos 95 %. No se supone independencia entre n01 y n10.
3. Es un intervalo conservador del efecto pareado, **no** un intervalo exacto óptimo para la diferencia. Requiere pares independientes de la misma distribución; compartir primario y estado inicial A/B no elimina la aleatoriedad entre pares.

La [documentación primaria de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html) describe el intervalo binomial exacto usado como componente. Nuestra combinación, nivel familiar y tamaño se fijan aquí. El [calculador](../herramientas/planificar_etapa2_oe1.py) implementa la inversión beta; sus pruebas la contrastan con `binomtest(...).proportion_ci(method='exact')`.

Con n01=n10=0, el intervalo es `±[1−0,0125^(1/N)]`, nunca cero. No se usa TOST al 90 % ni se cambia de método buscando una conclusión favorable.

| Escenario de diseño; no son resultados nuevos | Intervalo 95 % conservador, cuentas/millón | Decisión numérica |
|---|---|---|
| 0 discordancias | ±0,182584 | Dentro de ±M |
| 1 discordancia 0→1 | Extremo superior 0,265872; el inferior también queda dentro de ±M | Dentro de ±M |
| 2 discordancias 0→1 | Extremo superior 0,338427 | Inconcluso |

El [dimensionamiento reproducible](ensayos/etapa-2-v1.1/dimensionamiento.json) incluye ambos sentidos, discordancias compensadas y otros escenarios. Se eligen 24 millones para tolerar una discordancia y aun poder acotar el efecto, frente a los aproximadamente 14 millones preliminares basados en otro intervalo y cero discordancias. **No se promete potencia general ni un resultado concluyente con cualquier tasa.**

## 6. Regla de cierre y parada

Una sola evaluación confirmatoria al completar las 24 listas principales válidas:

- Intervalo estrictamente dentro de (−M,+M): efecto neto acotado al margen operativo, solo para esta ROI/caso/vista. No decir «la corrección no cambia nada» ni «toda la campaña es equivalente».
- Intervalo completamente por encima de +M o debajo de −M: diferencia neta relevante según el margen; cuantificar y usar B en la producción corregida.
- Cualquier otra ubicación, incluido tocar el límite: inconcluso. Puede haber un efecto distinto de cero sin probar relevancia o equivalencia.
- Fallos de contratos, datos faltantes o heterogeneidad de configuración: resultado no interpretable, con independencia de la decisión numérica.

Se permite parar por fallos técnicos, cuota, advertencias nuevas, seguridad operativa del clúster o discrepancia de control. No detenerse antes por equivalencia provisional, diferencia favorable o ausencia de cruces. No añadir bloques tras ver el intervalo. Un fallo se conserva; reintentar exactamente las mismas entradas/semillas en nueva carpeta, seleccionando el intento íntegro por criterios técnicos preestablecidos. No seleccionar resultados por su signo o magnitud.

Si N fijo resulta inconcluso, se informa como tal: no hay nueva simulación automática. La decisión posterior puede ser generar datos con B y conservar el impacto histórico como no acotado, o justificar por escrito otro diseño antes de datos adicionales. La producción con B no exige demostrar que A y B sean equivalentes.

## 7. Controles y diagnósticos que acompañan la conclusión

Antes del principal, ejecutar las siete corridas de control: tres A/B y una A/A. A/A debe repetir exactamente los resultados científicos, excluyendo rutas, tiempos y etiqueta administrativa. En geo-train-01, A/B no cambia la geometría: exigir correspondencia y ausencia de discrepancias científicas no explicadas antes del principal. El control pequeño es técnico, no un segundo ensayo de equivalencia con potencia igual al principal.

Para cada corrida y par principal:

- N filas completas, IDs únicos, SHA de lista y metadatos, FNV del primario recalculado y rng0 correspondiente A/B; estado final válido para cada evento. No exigir rng1 final igual en el caso afectado.
- Reconstruir exactamente el histograma desde todos los registros; verificar máscara, índices y flags ROI. Primario no detectado no equivale a primario perdido/ausente.
- B sin nuevas advertencias de solapamiento/navegación. En A solo se admite el defecto histórico declarado; no una lista abierta de errores.
- Informar transiciones ROI y detección total, por bloque y agregadas; histogramas A/B y diferencia normalizados por N; cambios de bin y conteo de pares detectados dentro de la ROI en ambas variantes pero en píxeles diferentes. No esconder cambios espaciales detrás de un Delta neto pequeño.
- Cruces 3D usando selección común: unión de IDs que cruzan en A o B. Reportar denominador, lado observado/inferido, longitudes, materiales y energía. No imponer que A/B tengan igual trayectoria. La partición de B en Z debe ser compatible con A1; discrepancias numéricas requieren análisis de cuerdas/dispersion y no relajación automática de tolerancia.
- Intervalos secundarios, si se presentan, son exploratorios sin garantía simultánea sobre todos los bins. Una estructura inesperada fuera de ROI obliga a limitar la interpretación, no a cambiar retrospectivamente el observable principal.

No se solicita otra campaña dirigida ni se cambian los binarios para reducir registros. Si una discrepancia concreta requiere trazas adicionales, documentarla por separado antes de modificar instrumentación.

## 8. Recursos y condiciones técnicas de arranque

Estimaciones escaladas del coste medido en etapa 1, **no mediciones de etapa 2**:

| Recurso | Estimación para las 55 corridas |
|---|---:|
| CPU de transporte, media | 11,44 horas CPU |
| Rango usando extremos históricos | 7,91–12,35 horas CPU |
| Registros completos CSV | 15,92 GB decimales |
| Esos registros comprimidos | 4,95 GB decimales |
| Una copia de listas de primarios | 3,54 GB decimales |
| Reserva operativa mínima | 30 GiB disponibles y dentro de cuota |

Los tiempos no incluyen espera en cola, generación, validación, compresión ni análisis; no son una promesa de tiempo de pared. Evitar duplicar listas idénticas A/B. Conservar CSV completo y copia comprimida mientras se verifica y transfiere; los 30 GiB contemplan ambos, listas y margen. Si se duplican insumos o se guardan reintentos adicionales, recalcular espacio antes de continuar.

Plan de trabajo: un CPU y un worker por corrida, memoria inicial solicitada 2 GiB por proceso, 45 min por bloque principal (coste histórico de transporte ~10–15 min). Esos valores son solicitudes iniciales que deben contrastarse con límites actuales de la partición. Mantener secuencial salvo que los estudiantes documenten una concurrencia permitida; varios procesos independientes no habilitan multihilo dentro del simulador.

**Antes de transportar**, registrar en `PREPARACION_ETAPA_2.md`:

1. Ruta real de trabajo y retención suficiente para revisión/descarga; salidas nuevas fuera del directorio con solo 596 MB disponibles según la medición anterior. Evidencia actual de espacio, cuota y permisos; no basta `df` si existe cuota de usuario.
2. Entorno, hashes congelados, controles geométricos y disponibilidad de ejecutables/tablas. Cualquier cambio de binario/entorno requiere revalidar su equivalencia técnica; no se presume.
3. Manifiesto, listas/sidecars con SHA, validadores de estructura/fuente y `--check-primaries` A/B. No regenerar una lista hasta que pase un test estadístico: conservar y explicar todo aviso.
4. Scripts adaptados al manifiesto, ensayo en seco de las 55 órdenes y verificación de conteos/seeds. Analizador con pruebas de conteos nulos, discordancias, IDs repetidos/faltantes e histograma incorrecto. Confirmar límite de eventos del binario para un millón por corrida.
5. Recursos SLURM efectivos y plan de recuperación sin sobreescribir intentos. Registrar el commit de esta preparación antes del primer transporte.

Cumplidas estas condiciones pueden ejecutar las siete corridas de control, verificarlas y continuar con los 48 transportes principales sin solicitar un nuevo diseño por cada bloque. Si no se cumplen, entregar el impedimento concreto. **Este documento no demuestra que exista ya esa cuota ni que los scripts SC3 estén adaptados**; esa preparación corresponde a los estudiantes en su entorno.

## 9. Entrega y camino al cierre de OE1

Carpeta nueva en rama de entrega de estudiantes, con `RESULTADOS_ETAPA_2.md`, `PREPARACION_ETAPA_2.md`, manifiesto ejecutado, versiones/huellas, scripts y comandos, registros de todos los intentos, recursos SLURM, transiciones por bloque, histogramas, mapas y análisis agregado. Datos grandes en almacenamiento compartido con acceso comprobado y SHA-256; evitar subir decenas de GB a Git. Mantener registros completos y no incluir exclusivamente detectados/cruces.

La revisión debe poder recuperar listas y registros, reconstruir histogramas y verificar N antes de aplicar el intervalo. El calculador de este repositorio recibe conteos: **no sustituye esa auditoría**. Entregar valores numéricos, incertidumbre, categoría de cierre y alcance, también si el resultado es nulo o inconcluso.

Tras revisar:

1. P-01: cuantificar este caso y decidir regeneración con B; revisar alcance en las otras cinco geometrías señaladas, sin extrapolar una vista. Usar controles existentes donde basten y definir controles adicionales solo para aspectos no cubiertos (por ejemplo recorte del edificio).
2. P-02/P-03: congelar entorno de producción y ruta reproducible; documentar sustitutos de scripts históricos ausentes.
3. P-04: justificar fuente, área y normalización de conteo en Geant4 con controles aplicables; la etiqueta temporal histórica no basta.
4. Producir el conjunto corregido dentro del alcance acordado, validar imágenes y reducciones de conteo, pares, metadatos y documentación. Solo entonces valorar cierre de OE1. Esto es producción y verificación final; no presupone una cadena ilimitada de ensayos exploratorios.

## 10. Material listo localmente

- [Manifiesto](ensayos/etapa-2-v1.1/corridas.csv) y [dimensionamiento](ensayos/etapa-2-v1.1/dimensionamiento.json), generados con `python herramientas/planificar_etapa2_oe1.py --out CARPETA_NUEVA`.
- [Calculador](../herramientas/planificar_etapa2_oe1.py): `python herramientas/planificar_etapa2_oe1.py --counts n00 n01 n10 n11`. Marca si N coincide con 24 millones; sus categorías son numéricas, no dictámenes automáticos.
- [Pruebas](../herramientas/test_planificar_etapa2_oe1.py): `python -m unittest discover -s herramientas -p test_planificar_etapa2_oe1.py -v`. Seis pruebas locales satisfactorias el 1 de octubre; [registro de validación local](evidencias/validacion-diseno-etapa2-v1.1.json). No prueban Geant4 ni SLURM.
- [Huellas del plan](ensayos/etapa-2-v1.1/SHA256SUMS.txt): verificar antes de preparar los insumos de SC3. La carpeta incluye atributos para preservar los bytes del manifiesto y del dimensionamiento.
- [Instrucción breve de ejecución](INSTRUCCIONES_ETAPA_2.md). El protocolo fija el diseño; los estudiantes completan la preparación operativa documentada en SC3.
