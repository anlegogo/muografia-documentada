# Discusión del ensayo de borde E1

2026-10-04, Colombia. Consolidación del ensayo E1 según las [instrucciones de cierre](../../INSTRUCCIONES_CIERRE_E1.md). Se parte del [borrador de la dirección](../../DISCUSION_E1_BORRADOR.md), de la [revisión independiente](../../REVISION_E1_804CE85.md) y de la entrega [804ce85](https://github.com/anlegogo/muografia-documentada/tree/804ce85f1bcb1e00d0956ae6bef26e69dd50130a/objetivo-2/entregas/2026-10-04-borde-cgan-f05).

- Las cifras regionales provienen del diagnóstico reproducido en esta entrega ([registro de cierre](REGISTRO_CIERRE_E1.md)).
- Las cifras por vista provienen del [análisis de las 54 comparaciones](../../evidencias/vistas-e1.json); la tabla completa está en el anexo y las 72 filas de anomalías en [anomalias-e1.csv](datos/anomalias-e1.csv).
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

## 3b. Anomalías

En cada pareja se evaluaron 24 combinaciones de vista y anomalía: el conducto de `geo-val-01`, la cavidad de `geo-val-02`, y el conducto y el cuerpo denso de `geo-val-03`, cada uno en seis vistas. Las 72 filas, con soporte, cuentas de referencia y sesgo firmado de la cGAN inicial, C0 y C1, están en [anomalias-e1.csv](datos/anomalias-e1.csv).

- **Frente a C0:** C1 aumentó la magnitud del sesgo medio en 9 de 24 combinaciones en B1, 12 en B2 y 13 en B3.
- **Frente a la cGAN inicial:** la aumentó en 6, 7 y 6 combinaciones.
- **Por anomalía, el patrón cambia entre parejas.** En B1, los deterioros frente a C0 se concentraron en el conducto de `geo-val-03` (6 de 6 vistas) y en el conducto de `geo-val-01` (3 de 6). En B2 y B3 aparecieron en el conducto de `geo-val-01` (6 de 6), en la cavidad de `geo-val-02` (3 de 6) y en algunas vistas de `geo-val-03`.
- **El cuerpo denso de `geo-val-03` concentra los mayores sesgos firmados de C1** en las tres parejas: +17,7 % en B1 (V5; C0: +27,3 %), +32,3 % en B2 (V2; C0: +30,7 %) y +25,7 % en B3 (V5; C0: +22,0 %). Las referencias son de 163 a 210 cuentas, en 379 a 524 píxeles.

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

## Anexo. Las 54 comparaciones por vista

C1 frente a C0 en cada vista. Q y borde en porcentaje; las diferencias, en puntos porcentuales (negativo favorece a C1). Fuente: [vistas-e1.json](../../evidencias/vistas-e1.json), tabulado en [vistas-e1.csv](datos/vistas-e1.csv) con [tabular_vistas_anomalias.py](verificacion/tabular_vistas_anomalias.py).

| Pareja | Geometría | Vista | Q C0 → C1 (%) | Δ Q (pp) | Borde C0 → C1 (%) | Δ borde (pp) |
|---|---|---:|---:|---:|---:|---:|
| B1 | `geo-val-01` | V0 | 10,517 → 10,926 | +0,409 | 11,699 → 7,044 | -4,655 |
| B1 | `geo-val-01` | V1 | 9,083 → 8,964 | -0,119 | 11,636 → 6,849 | -4,786 |
| B1 | `geo-val-01` | V2 | 8,856 → 8,537 | -0,319 | 11,680 → 6,946 | -4,734 |
| B1 | `geo-val-01` | V3 | 5,433 → 8,097 | +2,664 | 11,789 → 7,034 | -4,755 |
| B1 | `geo-val-01` | V4 | 7,341 → 8,918 | +1,577 | 11,613 → 6,852 | -4,761 |
| B1 | `geo-val-01` | V5 | 4,227 → 5,882 | +1,655 | 11,732 → 6,902 | -4,829 |
| B1 | `geo-val-02` | V0 | 5,344 → 0,935 | -4,408 | 11,579 → 7,055 | -4,523 |
| B1 | `geo-val-02` | V1 | 6,576 → 4,875 | -1,701 | 11,485 → 7,087 | -4,398 |
| B1 | `geo-val-02` | V2 | 4,313 → 3,122 | -1,191 | 11,319 → 6,986 | -4,333 |
| B1 | `geo-val-02` | V3 | 3,692 → 1,959 | -1,734 | 11,362 → 7,061 | -4,301 |
| B1 | `geo-val-02` | V4 | 5,928 → 4,926 | -1,002 | 11,387 → 6,964 | -4,424 |
| B1 | `geo-val-02` | V5 | 4,928 → 3,018 | -1,910 | 11,335 → 7,062 | -4,274 |
| B1 | `geo-val-03` | V0 | 2,511 → 2,277 | -0,234 | 10,329 → 6,759 | -3,570 |
| B1 | `geo-val-03` | V1 | 6,479 → 1,492 | -4,988 | 10,102 → 6,567 | -3,535 |
| B1 | `geo-val-03` | V2 | 6,464 → 1,828 | -4,636 | 10,431 → 6,738 | -3,693 |
| B1 | `geo-val-03` | V3 | 6,984 → 2,646 | -4,339 | 10,348 → 6,681 | -3,667 |
| B1 | `geo-val-03` | V4 | 5,523 → 2,066 | -3,457 | 10,368 → 6,690 | -3,678 |
| B1 | `geo-val-03` | V5 | 7,997 → 5,970 | -2,027 | 10,431 → 6,760 | -3,670 |
| B2 | `geo-val-01` | V0 | 9,772 → 11,983 | +2,211 | 11,925 → 7,100 | -4,825 |
| B2 | `geo-val-01` | V1 | 7,712 → 10,801 | +3,089 | 11,807 → 7,026 | -4,781 |
| B2 | `geo-val-01` | V2 | 8,025 → 10,826 | +2,801 | 11,826 → 7,012 | -4,814 |
| B2 | `geo-val-01` | V3 | 9,341 → 10,018 | +0,677 | 11,913 → 7,176 | -4,736 |
| B2 | `geo-val-01` | V4 | 10,691 → 11,414 | +0,723 | 11,791 → 7,025 | -4,766 |
| B2 | `geo-val-01` | V5 | 6,979 → 7,993 | +1,014 | 11,968 → 7,092 | -4,876 |
| B2 | `geo-val-02` | V0 | 4,940 → 2,976 | -1,964 | 11,527 → 7,451 | -4,076 |
| B2 | `geo-val-02` | V1 | 5,937 → 3,853 | -2,084 | 11,394 → 7,463 | -3,931 |
| B2 | `geo-val-02` | V2 | 7,575 → 4,933 | -2,641 | 11,310 → 7,409 | -3,902 |
| B2 | `geo-val-02` | V3 | 4,443 → 8,106 | +3,663 | 11,401 → 7,481 | -3,921 |
| B2 | `geo-val-02` | V4 | 1,606 → 2,710 | +1,105 | 11,268 → 7,286 | -3,982 |
| B2 | `geo-val-02` | V5 | 3,738 → 8,749 | +5,012 | 11,257 → 7,375 | -3,882 |
| B2 | `geo-val-03` | V0 | 5,902 → 4,757 | -1,146 | 10,546 → 6,635 | -3,910 |
| B2 | `geo-val-03` | V1 | 9,992 → 4,301 | -5,690 | 10,340 → 6,504 | -3,836 |
| B2 | `geo-val-03` | V2 | 10,765 → 9,635 | -1,130 | 10,704 → 6,755 | -3,949 |
| B2 | `geo-val-03` | V3 | 9,152 → 2,109 | -7,043 | 10,586 → 6,616 | -3,970 |
| B2 | `geo-val-03` | V4 | 10,455 → 4,826 | -5,628 | 10,552 → 6,669 | -3,883 |
| B2 | `geo-val-03` | V5 | 13,585 → 8,858 | -4,727 | 10,616 → 6,729 | -3,887 |
| B3 | `geo-val-01` | V0 | 7,434 → 11,120 | +3,686 | 11,398 → 7,136 | -4,263 |
| B3 | `geo-val-01` | V1 | 5,647 → 9,392 | +3,745 | 11,228 → 6,903 | -4,325 |
| B3 | `geo-val-01` | V2 | 5,551 → 10,757 | +5,206 | 11,319 → 7,015 | -4,304 |
| B3 | `geo-val-01` | V3 | 4,322 → 7,689 | +3,367 | 11,446 → 7,057 | -4,389 |
| B3 | `geo-val-01` | V4 | 5,343 → 8,291 | +2,948 | 11,298 → 6,876 | -4,422 |
| B3 | `geo-val-01` | V5 | 2,630 → 5,352 | +2,722 | 11,407 → 6,961 | -4,446 |
| B3 | `geo-val-02` | V0 | 0,400 → 0,955 | +0,555 | 11,548 → 7,411 | -4,136 |
| B3 | `geo-val-02` | V1 | 8,524 → 3,889 | -4,635 | 11,394 → 7,389 | -4,005 |
| B3 | `geo-val-02` | V2 | 2,671 → 3,508 | +0,837 | 11,197 → 7,338 | -3,859 |
| B3 | `geo-val-02` | V3 | 10,177 → 4,689 | -5,488 | 11,376 → 7,401 | -3,975 |
| B3 | `geo-val-02` | V4 | 3,893 → 4,451 | +0,558 | 11,258 → 7,356 | -3,902 |
| B3 | `geo-val-02` | V5 | 3,742 → 3,638 | -0,104 | 11,218 → 7,399 | -3,820 |
| B3 | `geo-val-03` | V0 | 1,352 → 2,808 | +1,457 | 10,448 → 6,951 | -3,498 |
| B3 | `geo-val-03` | V1 | 5,684 → 2,523 | -3,161 | 10,231 → 6,810 | -3,421 |
| B3 | `geo-val-03` | V2 | 7,649 → 3,498 | -4,152 | 10,616 → 6,882 | -3,734 |
| B3 | `geo-val-03` | V3 | 2,254 → 2,986 | +0,733 | 10,510 → 6,888 | -3,621 |
| B3 | `geo-val-03` | V4 | 6,347 → 5,711 | -0,636 | 10,462 → 6,813 | -3,649 |
| B3 | `geo-val-03` | V5 | 6,698 → 7,489 | +0,791 | 10,587 → 6,926 | -3,661 |
