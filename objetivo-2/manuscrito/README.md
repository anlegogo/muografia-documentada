# Informe académico del OE2

El [informe redactado](INFORME_OE2.md) reúne método, entrenamiento, resultados y discusión. Sus [tablas completas](TABLAS_OE2.md) y [matriz de cumplimiento](../MATRIZ_CUMPLIMIENTO.md) permiten incorporarlo al manuscrito oficial. El [registro de cierre documental](../CIERRE_OE2.md) distingue ejecución terminada de cumplimiento científico parcial.

## Material entregado

- `INFORME_OE2.md`: texto académico impersonal y ecuaciones, con las figuras introducidas antes de mostrarlas.
- `TABLAS_OE2.md`, `resumen.csv` y `geometrias.csv`: 18 resúmenes y 36 filas por geometría, derivados de C2; los CSV conservan precisión numérica completa.
- `figuras/comparacion-fija.png`: cuatro geometrías, vista 0 y realización 0; referencia, entrada, U-Net y cGAN.
- `figuras/caso-desfavorable.png`: caso elegido por mayor Q de cGAN, con las seis continuaciones y residuos en escala común.
- `figuras/procedencia-figuras.json`: regla de selección, índices, escala y huellas de 36 entradas y del informe C2.

## Reproducción de figuras

Requiere Python, NumPy y Matplotlib, con las matrices de datos y predicciones previamente auditadas. No descarga datos, ejecuta redes ni entrena. Desde la raíz del repositorio:

```powershell
python objetivo-2/herramientas/figuras_cierre_oe2.py --datos RUTA/dataset-v2/shards --predicciones RUTA/predictions --resultados objetivo-2/evidencias/ef01-c2/resultados.json --salida RUTA/figuras
```

Cada carpeta de modelo bajo `predictions` contiene cuatro NPY de forma 120 × 256 × 256, en orden vista × 20 + realización. Se conserva la fracción 0,05, sin cambiar orientación o interpolar píxeles. Las figuras son resúmenes descriptivos; la regla del caso desfavorable fue definida para esta presentación posterior a la evaluación. Los hashes permiten verificar los archivos que produjeron esta versión. El archivo fuente C2 debe conservar sus bytes para reproducir su huella, aunque cambios de fin de línea no modifiquen los números.

La generación local se completó con comprobaciones de forma, rango y finitud, y ambas figuras se inspeccionaron visualmente. Se verificaron las cifras de las tablas contra C2 y los enlaces locales nuevos. No se volvió a entrenar ni a evaluar todas las redes. Una primera ejecución carecía de Matplotlib en su ruta de dependencias; se corrigió el entorno y la ejecución definitiva finalizó satisfactoriamente.

## Integración editorial

El texto puede distribuirse entre metodología y resultados según la estructura del informe oficial. Al trasladarlo a LaTeX deben asignarse etiquetas y usar referencias automáticas de ecuaciones, figuras y tablas. Deben conservarse la distinción entre épocas ejecutadas y checkpoint seleccionado, los doce contrastes entre métodos, la revisión C2 y la exposición histórica del catálogo. No reemplazar las cifras por los contrastes originales ni eliminar casos desfavorables.

La propuesta aprobada es `Plan_trabajo_grado.pdf`; la transcripción del objetivo procede de la revisión previa, con la limitación de acceso descrita en el informe. No se aplica la meta SSIM > 0,80 retirada de una versión anterior. La revisión editorial de los autores no exige una nueva campaña experimental.
