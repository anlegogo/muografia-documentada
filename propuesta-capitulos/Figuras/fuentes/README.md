# Fuentes de las figuras del capítulo 2 (Marco teórico)

Las tres figuras son esquemas y curvas analíticas. No usan datos del proyecto ni imágenes externas.
- Se generan desde estas fuentes con herramientas de código abierto: TikZ y PGFPlots.
- Salen como PDF vectorial, sin imágenes raster incrustadas.
- La notación es la del capítulo 3: α, η, X, ρ, l, L, λ, t, **u**, **y**, G_θ, D_φ, S_φ.
- Usan la paleta Paul Tol «bright».

| Figura | Fuente | PDF en `Figuras/` | Herramienta |
|---|---|---|---|
| 2.1 La imagen muográfica por transmisión como proyección | `fig2-1_opacidad_proyeccion.tex` | `fig2-1_opacidad_proyeccion.pdf` | TikZ |
| 2.2 Estadística de conteo de Poisson | `fig2-2_ruido_conteo.tex` | `fig2-2_ruido_conteo.pdf` | PGFPlots |
| 2.3 Red generativa antagónica condicional de Wasserstein | `fig2-3_gan_condicional.tex` | `fig2-3_gan_condicional.pdf` | TikZ |

## Regenerar

```bash
python generar_figuras.py
```

El script hace tres cosas:
1. compila cada fuente con pdfLaTeX en un directorio temporal;
2. copia el PDF a `Figuras/`;
3. comprueba con `pdfimages` y `pdffonts` que no haya raster y que las fuentes estén incrustadas.

Los requisitos están en `requirements.txt`: solo la biblioteca estándar de Python, más pdfLaTeX con TikZ y PGFPlots. También puede compilarse cada fuente a mano con `pdflatex <fuente>.tex`.

## Valores representados

- **Figura 2.1(b):** tres columnas con la misma opacidad, X = 1,06 × 10⁵ g cm⁻². Se comprueba con X = 100 ρ L (L en m, ρ en g cm⁻³):
  - 400 m de roca de 2,65 g cm⁻³;
  - 530 m de 2,00 g cm⁻³;
  - 450 m que incluyen una cavidad de 50 m, es decir, 400 m de roca de 2,65 g cm⁻³.
- **Figura 2.2:** curvas analíticas √μ y 1/√μ para μ = λt entre 1 y 10⁶. Los puntos μ = 100 y μ = 400 muestran que cuadruplicar la exposición duplica el cociente entre media y desviación estándar.
- **Figura 2.3:** esquema conceptual sin dimensiones de capas. La arquitectura implementada se describe en el capítulo 3.
