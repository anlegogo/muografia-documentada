# Reglas para mantener la documentación

1. El README principal es la entrada; el índice enlaza los documentos activos. Evitar archivos paralelos llamados «final», «final2» o «último».
2. Toda actualización material añade una entrada fechada a `CHANGELOG.md` y a la bitácora del objetivo afectado: actividad, evidencia, resultado, limitación y siguiente paso.
3. La matriz usa estados **verificado**, **reportado**, **parcial** y **pendiente**. «Verificado» exige nombrar el control y su evidencia; no implica validación física automática.
4. Cada pendiente conserva un identificador estable, evidencia, criterio de cierre y estado. Una corrección debe conservar el antes y el después.
5. No editar archivos de `originales/` ni sustituir binarios bajo el mismo nombre. Incorporar una nueva entrega con revisión, inventario y comparación; ensayos derivados se guardan fuera de esa carpeta.
6. Separar fecha del experimento, fecha declarada por los autores y fecha de nuestra revisión. La bitácora de simulación recibida es retrospectiva.
7. Documentar entorno, comando, entradas y salidas de cada ejecución. Registrar fallos y advertencias, además de los resultados satisfactorios.
8. Al crear un Markdown, enlazarlo desde el índice o desde el documento que lo introduce. Los enlaces nuevos son relativos dentro de la réplica.
9. OE2 y OE3 se incorporarán solo cuando se amplíe expresamente el alcance. Una dependencia de preparación de datos no constituye una evaluación de modelos.

## Plantilla de entrada de bitácora

```text
Fecha y zona horaria:
Actividad y responsable:
Entradas / revisión:
Comando o procedimiento:
Evidencia / salidas:
Resultado y limitaciones:
Pendientes vinculados:
```
