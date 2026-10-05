# Informe final de muografía — proyecto LaTeX para Overleaf

## Contenido
Proyecto completo con introducción, marco teórico, metodología, resultados y discusión, conclusiones y trabajo futuro, resumen, abstract, bibliografía y anexos. Los datos de identificación están en `datos.tex`.

## Carga y compilación
1. Cargar el ZIP como proyecto nuevo en Overleaf.
2. Seleccionar `main.tex` como documento principal y pdfLaTeX como compilador.
3. Compilar; la bibliografía usa biblatex-apa y Biber, gestionado automáticamente por Overleaf.

En local: ejecutar `pdflatex main`, `biber main` y dos veces `pdflatex main`.
No se requiere ejecutar Python para compilar el documento: los PDF de las figuras están incluidos.

## Figuras y datos
Las figuras se conservan en PDF vectorial. `Figuras/fuentes/` incluye fuentes editables, datos y las instrucciones de regeneración en su propio README. Los scripts verifican las huellas de sus datos de entrada. Las modificaciones de presentación no cambian los resultados experimentales.

## Convenciones de escritura
Usar redacción narrativa e impersonal; citar figuras, tablas y ecuaciones antes de presentarlas. Numerar cada expresión matemática y agrupar con subecuaciones cuando corresponda. Conservar las referencias automáticas y distinguir resultados observados, limitaciones y trabajo futuro.

## Revisión editorial
Consultar `LEEME_CORRECCIONES_FINALES.txt` para el alcance de las últimas correcciones. La revisión editorial no sustituye la aprobación académica del director.
