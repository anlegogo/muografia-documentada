# Propuesta: aceptación de la recuperación con tolerancia declarada

2026-10-03 (Colombia). Propuesta para la decisión de la dirección, derivada de la [incidencia](INCIDENCIA_RECUPERACION_GPU.md). **No está aplicada:** el código de `main` y esta rama conservan el criterio de recuperación exacta.

## Problema

`revisar_ajuste_cgan.py` exige igualdad bit a bit entre la ejecución técnica continua y la recuperada. En CUDA, la cGAN difiere tras reanudar hasta en 2,9e-5 en pesos y 1,6e-5 en predicciones, por redondeo dependiente del historial del proceso. La causa está documentada, pero no se pudo eliminar. Sin aceptación GPU, el ensayo C0/C1 no puede ejecutarse.

## Cambio propuesto

Modificar únicamente la comparación continua frente a recuperada de `audit_technical` en `revisar_ajuste_cgan.py`:

| Elemento | Criterio actual | Criterio propuesto |
|---|---|---|
| Estados de RNG, pasos de los optimizadores, orden de datos, índices, identidad, `resume_count` | Igualdad exacta | Igualdad exacta, sin cambios |
| Tensores de generador, crítico y momentos de Adam | Igualdad exacta | Diferencia absoluta máxima ≤ 1e-4 |
| Valores numéricos del historial (pérdidas y métricas) | Igualdad exacta | Diferencia relativa ≤ 1e-4 |
| Predicciones técnicas de validación | Igualdad exacta | Diferencia absoluta máxima ≤ 1e-4 |
| Huellas SHA-256 de generador y crítico en el historial | Igualdad exacta | Se excluyen, porque reflejan la misma diferencia de pesos ya acotada |
| Informe de aceptación | `exact_recovery: true` | `exact_recovery: false`, `recovery_within_tolerance: true`, tolerancias y diferencias máximas por rama |

Las tolerancias se fijan antes de ejecutar el ensayo y quedan unas 3 veces por encima de la máxima diferencia observada. Son cuatro órdenes de magnitud menores que los efectos que el ensayo compara: diferencias de Q de varios puntos porcentuales y de SSIM del orden de 1e-4 entre variantes.

Como `revisar_ajuste_cgan.py` forma parte de la huella de código del ejecutor, el cambio produce una identidad nueva. Habría que repetir la etapa técnica completa antes de las continuaciones. Ni el entrenamiento, ni las pérdidas, ni la evaluación, ni la regla de decisión cambian.

## Alcance e implicaciones

- La garantía que se pierde es que un ensayo interrumpido y reanudado sea bit a bit idéntico a uno continuo. Pasaría a ser idéntico dentro de esa tolerancia.
- Si las continuaciones de cinco épocas no se interrumpen, la reanudación no interviene en sus resultados.
- El cambio se registraría como desviación en la entrega, con las diferencias máximas medidas en la nueva prueba técnica.

## Alternativas

1. **Mantener el criterio exacto** y ejecutar C0/C1 en CPU, donde la recuperación exacta ya está verificada. El costo de tiempo no está medido y el ejecutor actual solo permite CPU en la etapa técnica.
2. **Investigar la causa a nivel de kernels CUDA.** El plazo es incierto y no está garantizado el resultado.
3. **Aplicar esta propuesta** y ejecutar en GPU en unos 15 minutos.
