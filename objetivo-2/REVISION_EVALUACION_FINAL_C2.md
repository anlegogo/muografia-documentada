# Revisión final y corrección de contraste EF-01-C2

2026-10-04, Colombia. Se audita la entrega estudiantil `4e5945eefea1f799a4e2adee8858d98d604cf4ba`, rama `oe2/evaluacion-final-f05`. Se integra su contenido original sin modificarlo. La revisión C2 es posterior a la apertura de las reservas y debe citarse como corrección numérica, no como protocolo prospectivo. No se modifican pesos, predicciones, particiones ni criterios de aceptación física.

## 1. Integridad y reproducción

Se descargaron los 83 archivos de la [distribución de Drive](https://drive.google.com/drive/folders/1UfRJTnuwYfgql5SJdklM2Cp-P0ychaAA). Las 32 matrices suman 1.006.637.056 bytes y coinciden con SHA-256, tamaños y recibos; sus valores son finitos, float32, con forma 120 × 256 × 256 y rango válido. Los 48 JSON y los dos manifiestos coinciden byte a byte con los objetos Git. Se verificaron los ocho archivos reservados y los ocho pesos contra el contrato EF-01.

La evaluación se recalculó en CPU sobre 3.840 predicciones y 480 entradas: las 4.320 filas de SSIM/PSNR coincidieron exactamente, y las 1.134 filas regionales hasta 4,44 × 10⁻¹⁶. Además, cuatro imágenes de geo-test-01 por cada red se infirieron nuevamente con los pesos originales: diferencia máxima CPU/GPU 4,85 × 10⁻⁶. Esta comprobación de inferencia es una muestra; la reevaluación de métricas sí cubre todas las predicciones.

[Auditoría](evidencias/ef01-c2/auditoria.json) · [integridad de matrices](evidencias/ef01-c2/integridad.json) · [muestra de inferencia](evidencias/ef01-c2/inferencia-muestra.json).

## 2. Hallazgo y corrección

La reevaluación original en Windows difirió de la entrega Linux en cuatro contrastes: conducto y cavidad de geo-test-01 y geo-test-03, vista 4. En la última cavidad incluso cambió el signo del contraste de referencia. Las longitudes de algunos candidatos eran prácticamente iguales; ordenar por sus diferencias sin tolerancia podía cambiar el quinto donante por redondeos mínimos. Se demostró esa sensibilidad perturbando únicamente longitudes geométricas, sin usar resultados de redes para escoger controles. No se atribuye toda la diferencia a una biblioteca específica sin haberla aislado.

La revisión C2 establece:

1. Se conserva la elegibilidad original: misma elevación, roca sin anomalía y diferencia relativa de longitud no mayor de 0,05; cinco controles por píxel.
2. Se ordenan diferencias absolutas de longitud. Se forma cada grupo desde su mínimo, incluyendo diferencias a no más de **10⁻⁸ m** del ancla, sin encadenar empates transitivos. Dentro del grupo se desempata por columna ascendente. No se cambia el umbral físico del 5 % ni se introducen promedios sobre un número diferente de controles.
3. La tolerancia resuelve diferencias próximas a la precisión numérica; no representa resolución espacial física. Se fijó antes de leer las métricas corregidas y se aplicó a todos los escenarios, anomalías y métodos. No se eligió para mejorar un modelo.
4. Se guardan los índices exactos, huellas de máscaras, identidad del corrector y protocolo. La reproducción usa esos índices en lugar de seleccionar otra vez los donantes. Si las máscaras no coinciden, se detiene explícitamente.

Se conservó intacto el código congelado EF-01. El [corrector independiente](herramientas/controles_contraste_v2.py) sustituye temporalmente la selección solo durante la evaluación y registra la revisión en su salida. [Registro completo de controles](evidencias/ef01-c2/controles.json).

## 3. Validación y efecto

Pasaron cuatro [pruebas específicas](herramientas/test_controles_contraste_v2.py): orden de empates próximos, distancias separadas/elegibilidad, reproducción y rechazo de índices alterados, y rechazo de soporte cambiado. Los 54 conjuntos de controles pasaron 162 comprobaciones: tolerancias 10⁻⁹ y 10⁻⁷ m y perturbación aleatoria determinista de ±10⁻¹⁰ m. Todas conservaron exactamente los índices de C2. Estas pruebas acotan la sensibilidad en el catálogo; no son una garantía matemática universal ni una prueba de ejecución en todos los sistemas operativos.

Una segunda evaluación completa usando el registro guardado reprodujo exactamente el informe y el registro, byte a byte. El registro explícito permite evitar una nueva decisión numérica de donantes en otros entornos, sujeto a coincidencia de máscaras y datos.

La aplicación uniforme modifica **ocho** contrastes de referencia frente a la entrega, incluidos casos sin discrepancia previa entre entornos. No se limita la corrección a los cuatro casos detectados. Se conservan 54 registros, 48 estimables y soporte común de 30 en test y 16 en generalización. SSIM, PSNR y regiones no cambian. [Comparación antes/después y comprobaciones](evidencias/ef01-c2/comparacion.json) · [resultados corregidos](evidencias/ef01-c2/resultados.json).

| Partición | Modelo | Contraste original | Contraste C2 |
|---|---|---:|---:|
| test | entrada | 0.336628 | 0.337054 |
| test | unet_original | 0.093172 | 0.092463 |
| test | cgan_original | 0.135066 | 0.135104 |
| test | B1_C0 | 0.132899 | 0.133285 |
| test | B1_C1 | 0.100570 | 0.102743 |
| test | B2_C0 | 0.112721 | 0.112458 |
| test | B2_C1 | 0.108925 | 0.109112 |
| test | B3_C0 | 0.116936 | 0.116575 |
| test | B3_C1 | 0.127687 | 0.127915 |
| generalization | entrada | 0.271327 | 0.289711 |
| generalization | unet_original | 0.072958 | 0.071503 |
| generalization | cgan_original | 0.088471 | 0.086302 |
| generalization | B1_C0 | 0.101319 | 0.105524 |
| generalization | B1_C1 | 0.137584 | 0.090703 |
| generalization | B2_C0 | 0.113495 | 0.114919 |
| generalization | B2_C1 | 0.099638 | 0.096729 |
| generalization | B3_C0 | 0.076043 | 0.073659 |
| generalization | B3_C1 | 0.077899 | 0.077246 |


Los valores de contraste son errores absolutos adimensionales. **Cambio de interpretación puntual:** en B1, generalización, C1 pasa de mayor error de contraste que C0 (0,1376 frente a 0,1013, aproximadamente) a menor error (0,090703 frente a 0,105524). Debe usarse la tabla exacta anterior para citar cifras. Las doce clasificaciones globales siguen siendo `tradeoff_or_deterioration`; ninguna pasa a aceptación física. La frase “nueve comparaciones” del informe original se corrige aquí: son seis por partición y doce en total. Los originales no se reescriben.

## 4. Estado y alcance

| Identificador | Estado | Evidencia y criterio |
|---|---|---|
| EF-02 | verificado | Ocho redes, cuatro geometrías, 32 matrices íntegras; muestra de inferencia consistente. |
| EF-03 | verificado con revisión C2 | Métricas recalculadas y contraste reproducido desde índices registrados; comparación original conservada. |
| EF-C2 | verificado | Cuatro pruebas, 162 comprobaciones de sensibilidad y reproducción completa exacta. |
| EF-04 | parcial | Síntesis académica preparada; requiere incorporación al manuscrito y aceptación del alcance por la dirección. |
| OE2-P04 | parcial en alcance científico | Implementación, entrenamiento y evaluación al 5 % verificados; no se acredita equivalencia física con alta estadística ni las otras fracciones. |

Se considera terminada la revisión técnica de esta entrega al 5 %. Un cierre técnico no acredita automáticamente la frase amplia “calidad comparable”. Los resultados permiten una conclusión descriptiva completa, incluidas limitaciones, sin encadenar entrenamientos hasta obtener una comparación favorable. No se requiere otra corrida de estudiantes para resolver C2.

La [síntesis para el manuscrito y transición al siguiente objetivo](SINTESIS_OE2_TRANSICION_OE3.md) distingue lo demostrado de lo pendiente. La exposición histórica declarada en [procedencia de reservas](entregas/2026-10-04-evaluacion-final-f05/PROCEDENCIA_RESERVAS.md) impide presentar esta evaluación como confirmación independiente.

## 5. Reproducción opcional, sin nueva GPU

Se usa Python con NumPy 2.3.5, PyTorch 2.6.0, scikit-image 0.26.0 y dependencias del evaluador original. El entorno local fue Windows, Python 3.12.14, PyTorch CPU; los detalles de la reevaluación están en el JSON corregido. Se reutilizan los datos y pesos de EF-01 y las predicciones de Drive. Desde la raíz del repositorio:

```bash
python objetivo-2/herramientas/test_controles_contraste_v2.py
python objetivo-2/herramientas/controles_contraste_v2.py \
  --repo . --data /ruta/insumos --weights /ruta/pesos-evaluacion.json \
  --predictions /ruta/oe2-evaluacion-final-f05 --report /ruta/nueva/revision-c2 \
  --registry-in objetivo-2/evidencias/ef01-c2/controles.json
```

Sin `--registry-in` se genera el registro determinista y se ejecutan los sondeos geométricos. El directorio de informe debe ser nuevo. Es una vía de reproducción, no una nueva tarea obligatoria para los estudiantes. Se conservan fuentes y finales de línea exigidos por el contrato. No se sobrescriben resultados anteriores.
