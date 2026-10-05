# 5. Discusión y conclusiones

## 5.1. Calidad de imagen y conservación de cuentas

Los resultados muestran una separación entre similitud de imagen y conservación de cantidades relevantes para la interpretación muográfica. U-Net y cGAN producen imágenes al 5 % con mayor SSIM y PSNR que la entrada escalada. Sin embargo, el incremento de Q evidencia que esa mejora puede acompañarse de sesgo en los promedios regionales. Por tanto, la afirmación de calidad comparable debe especificar métrica, fracción y referente.

Esta coexistencia es coherente con la transformación empleada. T comprime el intervalo de conteos y su inversa es no lineal. Una diferencia pequeña en T no corresponde a un error uniforme en cuentas. A su vez, la entrada n/f tiene esperanza condicional c bajo el adelgazamiento binomial, sin que ello garantice precisión de cada realización o equivalencia con la intensidad física verdadera. La referencia contiene ruido y no constituye una verdad instrumental libre de incertidumbre.

El control U-Net supera a la cGAN original en SSIM/PSNR en ambas particiones. En consecuencia, la evaluación no permite atribuir a la componente adversaria una superioridad general. Su utilidad debe juzgarse junto con sesgo regional, error espacial y contraste, conservando las variantes desfavorables.

## 5.2. Qué aportaron las continuaciones

Las continuaciones con pérdidas regionales y de borde redujeron parte de las discrepancias de las redes originales. La reducción del error espacial en las comparaciones C1/C0 no eliminó todos los compromisos. El experimento no produjo una mejora uniforme de todos los indicadores.

B1–B3 son continuaciones pareadas desde pesos comunes; no equivalen a tres campañas independientes de entrenamiento desde cero. Tampoco corresponde escoger retrospectivamente la semilla con mejor desempeño y presentar su cifra como resultado predeclarado. El informe conserva las seis variantes y sus comparaciones.

Los controles de recuperación del entrenamiento y de integridad fueron necesarios para descartar diferencias técnicas en la ejecución. Su éxito no implica que la función de pérdida garantice conservación física, ni que un resultado científico desfavorable deba tratarse como fallo de software.

## 5.3. Anomalías: alcance de la mejora

El error absoluto de contraste disminuye con cGAN al 5 %, pero aumentan la frecuencia descriptiva de inversiones de signo y el error de CNR. Estas observaciones muestran que acercarse en promedio al valor de un indicador no garantiza conservar todos sus aspectos. No se interpreta la mejora de SNR espacial como probabilidad de detección: la dispersión puede disminuir por suavizado, incluida la atenuación de estructura real.

El signo se compara con una referencia de estadística finita y puede ser sensible cuando el contraste de esa referencia está próximo a cero. Esta limitación se declara, sin eliminar después los casos desfavorables mediante un umbral elegido sobre los resultados. El soporte común y las exclusiones por denominadores nulos se mantienen iguales entre los métodos comparados.

Las regiones y controles se derivan de geometrías conocidas. En un uso experimental con un volcán real no se dispondría necesariamente de esa información. Por ello, estas métricas son herramientas de evaluación del estudio sintético y no un procedimiento validado de localización de anomalías desconocidas.

## 5.4. Reducción de exposición y resultado negativo

El complemento responde una pregunta acotada: si los pesos existentes, aplicados a cuatro fracciones, alcanzan simultáneamente SSIM y PSNR de la entrada al 50 % en todas las vistas. La respuesta fue negativa. No se identificó un mínimo aceptado de la rejilla ni un factor asociado.

La razón 2:1 entre entrada al 10 % y cGAN al 5 % sigue siendo una comparación descriptiva favorable de similitud. No es contradictorio que esa comparación resulte favorable y el benchmark al 50 % no se alcance: los referentes son diferentes. Tampoco puede reemplazarse el resultado por 20×, obtenido simplemente de 1/0,05; ese cociente ignora la calidad de salida.

Los modelos fueron entrenados al 5 %. La evaluación de otras fracciones estudia transferencia, y el deterioro al 50 % no demuestra que una estrategia de entrenamiento multifracción sea inviable. Afirmar lo contrario excedería el experimento. El estudio tampoco demuestra que cualquier arquitectura futura carezca de reducción útil.

El benchmark se fijó antes de las nuevas inferencias, pero después de resultados históricos. Esta secuencia no se presenta como validación confirmatoria independiente. El informe conserva esa limitación y no reajusta retrospectivamente los umbrales para declarar éxito.

## 5.5. Opacidad y alcance del modelo sintético

El conjunto representa conteos direccionales de primarios bajo una fuente y un transporte idealizados. Su exposición convencional no equivale a tiempo físico calibrado. La ausencia de una campaña de campo no incumple por sí misma el diseño computacional aprobado; sin embargo, limita la extrapolación a un instrumento.

La metodología de la propuesta incluye contraste de opacidad. El contraste de cuentas empleado es un indicador sustituto, y la opacidad calculada desde el catálogo es una referencia nominal. Ninguno demuestra que las imágenes mejoradas recuperen cuantitativamente X. Una inversión exigiría una relación de respuesta apropiada y su validación; aplicar una fórmula de atenuación arbitraria o ajustar sobre las mismas reservas no resolvería esa exigencia.

La discrepancia potencial entre densidad nominal y sustitución por G4_AIR en una anomalía restringe la interpretación de seis filas del diagnóstico. No se utiliza para explicar causalmente el resultado negativo de los modelos ni para invalidar automáticamente la campaña completa. Se conserva como límite de la trazabilidad de materiales efectiva en ese análisis.

## 5.6. Balance de los objetivos

La Tabla 5.1 diferencia productos concluidos de afirmaciones parcialmente respaldadas.

**Tabla 5.1.** Balance de cumplimiento basado en la evidencia conservada.

| Objetivo | Resultado sustentado | Alcance de la conclusión |
|---|---|---|
| OE1 | 19 geometrías, 114 referencias y 9.120 pares generados y verificados. | Cumplido y cerrado bajo el alcance idealizado adoptado; sin equivalencia instrumental. |
| OE2 | Diseño, implementación, entrenamiento y evaluación de cGAN, control U-Net y continuaciones. Mejora de SSIM/PSNR respecto de entradas de baja estadística. | Calidad comparable respaldada parcialmente; sesgos y deterioros impiden afirmar equivalencia física general con alta estadística. |
| OE3 | Evaluación multifracción y local terminada; benchmark aplicado y factor no demostrado. | Cierre experimental con cumplimiento científico parcial; opacidad no reconstruida cuantitativamente. |

El cierre experimental evita repetir pruebas sin una nueva pregunta. No transforma una hipótesis favorable en un resultado demostrado ni sustituye la evaluación académica de la tesis.

## 5.7. Conclusiones

1. Se obtuvo un conjunto reproducible de imágenes muográficas sintéticas con distintas estadísticas de conteo. El producto conserva trazabilidad, particiones por geometría y siete excepciones a la meta descriptiva de roca, sin excluirlas para mejorar el balance.
2. Las redes incrementaron la similitud de imagen al 5 % frente a la entrada. U-Net superó a cGAN original en SSIM/PSNR bajo las configuraciones evaluadas. Esa mejora coexistió con sesgos regionales mayores que los de la entrada escalada.
3. Las pérdidas regionales y espaciales redujeron parte de los errores, con compromisos entre indicadores. No se obtuvo evidencia de conservación uniforme de cuentas y anomalías.
4. Ningún modelo alcanzó el benchmark conjunto frente a la entrada al 50 % en las fracciones estudiadas. No se demostró un factor de reducción bajo esa regla; el resultado no equivale a un factor nulo ni a imposibilidad universal.
5. El contraste de cuentas y la opacidad nominal permitieron delimitar la interpretación, pero no acreditaron reconstrucción cuantitativa de opacidad. La conclusión física amplia de calidad comparable permanece parcial.

## 5.8. Trabajo futuro y cierre editorial

Un estudio posterior podría evaluar entrenamiento multifracción, pérdidas acordes con el modelo de conteo y una calibración/inversión de opacidad. Debería fijar antes de evaluar nuevos casos sus criterios de aceptación y conservar una reserva independiente. Estas líneas son propuestas futuras, no resultados ni encargos actuales de cómputo.

La presente integración reúne metodología, resultados, discusión y conclusiones. La adaptación a la plantilla institucional, el marco teórico con bibliografía completa y la revisión y presentación por los autores son etapas editoriales distintas. No se afirma que el documento de Overleaf haya sido actualizado ni que la tesis esté aprobada.
