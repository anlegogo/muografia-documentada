# Discusión del ensayo de borde E1

2026-10-04, Colombia. Consolidación del ensayo E1 según las [instrucciones de cierre](../../INSTRUCCIONES_CIERRE_E1.md). Se parte del [borrador de la dirección](../../DISCUSION_E1_BORRADOR.md), de la [revisión independiente](../../REVISION_E1_804CE85.md) y de la entrega [804ce85](https://github.com/anlegogo/muografia-documentada/tree/804ce85f1bcb1e00d0956ae6bef26e69dd50130a/objetivo-2/entregas/2026-10-04-borde-cgan-f05).

- Las cifras regionales provienen del diagnóstico reproducido en esta entrega ([registro de cierre](REGISTRO_CIERRE_E1.md)).
- Las cifras por vista provienen del [análisis de las 54 comparaciones](../../evidencias/vistas-e1.json).
- No se realizó entrenamiento nuevo, no se modificaron coeficientes, semillas, épocas ni criterios, y no se abrieron test ni generalización.

Este documento describe un ensayo acotado. No declara el cierre del OE2 ni una aceptación física.

## 1. Propósito y diseño

El ensayo de repetición R1–R3 había mostrado que el término de conservación regional reducía el error del total de cuentas en el borde del cono, mientras aumentaba su error píxel a píxel. El [diagnóstico espacial](../../DIAGNOSTICO_ESPACIAL_CGAN.md) explicó esa coexistencia. El término regional compara cuentas integradas en cada región, de modo que permanece invariante si las cuentas se redistribuyen dentro de ella conservando la suma. Con base en esa observación se propuso E1. La pregunta fue si una penalización explícita del error espacial del borde reduce ese error sin deteriorar la conservación regional, el contraste ni la calidad de imagen.

Se compararon dos variantes de la cGAN corregida:

- **C0, control:** pérdida adversaria, 100·L1 y término regional de peso uno.
- **C1:** la misma pérdida más el término espacial de borde con peso 0,629. El peso se fijó con una regla aplicada a gradientes de doce lotes de entrenamiento, antes de observar resultados de validación.

Se ejecutaron tres parejas, B1, B2 y B3, con semillas 2026100411, 2026100412 y 2026100413. Cada pareja continuó cinco épocas desde el mismo checkpoint cGAN de la época 5 (SHA-256 `e54d51f7…57e0`), con optimizadores nuevos, sin parada temprana, y conservó la quinta época. Las parejas describen, por tanto, la variación de una continuación condicionada a un mismo punto de partida, no entrenamientos independientes desde cero. La regla de decisión fijada antes de ejecutar exige nueve controles simultáneos frente a C0:

1. Q menor.
2. Error espacial de borde estrictamente menor.
3. Ningún Q por geometría mayor.
4. Cielo no peor.
5. Borde no peor.
6. Soporte de contraste igual.
7. Error de contraste no mayor.
8. SSIM no menor.
9. PSNR no menor.

## 2. Resultados

La [tabla 1](#tabla-1) resume la entrega. El error espacial de borde se redujo en las tres parejas, de 11,05–11,26 % a 6,89–7,08 %, con reducciones relativas de 35,90 a 38,17 %. La reducción apareció en las 18 vistas de cada pareja, con disminuciones por vista de 3,42 a 4,88 puntos porcentuales. Ninguna pareja satisfizo los nueve controles. La síntesis prospectiva se clasificó como `dependencia_de_semilla_o_compromiso`, con `physical_acceptance: false`.

<a id="tabla-1"></a>**Tabla 1.** Error espacial de borde, Q global y controles por pareja (C1 frente a C0).

| Pareja | Borde C0 → C1 (%) | Reducción relativa | Q C0 → C1 (%) | Vistas con menor Q | Controles cumplidos |
|---|---:|---:|---:|---:|---:|
| B1 | 11,146 → 6,891 | 38,17 % | 6,233 → 4,802 | 14/18 | 6/9 |
| B2 | 11,263 → 7,045 | 37,45 % | 7,812 → 7,158 | 9/18 | 7/9 |
| B3 | 11,052 → 7,084 | 35,90 % | 5,018 → 5,486 | 6/18 | 5/9 |

El Q global disminuyó en B1 y B2 y aumentó en B3. Los controles que no se cumplieron variaron entre parejas:

- **Q de `geo-val-01`:** aumentó en las tres parejas.
- **Q de `geo-val-02`:** aumentó también en B2.
- **Q global:** aumentó en B3.
- **Cielo:** empeoró en B1.
- **Contraste:** empeoró en B2.
- **PSNR:** disminuyó en B1 y B3.
- **SSIM:** disminuyó en B3.

Las diferencias de SSIM y PSNR fueron pequeñas y de signo variable: la mediana entre parejas fue de +0,00006 en SSIM y −0,010 dB en PSNR.

**Excepciones por vista.** En `geo-val-01`, Q empeoró en cuatro de las seis vistas de B1 (V0, V3, V4 y V5) y en las seis vistas de B2 y B3. En `geo-val-02`, Q empeoró en tres vistas de B2 (V3–V5) y en tres de B3 (V0, V2 y V4). En `geo-val-03`, Q empeoró en tres vistas de B3 (V0, V3 y V5). Ninguna vista ni geometría se excluyó, y no se escogió una semilla favorable.

## 3. Diagnóstico de la geometría 1

En `geo-val-01` aumentó el sesgo medio de cuentas tanto en la roca como en el conducto ([tabla 2](#tabla-2)). C1 presentó exceso firmado de cuentas en las seis vistas de ambas regiones en las tres parejas. El deterioro no fue universal por vista: en B1, tres vistas del conducto no empeoraron, y en B3 una vista de roca tampoco.

<a id="tabla-2"></a>**Tabla 2.** Sesgo medio de cuentas en `geo-val-01`, promedio de seis vistas.

| Pareja | Roca: sesgo medio C0 → C1 (%) | Conducto: sesgo medio C0 → C1 (%) | Vistas con deterioro roca / conducto |
|---|---:|---:|---:|
| B1 | 5,383 → 6,662 | 9,769 → 10,446 | 6/6 y 3/6 |
| B2 | 7,007 → 7,645 | 10,500 → 13,367 | 6/6 y 6/6 |
| B3 | 4,749 → 4,911 | 5,559 → 12,623 | 5/6 y 6/6 |

Para localizar el exceso, cada región se dividió en tres bandas según la distancia euclidiana, en píxeles de la malla angular, al soporte de la máscara de borde: 0–2, 2–8 y más de 8 píxeles. Las contribuciones de las bandas usan el denominador de toda la región y suman el sesgo regional.

- **Conducto.** La banda a más de ocho píxeles aportó 9,779, 12,959 y 12,034 puntos porcentuales al sesgo de C1 en B1, B2 y B3. Esa misma banda contiene 876 de los 963 píxeles del conducto y el 99,5 % de sus cuentas de referencia. Por eso, su gran contribución integrada refleja dónde está la señal del conducto y no demuestra que cada píxel interior tenga mayor error relativo que los cercanos al borde.
- **Roca.** El aumento se reparte de forma distinta según la pareja. En B1 se concentra en la banda interior (1,868 → 3,660 puntos). En B2 aumenta menos de 0,35 puntos en cada banda. En B3 crece en la banda de 2–8 píxeles y disminuye ligeramente en la interior.

Los mapas reproducidos de las seis vistas por pareja ([B1](datos/reproduccion/mapas-B1-geo1.png), [B2](datos/reproduccion/mapas-B2-geo1.png), [B3](datos/reproduccion/mapas-B3-geo1.png)) muestran el error medio de C0, el de C1 y su diferencia, con el contorno del conducto. La escala es simétrica logarítmica, lineal entre −1 y +1 cuenta.

## 4. Interpretación

Los indicadores del ensayo miden propiedades distintas, lo que explica que una mejora del borde coexista con un exceso de cuentas en otras regiones:

- **El sesgo regional** resume la diferencia de cuentas integradas respecto de la referencia. Un valor bajo puede coexistir con una redistribución incorrecta entre píxeles.
- **El error espacial del borde** penaliza esa redistribución, pero solo dentro de la máscara del borde. No restringe directamente las cuentas de la roca ni de las anomalías situadas fuera de ella.
- **SSIM y PSNR** describen la similitud de la imagen normalizada, no la conservación de cuentas.

Por lo tanto, un contorno más preciso no garantiza conservar la señal del interior. Tampoco una reducción aislada de Q, o una mejora exclusiva del contorno, permite afirmar superioridad general.

La localización del exceso del conducto en su interior es una observación descriptiva. No identifica el mecanismo de optimización que la produjo. Los sondeos previos de gradientes mostraron oposición local entre el término de borde y la pérdida C1 en una muestra de entrenamiento, pero esos sondeos no representan la evolución del entrenamiento ni permiten atribuir causalmente el exceso observado.

Los porcentajes de este documento se refieren a cuentas respecto de referencias idealizadas, no a errores de densidad reconstruida. La entrada sin red tiene un Q de 1,81 %, menor que cualquier continuación, pero menor SSIM y PSNR. Esto confirma que la reducción de ruido y la conservación de cuentas deben valorarse por separado.

## 5. Límites y alcance

- Son tres continuaciones de cinco épocas desde un mismo checkpoint, evaluadas sobre tres geometrías de validación con seis vistas y veinte realizaciones cada una. No estiman la variabilidad entre entrenamientos independientes, no establecen significación estadística y no demuestran generalización.
- La validación ya se había usado en ensayos anteriores. E1 no es una confirmación independiente.
- Las bandas de distancia son una herramienta exploratoria de localización. No son distancias físicas ni umbrales de aceptación.
- Se conserva la clasificación original del ensayo. Los nueve controles no se reinterpretan a posteriori, y el resultado no justifica por sí solo prolongar el entrenamiento ni ajustar un nuevo coeficiente con validación.

## 6. Conclusión

E1 aporta evidencia de una mejora específica y repetida: el término espacial reduce el error del borde en todas las vistas de las tres parejas. También muestra un compromiso persistente, porque la conservación de cuentas empeora en `geo-val-01` en las tres parejas y los demás indicadores cambian de dirección según la semilla. El resultado permite presentar en el informe del OE2 una comparación explícita de ventajas y limitaciones. La demostración de calidad comparable a la alta estadística y la evaluación final siguen pendientes de un protocolo y de un criterio científico fijados por la dirección antes de abrir las particiones reservadas.
