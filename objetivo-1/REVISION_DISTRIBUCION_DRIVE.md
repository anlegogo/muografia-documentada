# Revisión independiente de la distribución en Drive

2026-10-03, Colombia. Se recuperó íntegramente la [carpeta de distribución](https://drive.google.com/drive/folders/10gRmkWqmCqN3qOf2gfOWCDG4bcC7zhaT) mediante la conexión disponible para la revisión de la dirección. **P-05 queda resuelto para esta copia:** 753 archivos, 1.126.769.406 bytes y 2.291 controles satisfactorios. No se modificaron los datos, los permisos de Drive ni la rama estudiantil.

## Evidencia y comparación

La referencia congelada es `f395570`, ya revisada en [REVISION_DATOS_F395570.md](REVISION_DATOS_F395570.md). Durante esta revisión se recibió `cb57145`, que incorpora la documentación de la dirección y la [verificación de Reinaldo en 8fa667c](https://github.com/anlegogo/muografia-documentada/blob/8fa667c/objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion/verificacion-drive-p05/VERIFICACION_DRIVE_P05.md). Se comprobó la descarga de forma independiente; no se dio por verificada únicamente a partir de ese reporte.

| Componente | Comprobación independiente | Resultado |
|---|---|---|
| Fusión | Archivos contra `posproceso/fusion.sha256` de Git | 248/248 idénticos. |
| Imágenes | Archivos contra `posproceso/imagenes.sha256` de Git | 229/229 idénticos, incluidas las 114 referencias. |
| Pares | Contenido de referencias, conteos reducidos y fracciones contra `huellas-contenido.json` | 342/342 arreglos coincidentes en 114 paquetes que contienen 9.120 pares. |
| Inventario de pares | Huellas de los 114 NPZ y sus 114 metadatos contra el manifiesto de Drive; vínculo a las imágenes | Todos coinciden. |
| Coordenadas | Ejes y centros de los pares contra su imagen de origen | Coincidencia exacta de contenido y tipo. |
| Derivado `dataset-v2` | Integridad de 19 paquetes; 57 huellas de contenido; coordenadas, manifiesto y particiones | Coinciden. Es una comprobación de distribución, no una auditoría del conversor ni evaluación de redes. |
| Copia completa | Rutas y tamaños contra listado de Drive; inventario SHA-256 local | 753 archivos y 1.126.769.406 bytes, coincidentes con el total reportado por estudiantes. |

Las particiones conservan 5.760 / 1.440 / 1.440 / 480 pares por geometría para entrenamiento / validación / prueba / generalización. La comprobación de distribución no demuestra desempeño predictivo.

Los pares de Drive se regeneraron con NumPy 2.4.4 y zlib 1.3.2, según su LEEME; la entrega anterior empleó zlib 1.3.1. Las huellas de archivo comprimido pueden diferir sin modificar los arreglos. Se verificaron los bytes contra el manifiesto de la propia copia y, separadamente, el contenido numérico contra Git. El manifiesto de pares de Drive tiene SHA-256 `cce4444978b3650038f26e0f56b3a4960177531f24a160ee4a58fc31d124017b`.

## Procedimiento reproducible

Se descargaron archivos originales, sin conversiones, mediante la integración de Drive y referencias temporales de descarga. La copia local se conserva en `trabajo/drive-2026-10-03`, excluida de Git; no se publican enlaces temporales de autenticación. Entorno de comprobación: Windows, Python 3.12.14 y NumPy 2.4.4. No se realizó muestreo ni transporte para esta revisión.

Desde la raíz del repositorio, `REFERENCIA` debe apuntar a `datos/sc3/campana-114` extraído de `f395570` y `DESCARGA` a la carpeta recuperada de Drive:

```bash
python herramientas/verificar_distribucion_oe1.py \
  --descarga DESCARGA --referencia REFERENCIA \
  --inventario-remoto objetivo-1/evidencias/revision-drive-2026-10-03/inventario-remoto.json \
  --salida NUEVA_VERIFICACION.json
```

La salida debe ser nueva. El [verificador](../herramientas/verificar_distribucion_oe1.py) registra cada comparación y termina con código distinto de cero si encuentra discrepancias. Evidencia conservada: [inventario remoto](evidencias/revision-drive-2026-10-03/inventario-remoto.json) y [verificación completa con inventario SHA-256](evidencias/revision-drive-2026-10-03/verificacion.json).

Se comprobó también el rechazo de una huella esperada alterada en una copia temporal: el verificador detectó exactamente una discrepancia y terminó con código 1, sin modificar los datos. Se revisaron 173 enlaces locales, sin rutas rotas; [validación de la herramienta](evidencias/revision-drive-2026-10-03/validacion-herramienta.json).

Durante el desarrollo del verificador se corrigió una expectativa propia: los NPZ contienen cuatro arreglos de coordenadas además de los tres incluidos en las huellas publicadas. Los 133 avisos iniciales correspondían a esa expectativa, no a corrupción de los datos. La ejecución final comprueba también esas coordenadas y no presenta fallos. Tres lotes de descarga se repitieron tras corregir la resolución del directorio local; todos terminaron completos. No se alteraron los archivos de estudiantes.

## Alcance del cierre

La recuperación quedó demostrada con la conexión utilizada; no certifica acceso anónimo, permisos de cualquier cuenta ni permanencia indefinida del enlace. Tampoco acredita los 1.026 bloques crudos de SC3, que no forman parte de esta distribución. La revisión previa ya delimitó qué se verificó desde histogramas y registros.

**Actualización de cierre:** P-04 se resolvió posteriormente con el informe integrado y la decisión de la dirección; véase [CIERRE_OE1.md](CIERRE_OE1.md). El párrafo siguiente conserva el estado observado durante la revisión de distribución.

No se requiere otra campaña para resolver P-05. Sigue pendiente P-04: incorporación y valoración académica del manuscrito. La plantilla local tiene resultados y conclusiones vacíos, y no se identificó un manuscrito actualizado en `cb57145`; no puede declararse revisado un texto no recibido. La [síntesis](SINTESIS_RESULTADOS_OE1.md#integración-documental-y-cierre) contiene el material y la lista de incorporación que permiten avanzar sin más simulación por defecto.
