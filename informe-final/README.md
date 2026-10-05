# Informe integrado de metodología, resultados y conclusiones

**Versión institucional vigente:** [proyecto LaTeX corregido](latex/README.md), [PDF compilado](latex/main.pdf) y [ZIP para Overleaf](latex/Trabajo_de_Grado_Muografia_corregido.zip). Los archivos Markdown de esta carpeta se conservan como antecedente. El [registro editorial](latex/LEEME_CORRECCIONES_FINALES.txt) describe los cambios y la validación.

Versión: 2026-10-04, Colombia. Integración editorial sobre la revisión experimental cerrada. Se preservan las fuentes originales, los resultados desfavorables y la atribución a los estudiantes de sus ejecuciones. No se han realizado nuevas simulaciones, entrenamientos ni inferencias para redactar estos capítulos.

## Resumen

Se construyó un conjunto sintético de 114 referencias muográficas y 9.120 pares en diecinueve escenarios idealizados. Se implementó y evaluó una cGAN, junto con un control U-Net y seis continuaciones. Las redes mejoraron SSIM y PSNR respecto de entradas al 5 %, con compromisos en conservación regional y métricas de anomalías. La evaluación de pesos existentes al 1 %, 5 %, 10 % y 50 % no encontró una fracción que alcanzara simultáneamente los umbrales del referente sin red al 50 %. Por tanto, no se demostró un factor de reducción bajo ese benchmark. El contraste de cuentas y la opacidad nominal no constituyen una inversión validada de opacidad. El cierre experimental conserva cumplimiento científico parcial de las afirmaciones amplias de OE2/OE3.

## Lectura del informe

1. [Metodología](03_METODOLOGIA.md): conjunto, formación de pares, modelos, pérdidas, entrenamiento y criterios.
2. [Resultados](04_RESULTADOS.md): tres tablas numéricas generadas de la síntesis auditada y seis figuras existentes integradas con interpretación.
3. [Discusión y conclusiones](05_DISCUSION_CONCLUSIONES.md): balance de los tres objetivos, límites y trabajo futuro.
4. [Nomenclatura](NOMENCLATURA.md): símbolos, unidades y convenciones.
5. [Revisión de coherencia](REVISION_COHERENCIA.md): propuesta, evidencia y decisiones editoriales.

La integración contiene el núcleo experimental del informe final. No sustituye portada, introducción, marco teórico, bibliografía institucional ni presentación de autores; no acredita modificación del documento remoto de Overleaf. La propuesta aprobada conserva los objetivos: [lectura y transcripción verificadas](../docs/REVISION_PROPUESTA_APROBADA.md).

Las fuentes y las figuras se enlazan dentro del mismo repositorio, sin duplicar binarios ni cambiar datos. Las fórmulas se muestran en Markdown matemático y pueden trasladarse a la plantilla LaTeX conservando sus definiciones. Las referencias numéricas corresponden a esta integración.

## Fuentes documentales

- [Ficha y receta del conjunto](../objetivo-1/FICHA_CONJUNTO_OE1.md) y [cierre OE1](../objetivo-1/CIERRE_OE1.md).
- [Síntesis OE2](../objetivo-2/manuscrito/INFORME_OE2.md), [tablas C2](../objetivo-2/manuscrito/TABLAS_OE2.md) y [evaluación final](../objetivo-2/REVISION_EVALUACION_FINAL_C2.md).
- [Protocolo OE3-C1](../objetivo-3/PROTOCOLO_COMPLEMENTO_OE3.md), [auditoría](../objetivo-3/REVISION_COMPLEMENTO_OE3_C1.md) y [cierre](../objetivo-3/CIERRE_OE3.md).
- [Opacidad nominal y límites](../objetivo-3/OPACIDAD_NOMINAL_Y_ALCANCE.md).

Los antecedentes bibliográficos deben citarse desde la bibliografía comprobada del manuscrito institucional. Esta integración se fundamenta en las evidencias internas; no añade citas externas sin revisión ni atribuye a artículos fórmulas operativas definidas por el protocolo.
