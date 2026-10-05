# Propuesta de capítulos de la tesis

2026-10-04, Colombia. Propuesta de los estudiantes, para revisión de la dirección, de los capítulos de la tesis *Reconstrucción muográfica por transmisión asistida por aprendizaje profundo mediante mejora predictiva de imágenes de baja estadística para exploración volcánica*.

Se construyó con lo documentado en este repositorio y se presenta para recibir observaciones. No reemplaza ninguna entrega ni modifica `main`, `originales/`, `objetivo-*/` ni las entregas previas.

- **Plantilla:** `main.tex` y `settings.tex` son los de la dirección, sin cambios.
- **Origen:** manuscrito de los autores en `muography-thesis`, rama `docs/caps-1-2`, commit `be8dc79`.
- **Base en este repositorio:** la rama parte de `main` en `f0b8037`.

**Documento compilado:** [Propuesta_Capitulos_Tesis.pdf](Propuesta_Capitulos_Tesis.pdf), 93 páginas.

## Contenido y estado por capítulo

| Parte | Contenido | Estado |
|---|---|---|
| Resumen y abstract | Descripción del trabajo y resultados con las cifras C2 | **Completo** respecto de OE1 y OE2. Falta añadir el resultado del complemento OE3-C1 y el cierre del OE3 |
| 1. Introducción | Problema, justificación, objetivos (texto literal de la propuesta aprobada), alcance y estructura | **Completo** |
| 2. Marco teórico | Muones cósmicos, pérdida de energía, formación de la imagen, estadística de conteo, aprendizaje profundo, aprendizaje automático en muografía, datos sintéticos y métricas (§2.1–2.8) | **Completo** |
| 3. Metodología | OE1 (campaña de 114 vistas); OE2 (implementación v1, U-Net y crítico PatchGAN, WGAN-GP con las correcciones OE2-P01 y CG-04c, ensayos de desarrollo y protocolo EF-01 con la corrección C2); OE3 (factor nominal y curvas descriptivas) | **Parcial.** Completo hasta `d45470b`. No describe el protocolo del complemento OE3-C1. **Debe conciliarse con el capítulo 3 que la dirección montó en Overleaf el 2026-10-04**, con recuadros `met_01` a `met_09`: las nueve figuras `met_*` están en `Figuras/`, con sus fuentes, pero aún no se insertan en el texto, que conserva las figuras `fig3-*` |
| 4. Resultados y discusión | Capítulo reservado: título y secciones de OE1, OE2 y OE3, sin contenido | **Retirado de esta propuesta.** Queda pendiente de integrarse a partir del informe de la dirección (`informe-final/04_RESULTADOS.md` y `05_DISCUSION_CONCLUSIONES.md`, `main` `9558099`). Se conservan las etiquetas de sección para que las referencias de los demás capítulos se resuelvan, y se retiraron sus ocho figuras |
| 5. Conclusiones y trabajo futuro | Conclusiones por objetivo, conclusión general y trabajo futuro | **Parcial.** OE1 y OE2 completos. La conclusión del OE3 debe incorporar la formulación del cierre (`f0b8037`) |
| Anexos | — | **Pendiente** |

## Evidencia en que se sustenta cada objetivo (commits de este repositorio)

| Objetivo | Incorporado en la propuesta | Publicado después y aún no incorporado |
|---|---|---|
| OE1 | Síntesis de resultados del OE1 (`4529c49`); entrega de la campaña (`f395570`); rama de entrega `oe1/justificacion-fisica-produccion` (`800ab86`) | — |
| OE2 | Evaluación final y corrección C2 (`1214307`); informe académico y matriz de cumplimiento (`166be6f`); precisión sobre calidad comparable (`d45470b`) | — |
| OE3 | Curvas descriptivas de exposición (`08cdc0c`); comparación por geometría (`d45470b`) | Desglose por vista (`4a74e55`); revisión de la propuesta (`f1094d7`); protocolo OE3-C1 (`39d8fd3`); entrega y auditoría OE3-C1 (`5c3b0ee`, `64ca8b2`); opacidad nominal (`d7c865a`); cierre del OE3 (`f0b8037`) |

## Cómo compilar

Desde esta carpeta, con pdfLaTeX y Biber: pdfLaTeX → Biber → pdfLaTeX → pdfLaTeX, o bien

```bash
latexmk -pdf main.tex
```

El resultado son 93 páginas, sin errores ni referencias o citas indefinidas. Las figuras están en `Figuras/` en PDF vectorial. Sus fuentes (TikZ, Matplotlib y PGFPlots) y los datos verificados por SHA-256 están en `figuras-fuentes/`:

| Carpeta | Contenido | README |
|---|---|---|
| `cap2/` | Figuras del capítulo 2 | `figuras-fuentes/cap2/README.md` |
| `oe1-v3/` | Figuras del OE1 | `figuras-fuentes/oe1-v3/README.md` |
| `oe2-v4/` | Figuras y tablas del OE2 y del OE3 | `figuras-fuentes/oe2-v4/figuras/README.md` |
| `cap3-metodologia/` | Figuras `met_*` | `figuras-fuentes/cap3-metodologia/README.md` |

Los datos de figuras se conservan con sus bytes exactos (ver `.gitattributes`). El historial de cambios del texto está en `figuras-fuentes/oe2-v4/REGISTRO_CAMBIOS.md`.

## Puntos que requieren decisión de la dirección

1. **Declaración de uso de herramientas de IA.** El documento no contiene ninguna. Se solicita indicar si debe incluirse y dónde: en los preliminares, en la metodología o en un anexo.
2. **`\nocite` en `main.tex`.** La plantilla conserva un `\nocite` de siete referencias con la indicación de retirarlo cuando el texto tenga sus citas definitivas. Las siete ya se citan en el texto. Como `main.tex` es de la dirección, no se modificó.
3. **Criterio de calidad para el factor de reducción.** El texto informa el factor nominal 1/f = 20, las razones nominales y las comparaciones descriptivas, y declara que el factor alcanzable no está demostrado. Se solicita confirmar cómo debe presentarse en el libro:
   - el benchmark operativo del complemento OE3-C1 (referente sin red al 50 %, con resultado nulo);
   - la comparación descriptiva 2:1 frente a la entrada al 10 %;
   - u otro criterio.
4. **Hallazgo del contraste de Geant4.** El contraste de Geant4 resultó unas diez veces más débil que el del motor analítico. No se incluyó en el libro y queda a decisión de la dirección.
