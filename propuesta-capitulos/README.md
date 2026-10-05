# Propuesta de capítulos de la tesis

2026-10-04, Colombia. Propuesta de los estudiantes, para revisión de la dirección, de los capítulos de la tesis *Reconstrucción muográfica por transmisión asistida por aprendizaje profundo mediante mejora predictiva de imágenes de baja estadística para exploración volcánica*.

Se construyó con lo documentado en este repositorio y se presenta para recibir observaciones. No reemplaza ninguna entrega ni modifica `main`, `originales/`, `objetivo-*/` ni las entregas previas.

- **Plantilla:** `main.tex` y `settings.tex` son los de la dirección, sin cambios.
- **Capítulos 3 y 4:** copias de los que la dirección integró en Overleaf el 2026-10-04 (`main` `9558099`).
  - El único ajuste es de referencias cruzadas en el capítulo 3: la opacidad y la esperanza del conteo remiten a sus ecuaciones del capítulo 2 en lugar de repetirlas.
- **Base en este repositorio:** la rama parte de `main` en `f0b8037`.

**Documento compilado:** [Propuesta_Capitulos_Tesis.pdf](Propuesta_Capitulos_Tesis.pdf), 86 páginas.

## Contenido y estado por capítulo

| Parte | Contenido | Estado |
|---|---|---|
| Resumen y abstract | Descripción del trabajo y resultados | **Ajustados (2026-10-04)** al resultado de la evaluación multifracción, al factor no demostrado y al alcance sobre anomalías |
| 1. Introducción | Problema, justificación, objetivos (texto literal de la propuesta aprobada), alcance y estructura | **Ajustada (2026-10-04)** con el mismo criterio que el capítulo 5: OE3 evaluado en cuatro fracciones sin factor demostrado, sin causa atribuida, y anomalías evaluadas en regiones de ubicación conocida |
| 2. Marco teórico | Muones y su paso por la materia; imagen por transmisión (opacidad, proyección, no unicidad); estadística de conteo (Poisson, adelgazamiento binomial, Clopper–Pearson, Bonferroni, compresión logarítmica); simulación con Geant4 y EcoMug; aprendizaje profundo (U-Net, GAN condicional, crítico de parches, Wasserstein y penalización del gradiente); métricas de similitud y de conservación; estado del arte | **Completo, versión 2.** Contiene solo los conceptos que usa el capítulo 3, en el orden en que los necesita y con su misma notación. Tiene tres figuras vectoriales con fuente en `Figuras/fuentes/` |
| 3. Metodología | Texto de la dirección en Overleaf | **Completo** (dirección) |
| 4. Resultados y discusión | Texto de la dirección en Overleaf | **Completo** (dirección) |
| 5. Conclusiones y trabajo futuro | Conclusiones directas por objetivo (logrado y no demostrado); conclusión general con el alcance sobre anomalías; trabajo futuro como posibles líneas de continuación | **Versión 2 (2026-10-04)**, ajustada según las observaciones de la dirección |
| Anexo A | Protocolo propuesto para estimar el factor de reducción (pseudocódigo con entradas, salidas y pasos) | **Nuevo.** Se referencia desde la sección 5.5 |

## Cambios del capítulo 5 según las observaciones de la dirección

1. **Conclusiones por objetivo:** cada una dice qué se logró y qué no se demostró, solo con los resultados principales. El detalle remite al capítulo 4.
2. **OE3:** la evaluación se realizó, pero con el criterio adoptado no se demostró un factor de reducción. Se dice así, sin compensarlo con trabajo futuro.
3. **Inversión de opacidad e instrumento real:** se presentan como investigación posterior, no como tareas pendientes.
4. **Trabajo futuro en condicional:** «se propone investigar», «permitiría evaluar», «no garantiza».
5. **Tabla 5.1:** la columna «Causa de la brecha» pasa a «Limitación identificada». Las explicaciones no comprobadas se presentan como hipótesis.
6. **Anomalías:** la conclusión general precisa que los indicadores se calcularon en regiones de ubicación conocida y que no demuestran la detección ni la localización de anomalías desconocidas.
7. **Líneas de trabajo futuro:** cada una tiene un párrafo breve (qué, por qué, qué permitiría evaluar). El algoritmo pasó al anexo A.
8. **Tabla 5.1 legible:** tabularx con cuatro columnas de ancho controlado, booktabs y texto conciso.
9. **Última página:** el capítulo termina en una página con contenido suficiente.

Con el mismo criterio se ajustaron el alcance de la introducción, el resumen y el abstract.

## Capítulo 2: criterio y conceptos

El capítulo explica el fundamento y deja el procedimiento al capítulo 3. No adelanta decisiones ni resultados. Cada concepto se incluyó porque el capítulo 3 lo usa sin explicar su fundamento:

- **Física del muón:** flujo, dependencia cenital y parametrización de Guan; pérdida de energía y energía mínima; dispersión múltiple.
- **Imagen por transmisión:** opacidad como integral de línea; transmisión; proyección frente a volumen; no unicidad espesor–densidad; diferencia entre contraste de cuentas y opacidad.
- **Estadística de conteo:** proceso de Poisson y E[N(t)] = λt; ruido relativo; referencia finita; adelgazamiento binomial; intervalos de Clopper–Pearson; corrección de Bonferroni; compresión logarítmica.
- **Simulación:** Monte Carlo con Geant4; lista de física; corte de producción frente a umbral de registro; materiales de referencia; EcoMug; brecha entre simulación y realidad.
- **Aprendizaje profundo:**
  - aprendizaje supervisado y Adam; validación y fuga de información;
  - redes convolucionales y campo receptivo; U-Net;
  - pérdida L1; GAN condicional y crítico de parches;
  - distancia de Wasserstein y penalización del gradiente.
- **Métricas:** MSE, PSNR y SSIM; compromiso entre distorsión y percepción; sesgo regional y error espacial; borde; contraste y signo; indicadores locales.

Respecto de la versión 1 se retiró lo que el capítulo 3 no usa:
- el tiempo de detección de una anomalía;
- el riesgo de alucinación;
- la inversión conjunta con gravimetría;
- la fórmula de Highland;
- el detalle de aplicaciones volcánicas, que queda resumido en el estado del arte.

Todas las referencias del capítulo tienen DOI o identificador arXiv verificados. La única nueva es `goodfellow2014` (arXiv:1406.2661). Se añadieron también `repositorioMuografia2026` y `propuestaCapitulos2026`, que citan los capítulos 3 y 4 de la dirección.

## Cómo compilar

Desde esta carpeta, con pdfLaTeX y Biber: pdfLaTeX → Biber → pdfLaTeX → pdfLaTeX, o bien

```bash
latexmk -pdf main.tex
```

El resultado son 86 páginas, sin errores, sin referencias o citas indefinidas y sin cajas desbordadas. Las figuras de los capítulos 2, 3 y 4 están en `Figuras/`, todas en PDF vectorial.

Sus fuentes están en `Figuras/fuentes/`: un `.tex` o `.py` por figura con el mismo nombre que su PDF, junto con los datos verificados por SHA-256, `generar_figuras.py`, `requirements.txt` y `README.md`. Para regenerar las 20 figuras y comprobar que son vectoriales:

```bash
pip install -r Figuras/fuentes/requirements.txt
python Figuras/fuentes/generar_figuras.py
```

Regeneradas así en una copia aparte, las 20 coinciden píxel a píxel con los PDF publicados. La carpeta `figuras-fuentes/` conserva como antecedente las fuentes de versiones anteriores (`fig3-*`, `fig4-*`) y las tablas del OE2.

## Puntos que requieren decisión de la dirección

1. **Declaración de uso de herramientas de IA.** El documento no contiene ninguna. Se solicita indicar si debe incluirse y dónde: en los preliminares, en la metodología o en un anexo.
2. **`\nocite` en `main.tex`.** La plantilla conserva un `\nocite` de siete referencias con la indicación de retirarlo cuando el texto tenga sus citas definitivas. Las siete ya se citan en el texto. Como `main.tex` es de la dirección, no se modificó.
3. **Ajuste de referencias cruzadas en el capítulo 3.** Para no repetir ecuaciones del capítulo 2, la opacidad y la esperanza del conteo del capítulo 3 remiten a sus ecuaciones del capítulo 2. Si la dirección prefiere conservarlas en el capítulo 3, se revierte sin otros efectos.
