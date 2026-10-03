# Informe de cierre del objetivo específico 1

**OE1 cumplido y cerrado por decisión de la dirección el 2026-10-03, dentro del alcance idealizado adoptado.** El texto integra el objetivo aprobado, la justificación de representatividad, metodología, ecuaciones, resultados, tres figuras, discusión y conclusión de cumplimiento.

- [Informe en PDF, 15 páginas](INFORME_OE1.pdf).
- [Fuente LaTeX editable](INFORME_OE1.tex).
- [Decisión y registro de cierre](../CIERRE_OE1.md).
- [Evidencia del plan y las 19 geometrías](EVIDENCIA_CIERRE.json).
- [Validación numérica y editorial](VALIDACION.json).

La ejecución en SC3 se atribuye a los estudiantes; la revisión técnica y consolidación documental a la dirección. El cierre del objetivo no se presenta como aprobación institucional de la tesis. La incorporación de este informe al documento global y su presentación por los estudiantes no constituyen nuevas tareas de generación o verificación del OE1.

## Contenido y nomenclatura

La formulación reserva N para primarios transportados, C para cuentas de referencia, L para cuentas reducidas y X para columna de masa. Los índices de píxel corresponden a elevación y azimut, con centros y bordes diferenciados. Se formalizan el adelgazamiento binomial, sus momentos y dependencia, el contraste de bordes con corrección simultánea y la meta descriptiva de roca.

La representatividad se justifica mediante edificios cónicos de distintas dimensiones, control homogéneo, déficits y excesos de masa, combinaciones y vistas. Se acepta para un estudio sintético controlado, sin afirmar cobertura estadística de volcanes reales. Se corrigió una frase del borrador: geo-train-01 es homogénea; geo-gen-01 contiene un conducto y dos cavidades. No se modificaron los datos.

Las tres figuras científicas están incorporadas en el PDF, con leyendas y referencias cruzadas. Las siete vistas bajo la meta del 90 %, el ruido de referencia, la fuente híbrida, el registro computacional y la exposición convencional se conservan explícitos. No se declara una reducción física de tiempo de adquisición ni desempeño de redes.

## Verificación y reproducción editorial

Se contrastó el enunciado del plan (sección 4.2, página impresa 9), se verificaron las 19 huellas del catálogo contra la receta y se comprobaron cifras, coordenadas, excepciones e identidades estadísticas. Los 18 controles del texto anterior se repitieron satisfactoriamente sobre el informe. La evidencia adicional conserva los parámetros del catálogo y la huella del plan. Las 15 páginas se renderizaron para revisión visual.

El compilador integrado del editor no encontró sus directorios de entorno. Se utilizó pdfLaTeX de TeX Live 2025, ya instalado, con referencias resueltas y sin desbordamientos. No se instalaron dependencias. Desde la raíz del repositorio, crear una carpeta de salida y ejecutar hasta resolver las referencias:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=SALIDA objetivo-1/manuscrito/INFORME_OE1.tex
```

La fuente requiere los tres PDF de objetivo-1/figuras/cierre-2026-10-03/, conservados en el repositorio. El borrador anterior se mantiene en el [historial 24c9066](https://github.com/anlegogo/muografia-documentada/tree/24c9066/objetivo-1/manuscrito); la versión vigente es este informe. No se mantienen versiones paralelas de cierre.
