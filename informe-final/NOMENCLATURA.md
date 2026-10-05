# Nomenclatura y convenciones

| Símbolo o término | Definición | Unidad o cautela |
|---|---|---|
| g, v, k, p | Geometría, vista, realización y píxel | Unidades de análisis distintas |
| c_p | Conteo de referencia finita | Número de eventos, no densidad |
| f | Fracción retenida | 0,01; 0,05; 0,10; 0,50 |
| n_{f,k,p} | Conteo reducido condicionado a c_p | Binomial(c_p,f) |
| x = n/f | Entrada en cuentas equivalentes a referencia | No es el conteo reducido sin escalar |
| T, s | Transformación acotada y escala de entrenamiento | s = 8,239329427901795, logaritmo natural |
| u, y, z | Entrada T(x), objetivo T(c), salida del generador | Adimensionales; 0 ≤ z < 1 |
| ĉ | Predicción tras T inversa | Cuentas equivalentes |
| G, D | Generador y puntuación media del crítico | D promedia parches por muestra |
| P, B | Píxeles por imagen y tamaño de lote | B no es la etiqueta de semilla B1–B3 |
| R_b | Región de borde de una muestra | No confundir con factor de reducción R |
| Q | Indicador agregado de sesgo regional | Fracción en CSV; porcentaje = 100 Q |
| A, B en métricas locales | Anomalía y fondo de control | B aquí no es tamaño de lote |
| μ_A, μ_B | Medias espaciales de cuentas | Fondo con ponderaciones C2 |
| s_A, s_B | Desviaciones espaciales | ddof = 1; fondo con donantes únicos |
| C_N | μ_A/μ_B − 1 | Contraste de cuentas, adimensional |
| SNR_A, CNR_{A,B} | Cocientes definidos en capítulo 3 | No probabilidad de detección |
| ρ, X | Densidad y opacidad integrada | g/cm³ y g/cm² |
| L, ℓ | Longitud total y longitud en anomalía | Metros en cálculo nominal; conversión explícita |
| f_min | Mínimo aceptado de la rejilla | No determinado si conjunto vacío |
| R | 0,50/f_min | Factor del benchmark; no demostrado en este estudio |
| T_conv | Etiqueta de exposición convencional | No duración física calibrada |

Los decimales en texto usan coma; los CSV y las expresiones de código mantienen punto. SSIM es adimensional y PSNR se expresa en dB para rango uno en T. Los nombres de modelos y particiones se conservan cuando identifican registros: entrada, unet_original, cgan_original, B1_C0 a B3_C1, test y generalization.

C0/C1 se interpretan dentro de E1: C0 incluye la pérdida regional y C1 añade borde. No se trasladan automáticamente a otros ensayos históricos. C2 identifica la corrección del registro de controles, no una tercera variante de entrenamiento.

Las ecuaciones (3.1)–(3.5) tienen etiquetas propias de esta integración. Las demás expresiones de entrenamiento se presentan sin número. Las tablas 4.1–4.3 y 5.1, y figuras 4.1–4.6, se introducen antes de aparecer.
