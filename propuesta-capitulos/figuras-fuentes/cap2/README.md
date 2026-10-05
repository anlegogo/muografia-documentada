# Fuentes de las figuras del capítulo 2

Las dos figuras del marco teórico son esquemas y curvas analíticas; no usan datos del proyecto.

| Figura | Fuente | Salida en `Figuras/` | Herramienta |
|---|---|---|---|
| 2.1 La imagen muográfica por transmisión como proyección | `fuentes/fig2-1_opacidad_proyeccion.tex` | `fig2-1_opacidad_proyeccion.pdf` | TikZ |
| 2.2 Relación señal-ruido y ruido relativo de un conteo de Poisson | `fuentes/fig2-2_ruido_conteo.tex` | `fig2-2_ruido_conteo.pdf` | PGFPlots |

## Regenerar

```bash
cd manuscrito/figuras-fuentes/cap2/fuentes
pdflatex fig2-1_opacidad_proyeccion.tex
pdflatex fig2-2_ruido_conteo.tex
cp fig2-1_opacidad_proyeccion.pdf fig2-2_ruido_conteo.pdf ../../../Figuras/
```

Requiere pdfLaTeX con TikZ, PGFPlots y la clase `standalone`. Ambas figuras usan la paleta Paul Tol «bright», la tipografía Latin Modern y el encabezado de las figuras TikZ del capítulo 3.

## Valores representados

- Figura 2.1(b): tres columnas con la misma opacidad, X = 1,06 × 10⁵ g cm⁻²: 400 m de roca de 2,65 g cm⁻³; 530 m de 2,00 g cm⁻³; 450 m con una cavidad de 50 m y 400 m de roca de 2,65 g cm⁻³.
- Figura 2.2: SNR = √λ y ruido relativo = 1/√λ para λ entre 1 y 10⁶. Los puntos marcan λ = 100 y λ = 400, donde cuadruplicar la exposición duplica la SNR.
