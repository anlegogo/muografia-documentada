# Revisión local de la preparación de datos

## Qué se ejecutó

Se leyeron las 114 vistas crudas y los 19 shards entregados. Se regeneraron **en memoria los 9.120 pares** mediante la rama binomial y la derivación de semillas declaradas en `build_dataset.py`. No se sobrescribió ningún archivo recibido ni se realizó transporte Monte Carlo nuevo.

| Control | Resultado |
|---|---|
| Conteos de referencia de cada shard frente a sus seis vistas crudas | Coinciden. |
| Forma por shard | Referencia `(6,256,256)`; entradas `(6,4,20,256,256)`. |
| Tipos | Referencia `uint32`; entradas `uint16`. |
| Fracciones | 0,50 / 0,10 / 0,05 / 0,01. |
| Semillas de las 20 realizaciones por vista y fracción | Coinciden con los metadatos. |
| Submuestreo binomial regenerado | 9.120/9.120 pares coinciden elemento a elemento. |
| Conteos bajos superiores a su referencia | Ninguno. |
| Recorte por límite uint16 al regenerar | Ningún píxel por encima de 65.535. |

La implementación recibida contiene un recorte a 65.535 antes de guardar; el control de esta entrega muestra que no se activó en los pares reproducidos. El ensayo también comprueba el orden de geometrías utilizado en la derivación de semillas. Las verificaciones de hashes y particiones previas se conservan independientemente.

## Cómo repetir

Desde la raíz de la réplica, con Python y NumPy y los archivos pesados restaurados:

```powershell
python herramientas/auditar_oe1.py
```

Escribe [auditoria-oe1.json](evidencias/auditoria-oe1.json), que registra versiones, huella del script, resultados por geometría y límites. El registro corresponde al entorno de auditoría local; no acredita reproducibilidad universal entre versiones de bibliotecas.

## Qué no demuestra

- La reproducción de pares comprueba la transformación de los conteos recibidos; no prueba que esos conteos procedan de una geometría físicamente válida.
- Los 20 submuestreos de una vista comparten referencia y no son 20 escenarios independientes. La separación por geometría se conserva.
- El módulo original normaliza usando el máximo de la referencia; esto debe explicarse cuando se interpreten métricas de imágenes. Aquí no se evalúan redes.
- La exposición de referencia de 30 días se completa por defecto si falta en el metadato crudo; es una convención del constructor, no una medición independiente del tiempo equivalente.
- Siguen pendientes los supuestos de flujo y área de detección. La convergencia del tamaño del plano de conteo, por sí sola, no prueba una normalización física sin sesgo.

**Conclusión:** la preparación binomial de datos está reproducida para la entrega disponible. La validación del transporte y su interpretación física permanecen abiertas.
