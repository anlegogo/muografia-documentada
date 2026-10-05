# Registro de cambios del manuscrito, versión 4 (OE2 y parte sustentada del OE3)

2026-10-04, Colombia. Base de la redacción: `anlegogo/muografia-documentada`, `origin/main` = **`08cdc0c`**. El texto base es la síntesis de la dirección (`objetivo-2/SINTESIS_OE2_TRANSICION_OE3.md`), junto con la revisión EF-01-C2, el protocolo EF-01, la entrega de la evaluación final (resultados y procedencia), las revisiones del piloto, del ajuste, de CG-04c, de R1–R3 y de E1, `DISCUSION_E1.md` y `objetivo-3/README.md`. No se ejecutaron entrenamientos, inferencias, ajustes ni campañas, y no se usó GPU.

Versión anterior: la v3 del libro de prueba, 2026-10-03, con el OE1 aprobado. Hay copia en `respaldo-libro-v3/` y en `base-v3/`. No se modificaron `main.tex` ni `settings.tex`.

## Capítulo 3 — Metodología

| Sección | Cambio |
|---|---|
| Encabezado | Se retiró la guía general de la plantilla. |
| 3.1.1 a 3.1.4 | Se añadió en cada subsección el párrafo correspondiente al OE2 y al OE3, en lugar de las guías. 3.1.4 incluye la **figura 3.2**, con el flujo del OE2 y del OE3 (TikZ; archivo `fig3-6_flujo_oe2.pdf`). Al insertarla, las figuras del OE1 se renumeran de 3.3 a 3.5; las referencias son automáticas. |
| 3.2.8 | **Única edición del texto del OE1.** Se reemplazó su última frase por una remisión: la implementación v1 sustituyó ambas convenciones de normalización por una escala ajustada solo con la partición de entrenamiento y no usó aumentos de datos. |
| 3.3 (nueva redacción completa) | Contiene: tarea; normalización v1 (ec. 3.11); generador U-Net y crítico PatchGAN (**figura 3.6**, TikZ, archivo `fig3-5_arquitecturas.pdf`, y **tabla 3.8**); pérdidas WGAN-GP con la corrección OE2-P01 (ec. 3.12); pérdidas regional y de borde (ec. 3.13); regla del coeficiente 0,629 (ec. 3.14); entrenamiento y secuencia de ensayos (**tabla 3.9**); criterios de ocho y nueve controles; corrección CG-04c (**algoritmo 3.5**); comparadores y ablaciones. |
| 3.4 (nueva redacción completa) | Contiene: protocolo EF-01 (**tabla 3.10**, con los métodos); **doce comparaciones** y regla de clasificación (ec. 3.15); ausencia de margen de equivalencia; **declaración de exposición previa**; SSIM y PSNR (ec. 3.16); regiones, Q, borde y contraste (ec. 3.17 y 3.18); corrección C2 (**algoritmo 3.6**); tratamiento de la dependencia; factor nominal E[N] = λt, f y R (ec. 3.19) y límites del análisis de exposición; generalización y sensibilidad. |
| 3.5.1 a 3.5.4 | Se añadieron, en lugar de las guías: el equipo y el software del OE2 (**tabla 3.12**), incluido el cambio de MATLAB a Python; la identificación de pesos, predicciones y controles; la verificación y reproducción en dos niveles; y los cambios respecto del plan, las decisiones de la dirección y las limitaciones. |

## Capítulo 4 — Resultados y discusión

| Sección | Cambio |
|---|---|
| Introducción | Se reescribe para tres secciones, una por objetivo, y se retira la guía. |
| 4.2 (nueva) | Contiene: ensayos de desarrollo en validación (**tabla 4.3**); integridad de EF-01; resultados globales (**tabla 4.4**, **figura 4.4** del compromiso); error de borde (**figura 4.5**); contraste antes y después de C2 (**tabla 4.5**) con el **cambio de interpretación de B1 en generalización**; doce comparaciones (**tabla 4.6**). |
| 4.3 (nueva) | Contiene: curvas descriptivas de exposición (**tabla 4.7**, **figura 4.6**); razones nominales; enunciado de que el factor alcanzable **no está demostrado**; discusión conjunta del OE2 y del OE3 sobre el texto propuesto por la dirección. |

## Capítulo 5 — Conclusiones y trabajo futuro

Se añadieron las conclusiones acotadas del OE2 (5.2) y del OE3 (5.3), una conclusión general (5.4) coherente con el OE1 y el trabajo futuro del modelo. En el trabajo futuro se separan las mejoras metodológicas de la aplicación de campo.

## Correcciones obligatorias de la dirección: dónde quedan

| Corrección | Ubicación |
|---|---|
| Doce comparaciones, seis por partición (el informe original decía nueve; en el libro solo figuran las doce) | 3.4.1; 4.2.5 y tabla 4.6 |
| Tablas de contraste C2 y comparación con el cálculo original | Tabla 4.5; 4.2.4 |
| B1 en generalización: C1 pasa a 0,090703 frente a 0,105524 de C0 | 4.2.4 y discusión |
| Rótulo «evaluación descriptiva sobre datos potencialmente expuestos» | 3.4.1; 4.2; pies de las tablas y figuras de EF-01 y del OE3 |
| No se afirma calidad comparable a alta estadística ni equivalencia física | 3.4.1; 4.3.3; 5.2; 5.4 |
| Factor: solo el nominal 1/f = 20, las razones R = f/0,05 y los cruces discretos; sin interpolar, extrapolar, calcular intervalos ni fijar umbrales; se declara no demostrado | 3.4.5; 4.3.2; 5.3 |
| Soporte de contraste del OE3 (21/11) distinto del de C2 (30/16): no se comparan | 3.4.5; 4.3.1 y pie de la tabla 4.7 |
| Resultados históricos de `dataset-v1.0`: no se presentan como resultados | Solo se menciona su existencia en la declaración de procedencia (3.4.1), sin cifras |
| Hallazgo del contraste de Geant4 frente al analítico | No se incluye |

## Bibliografía añadida

DOI verificados en Crossref o DataCite: `arjovsky2017`, `mirza2014`, `kingma2015`, `hore2010` y `blau2018`. Se añadió además el DOI a `ronneberger2015`, `isola2017`, `wang2004` y `gulrajani2017`.

## Verificación final

- latexmk sin errores, sin referencias ni citas indefinidas y sin cajas desbordadas.
- 92 páginas, en la copia de compilación y en el libro de prueba.
- Las 5 figuras nuevas son vectoriales: ninguna imagen raster (pdfimages) y fuentes incrustadas (pdffonts).
- Las tablas 4.4 a 4.7 se generan desde los JSON del repositorio, verificados con SHA-256, y coinciden con las tablas publicadas por la dirección.
- Cero `\GuiaRedaccion` en los capítulos 3, 4 y 5.

## Ajustes de redacción (versión 4.1, revisión de Rey)

No cambian las cifras, la estructura, las tablas ni las figuras.

1. En 4.2.5 se suprimió la frase sobre el informe original que contaba nueve comparaciones y la precisión de la dirección. Queda solo «las doce comparaciones fijadas en el protocolo, seis por partición».
2. Se suprimió «al cerrar esta versión» en 3.1.2, 4.3.2 y 5.3, con redacción impersonal: «quedaron pendientes de confirmación por la dirección», «como no se había fijado un criterio de calidad aceptable» y «que no se había fijado».
3. «Entrega original» se sustituyó por «selección original de controles» en el pie de la tabla 4.5 y por «cálculo original» en 4.3.3.
4. Se eliminó «su valoración académica corresponde a la dirección del proyecto» de las conclusiones 5.1 y 5.2. Se conservan las menciones del texto del OE1 en 3.2.1 y 4.1.5.

Verificación: latexmk sin errores, sin advertencias y sin referencias ni citas indefinidas; 92 páginas.

## Integración del informe académico del OE2 de la dirección (versión 4.2, revisión `166be6f`)

El 2026-10-04 a las 16:02, la dirección publicó el informe académico del OE2, la matriz de cumplimiento y el cierre documental. El único pendiente que deja a los autores es la **integración editorial OE2-D01**: incorporar el texto y las figuras al manuscrito, conservar las cifras C2 y sus limitaciones, y registrar la revisión. Se incorporó lo siguiente, sin cambiar ninguna cifra:

1. **Figuras 4.5 y 4.6:** la comparación fija de imágenes (vista 0 y realización 0 de las cuatro geometrías reservadas) y el caso desfavorable (geo-test-03, Q = 27,835 %), con las seis continuaciones y los residuos. Usan la misma regla de selección y las mismas matrices que el informe, verificadas con sus 36 huellas, y se regeneraron como PDF vectorial con las matrices a resolución nativa. Ambas se presentan en 4.2.3 antes de mostrarse. Las figuras de borde y de curvas pasan a ser la 4.7 y la 4.8.
2. **Discusión (4.3.3):** se añadieron dos ideas del informe. La U-Net superó a la cGAN original en SSIM y PSNR, de modo que la componente antagónica no mostró una ventaja global. La entrada escalada conservó mejor los promedios regionales, en coherencia con la esperanza condicional del adelgazamiento binomial.
3. **Conclusión del OE2 (5.2):** se añadió la formulación literal del objetivo según el plan de trabajo, y el grado de cumplimiento se alinea con la matriz de la dirección: «la calidad comparable a la de alta estadística queda respaldada solo de forma parcial».

Verificación: latexmk sin errores, sin advertencias y sin referencias ni citas indefinidas; 94 páginas. Las figuras nuevas no tienen fuentes sin incrustar y sus matrices están a 256 × 256 sin interpolación.

## Precisión de «calidad comparable» y continuidad del OE3 (versión 4.3, revisión `d45470b`)

El 2026-10-04 a las 16:23, la dirección precisó en su revisión `d45470b` dos puntos:

- La formulación del OE2 se refiere a la calidad de las imágenes y no establece la equivalencia física completa como condición independiente; esa condición no debe añadirse a posteriori, aunque para el uso muográfico deben discutirse las alteraciones de cuentas.
- Verificó por geometría que la cGAN al 5 % supera a la entrada sin red al 10 % en SSIM y PSNR.

Para el OE3 propuso que, sin un margen fundamentado, los resultados se mantengan como una comparación descriptiva explícita por métrica. Se incorporó lo siguiente, sin cambiar ninguna cifra existente:

1. **Tabla 4.8 nueva (4.3.1):** SSIM y PSNR de la cGAN al 5 % frente a la entrada al 10 %, por geometría. Se genera desde los JSON (resultados C2 y curvas) y sus 16 valores coinciden con la tabla de la dirección. Su texto precisa que la relación se cumple en las cuatro geometrías, que la cGAN queda por debajo de la entrada al 50 % en todas ellas (comprobado por geometría) y que ambas métricas se calculan frente a la misma referencia.
2. **4.3.2:** se indica que la superación de la entrada con el doble de conteos se cumple, para la cGAN, en cada geometría. También se precisa que, sin un criterio con margen fundamentado, los resultados se informan como una comparación descriptiva por métrica, sin un factor único que oculte el deterioro de la conservación de cuentas.
3. **5.2:** la conclusión adopta la formulación de la dirección. La cGAN supera en las cuatro geometrías a la imagen sin procesar con el doble de conteos y queda por debajo de la obtenida con diez veces más. La mejora no garantiza la conservación de cuentas, de modo que la calidad comparable queda respaldada solo de forma parcial. La equivalencia física completa no se añade a posteriori como condición del objetivo. Se retiró la frase que hacía depender la demostración de un margen físico de equivalencia.
4. **5.3:** se añadió la precisión por geometría y la comparación descriptiva por métrica en ausencia de un margen fundamentado.

El desglose por vista y región (OE3-P03) que la dirección propone como continuidad no se ejecutó: es un análisis adicional que no se pide para esta entrega.

Verificación: latexmk sin errores, sin advertencias y sin referencias ni citas indefinidas; 96 páginas. El diff palabra por palabra frente a la versión 4.2 muestra solo los cambios descritos.
