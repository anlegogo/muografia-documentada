# Borrador académico del objetivo específico 1

Versión del 2026-10-03. Se preparó un texto descriptivo e impersonal que integra metodología, desarrollo matemático, resultados, discusión y una conclusión acotada del OE1. Conserva la distinción entre ejecución estudiantil en SC3 y revisión técnica de la dirección.

- [Leer el PDF, 11 páginas](BORRADOR_OE1.pdf).
- [Fuente LaTeX editable](BORRADOR_OE1.tex).
- [Validación numérica y editorial](VALIDACION.json): 18 controles satisfactorios y revisión visual de las once páginas.

El PDF y el archivo LaTeX contienen el mismo borrador. Se propone una nomenclatura explícita compatible con los campos de datos y con el residuo del evaluador de bordes. La plantilla del informe no contenía una nomenclatura matemática desarrollada que pudiera reproducirse literalmente. Al integrar otros capítulos deberá conservarse esta correspondencia o realizarse un cambio global documentado de símbolos.

| Parte del borrador | Destino en el informe |
|---|---|
| Alcance y tabla de símbolos | Introducción de la metodología del OE1 o lista de nomenclatura. |
| Generación, fuente, transporte, malla, pares y particiones | Generación y preparación del conjunto sintético. |
| Integridad y criterios de bordes y roca | Procedimiento de verificación, antes de presentar resultados. |
| Cifras de campaña, excepciones y distribución | Resultados del OE1. |
| Dependencia estadística, representatividad y límites físicos | Discusión. |
| Conclusión propuesta | Balance del OE1, sujeto a revisión académica. |

## Criterio matemático y nomenclatura

Se reserva `N` para primarios transportados, `C` para conteos de referencia, `L` para conteos reducidos y `X` para columna de masa. Los índices `i` y `j` corresponden a elevación y azimut. Se definen expresamente los índices de geometría, vista, región y realización.

El texto desarrolla la ley binomial condicional, sus momentos y la dependencia inducida por la referencia compartida. Distingue el adelgazamiento de una nueva simulación con un presupuesto fijo menor. Formula el residuo de bordes, la corrección sobre 114 × 16 probabilidades y la condición de que el intervalo completo esté dentro de la tolerancia. Las probabilidades tabuladas se tratan como fijas; esa cobertura no incluye incertidumbre del modelo físico.

Las tres figuras verificadas se enlazan desde el PDF, con sus leyendas propuestas, y permanecen disponibles en la [síntesis ilustrada](../SINTESIS_RESULTADOS_OE1.md). El documento autónomo no incorpora archivos gráficos externos: las figuras se insertarán al integrar el manuscrito. No se generaron resultados nuevos ni se reutilizaron cifras históricas como si correspondieran a esta campaña.

## Fuentes y límites editoriales

Se contrastaron la [receta](../contratos/receta-operativa-siete-actividades.json), el exportador angular, el empaquetador, los evaluadores, la [evaluación desde píxeles](../evidencias/revision-datos-f395570/evaluacion-local.json) y la [revisión de Drive](../REVISION_DISTRIBUCION_DRIVE.md). Las referencias del proyecto se fijan al commit `4529c49`. Se consultaron las fuentes oficiales de Geant4, EcoMug y el registro del artículo de Guan para las referencias bibliográficas; no se atribuye a esos antecedentes una validación de la fuente híbrida implementada.

El ejemplo geométrico de `geo-train-06` conserva la huella de la receta. La tabla de excepciones y los valores globales se contrastaron con la evaluación. Las identidades estadísticas se desarrollan bajo las hipótesis declaradas; no representan ensayos físicos adicionales.

La versión local de `Informe_Final_Muografia` permanece como plantilla. Este documento es un borrador de la dirección para revisión e incorporación, no una entrega redactada o aprobada por los estudiantes. P-04 y A-02 continúan abiertos. Deben revisarse la justificación de representatividad, el enunciado literal del plan y la concordancia con los capítulos que se incorporen posteriormente.

## Compilación

Se abrió la fuente en el editor de LaTeX. Su compilador integrado informó `Unable to find standard directories for platform`. Como alternativa se utilizó la instalación local existente de pdfLaTeX (TeX Live 2025), sin instalar dependencias. La compilación final no presenta referencias indefinidas ni cajas desbordadas; todas las páginas se renderizaron e inspeccionaron.

Desde la raíz del repositorio, crear un directorio de salida y ejecutar hasta resolver las referencias cruzadas:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=SALIDA objetivo-1/manuscrito/BORRADOR_OE1.tex
```

El PDF se conserva junto a su fuente para lectura inmediata. Los auxiliares de compilación no forman parte de la entrega.
