# Licencias y preparación de publicación

Revisión: 2026-10-26 (Colombia). Base revisada: `e92caea12136d88e648efe98cbac638544eae3eb`.

## Autorización y alcance

La dirección confirmó en esta fecha que se cuenta con autorización de Reinaldo Cárdenas Tirado y Daniel Andrés Pinto Ortega para las licencias propuestas y que no existen restricciones institucionales conocidas. Esta confirmación permite preparar la asignación de licencias; no constituye una verificación jurídica independiente de la titularidad de cada elemento.

El alcance operativo se encuentra en [LICENSE.md](../LICENSE.md). Se preservan las bitácoras, entregas originales, resultados, pesos y archivos históricos. Las observaciones antiguas de procedencia que indicaban ausencia de licencia describen el estado anterior a esta revisión.

## Distribuciones externas cubiertas para material propio

| Distribución | Identificación | Licencia del material propio |
|---|---|---|
| Datos OE1 | https://drive.google.com/drive/folders/10gRmkWqmCqN3qOf2gfOWCDG4bcC7zhaT | CC BY 4.0 para datos; Apache-2.0 para código propio independiente, si se incluye. |
| Pesos originales U-Net/cGAN | https://drive.google.com/drive/folders/18pOGXzN2lEhKfxJlpcC4GuTujkNyA-ix | Apache-2.0 para pesos propios; CC BY 4.0 para informes. |
| Continuaciones E1 B1/B2/B3, C0/C1 | https://drive.google.com/drive/folders/1cuOFqrq8BbWTDSpdIegLpPK5jmLz3TMF | Apache-2.0 para pesos propios; CC BY 4.0 para matrices y resultados. |
| Evaluación final f05 | https://drive.google.com/drive/folders/1UfRJTnuwYfgql5SJdklM2Cp-P0ychaAA | CC BY 4.0 para predicciones y resultados. |
| Complemento multifracción | https://drive.google.com/drive/folders/12RB9qJ32WjUWGFBQRxuvIiZ7szTM9IbO | CC BY 4.0 para predicciones y resultados. |

La asignación se refiere a los artefactos del proyecto identificados por sus índices y manifiestos, no a futuras adiciones arbitrarias a las carpetas. Los permisos de descarga de Drive son independientes de la licencia de reutilización. No se han modificado esos permisos ni se han añadido avisos dentro de Drive en esta revisión.

## Verificación y pendientes

| ID | Estado | Evidencia y criterio de cierre |
|---|---|---|
| PUB-L1 | Confirmado por la dirección | Autorización de autores y ausencia de restricciones institucionales conocidas, según declaración recibida el 2026-10-26. |
| PUB-L2 | Revisado | Textos de GPL v3, Apache-2.0, CC BY 4.0 y MIT; alcance por materiales y avisos de terceros revisados en la propuesta #3. |
| PUB-L3 | Pendiente | Identificar versión/huella y modificaciones de EcoMug realmente usadas en UIS; el Makefile original utiliza una rama mutable. No impide conservar la licencia ya declarada por la copia archivada, pero limita la reproducción exacta. |
| PUB-L4 | Parcial | El código de entrenamiento revisado no mostró llamadas a descarga de pesos preentrenados externos. Confirmar la procedencia completa de los ocho checkpoints antes de presentarla como auditada. |
| PUB-D1 | Parcial | Se listaron anónimamente las cinco carpetas y se descargó un archivo pequeño de verificación/manifiesto por carpeta. No se descargaron ni verificaron íntegramente todos los datos y pesos. |
| PUB-D2 | Pendiente | Acompañar las distribuciones de Drive de los avisos y textos aplicables, sin reemplazar binarios ni cambiar sus hashes. |
| PUB-R1 | Revisado con alcance explícito | Se completaron los controles documentados en [revisión previa a publicación](REVISION_PUBLICACION.md): historial y cambios remotos, contenedores ZIP/NPZ, PDF, procedencia y datos identificativos. No se identificaron credenciales ni impedimentos concretos en el alcance examinado; no constituye certificación exhaustiva. |

La publicación puede comunicar limitaciones de reproducción pendientes; no debe presentar verificaciones parciales como completas. La licencia de datos y pesos no implica validación física, mejora general de calidad ni demostración de un factor de reducción de adquisición.

## Procedencia de los textos

Se conservaron los textos sin reescribir sus condiciones:

- https://www.gnu.org/licenses/gpl-3.0.txt
- https://www.apache.org/licenses/LICENSE-2.0.txt
- https://creativecommons.org/licenses/by/4.0/legalcode.txt
- https://raw.githubusercontent.com/nlohmann/json/v3.11.3/LICENSE.MIT

Las copias están en [LICENSES/](../LICENSES/). Los términos de terceros ya vigentes no dependen de la aprobación de una licencia nueva para el material propio.
