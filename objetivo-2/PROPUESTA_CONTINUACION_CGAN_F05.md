# Propuesta de continuación controlada de cGAN al 5 %

**Actualización 2026-10-04:** CG-01/02 y la ejecución/evaluación CG-03 ya están [verificados](REVISION_BINARIOS_CG04C.md). La [valoración posterior](VALORACION_COMPROMISO_CGAN_F05.md) mantiene límites físicos y fija una repetición condicionada, aún pendiente de integración. Los estados de preparación siguientes se conservan como antecedente histórico.

Fecha: 2026-10-03, Colombia. **Estado vigente: diseño implementado y recuperación exacta verificada en CPU. La comprobación GPU y el ensayo completo siguen pendientes.** La [guía operativa](INSTRUCCIONES_CONTINUACION_CGAN_F05.md) fija los comandos y condiciones de avance; se conservan a continuación la motivación y los parámetros del diseño.

## Motivo

La [revisión independiente del ajuste U-Net](REVISION_AJUSTE_A6AA6B8.md) confirma un compromiso: menor sesgo regional, con deterioro de borde y PSNR frente a la continuación de control. La región del cuerpo denso sigue teniendo un sesgo elevado. El resultado no justifica promover la penalización como solución general.

El OE2 nombra explícitamente una cGAN. Por ello, el siguiente experimento propuesto examina si el efecto del término regional se conserva al continuar la cGAN corregida. Es una hipótesis exploratoria; no se presupone que la componente adversaria resuelva los sesgos. Se evita una búsqueda simultánea de coeficientes, arquitecturas y fracciones.

## Pregunta y contraste

¿Añadir la misma penalización regional a la continuación de la cGAN reduce el sesgo de cuentas frente a una continuación cGAN sin esa penalización, sin deteriorar las otras medidas fijadas?

Se proponen dos ramas, C0 y C1. Ambas parten del mismo checkpoint cGAN de época 5, incluidos generador y crítico. Se comprobó que la copia recibida contiene ambos estados, con SHA-256 e54d51f758a9dcb88d65ba74369907f8d09f071d5085814d01ca2aa2958a57e0. No se sustituye el crítico por uno aleatorio ni se parte de los pesos U-Net ajustados.

| Elemento | C0 | C1 |
|---|---|---|
| Generador y crítico | unet_dc_5 y patch_critic_70 del checkpoint cGAN inicial | Iguales |
| Pérdida de G | 100 L1 + adversaria corregida | 100 L1 + adversaria corregida + Lreg |
| Pérdida del crítico | La cWGAN-GP corregida, GP del promedio por muestra, coeficiente 10 | Igual |
| Optimizadores | Adam nuevos para G y D; lr=0,00001; betas=(0; 0,9) | Iguales |
| Actualizaciones por lote | Cinco del crítico y una del generador, como en el piloto | Iguales |
| Datos | 1.440 train / 360 val; fracción 0,05; contrato y normalización v1 | Iguales |
| Máscaras | Reglas del ajuste U-Net; solo participan en entrenamiento/evaluación | Iguales |
| Semilla propuesta | 2026100303 | Igual |
| Lote / aumentos / AMP / recorte | 4 / desactivados / desactivado / desactivado | Iguales |
| Presupuesto | Cinco épocas adicionales, sin parada temprana | Igual |
| Selección | Quinta época adicional | Igual |

La reducción de la tasa de aprendizaje conserva la proporción de tasas G/D del piloto. Es una decisión propuesta para una continuación breve, no evidencia de optimalidad. Reiniciar optimizadores debe hacerse de forma idéntica en las dos ramas. Las máscaras no se añaden a la entrada del generador durante inferencia.

La U-Net inicial, U-Net A/B y la cGAN inicial permanecen como referencias identificadas. Comparar las continuaciones cGAN con U-Net es informativo, pero no aísla por sí solo el efecto adversario: heredan entrenamientos previos diferentes. El contraste controlado del nuevo experimento es C1 frente a C0.

## Evaluación y límites

Mantener Q, Q por geometría, error de cuentas de cielo/borde, contraste sobre las 23 combinaciones comunes, SSIM y PSNR, sin cambiar umbrales para aceptar resultados ya vistos. La misma regla descriptiva del ajuste U-Net permite comparar la dirección del cambio dentro de cGAN.

Añadir obligatoriamente una tabla por anomalía y vista frente a C0 y al checkpoint cGAN inicial. Mostrar sesgo firmado, su magnitud y error absoluto espacial, con soporte en píxeles y cuentas de referencia. Una mejora de Q no basta para declarar fidelidad física si oculta un deterioro de una anomalía. Esta tabla es una salvaguarda de interpretación, no un cambio retrospectivo de la clasificación U-Net.

Se conserva la distinción entre error de cuentas sumadas en una región y suma de errores absolutos por píxel. Los porcentajes promediados por anomalía no equivalen al porcentaje de la unión de anomalías ponderada por sus cuentas.

No se abren test/generalization. La validación ya utilizada es exploratoria; el ensayo no se presenta como confirmación independiente ni estima variabilidad entre entrenamientos.

## Preparación necesaria antes de delegar ejecución

- **CG-01 — Verificado en CPU:** se implementó el ejecutor descrito en la [guía y evidencia](INSTRUCCIONES_CONTINUACION_CGAN_F05.md). Requisito satisfecho: implementar el ejecutor específico conservando pesos del crítico, identidades, estados de ambos optimizadores y todos los RNG. Añadir el término regional solo a la pérdida del generador. No reutilizar ejecutar_ajuste.py cambiando únicamente el nombre del checkpoint: ese ejecutor entrena U-Net sin crítico.
- **CG-02 — Parcial, CPU verificado/GPU pendiente:** diecinueve controles y cuatro ejecuciones completas acreditan pérdida, separación y recuperación exacta en CPU. Se conserva el requisito: verificar en CPU control de coeficiente cero, gradientes, cinco pasos D/uno G, separación de actualizaciones, selección fija y recuperación exacta de G, D y ambos optimizadores. Después repetir la batería técnica en GPU.
- **CG-03 — Preparado para ejecución condicionada; resultados pendientes:** configuraciones y comandos publicados. Tras aceptar la comprobación GPU y medir recursos, ejecutar las dos continuaciones. Cualquier modificación del diseño se versionará antes de correr.

La batería técnica propuesta conserva ocho pares train/val y dos épocas, con ejecución continua y recuperada por rama: 16 actualizaciones de G y 80 de D. El ensayo completo suma 3.600 actualizaciones de G y 18.000 de D entre ambas ramas. Se requiere una GPU por proceso; pueden ejecutarse secuencialmente. Los tiempos de U-Net no estiman el costo de cGAN con GP.

No se requieren nuevas simulaciones ni una campaña de 24 entrenamientos para preparar este contraste. La integración y las pruebas locales ya están verificadas. El siguiente trabajo corresponde a la prueba técnica GPU y, si se acepta y hay recursos disponibles, a las dos continuaciones conforme a la guía.
