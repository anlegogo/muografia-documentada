# Verificación de la copia de distribución en Drive (P-05)

2026-10-03, Colombia. Se verificó la copia de distribución del conjunto OE1 publicada en la [carpeta de Drive `oe1-campana-114`](https://drive.google.com/drive/folders/10gRmkWqmCqN3qOf2gfOWCDG4bcC7zhaT), enlazada en la entrega estudiantil `f395570`. La referencia de comparación son los inventarios de la rama `oe1/justificacion-fisica-produccion` en `f395570`, ya verificados por la dirección en [REVISION_DATOS_F395570.md](https://github.com/anlegogo/muografia-documentada/blob/efeee44/objetivo-1/REVISION_DATOS_F395570.md).

Se realizaron dos comprobaciones: la recuperación de la carpeta desde el enlace con una cuenta distinta de la propietaria, y la lectura de la copia desde la cuenta propietaria. Ambas dieron el mismo resultado.

## Recuperación desde el enlace

La carpeta se descargó desde el enlace publicado con una segunda cuenta de Google, distinta de la propietaria, en una sesión del navegador separada. Drive entregó un único archivo `datos-oe1-campana-114-20261003T175814Z-1-001.zip` de 1.048 MB (SHA-256 `8eff236f2300e25b9142f00e5aa22995f47f75a9b7cd30eb167746111819a402`), que se descomprimió en una carpeta nueva.

| Componente | Referencia en la rama | Criterio | Resultado |
|---|---|---|---|
| Imágenes (114 NPZ, 114 metadatos, `revision-exportacion.json`) | `posproceso/imagenes.sha256` | Huella de archivo | **229/229 coinciden**; ninguno falta ni difiere |
| Fusión (114 histogramas, 114 metadatos, 19 `entradas.sha256`, `revision-fusion.json`) | `posproceso/fusion.sha256` | Huella de archivo | **248/248 coinciden**; ninguno falta ni difiere |
| Pares (114 archivos, 9.120 pares) | `huellas-contenido.json` | Huella de contenido de `counts_ref`, `low_counts` y `fractions` | **114/114 archivos; 342/342 arreglos coinciden** |
| Inventario completo | Copia subida | Número de archivos, bytes y huella de cada archivo | **753 archivos, 1.126.769.406 bytes; 753/753 idénticos** a la copia subida |

La descarga no contiene archivos ajenos al conjunto. Resultado detallado: [verificacion-descarga-p05.json](verificacion-descarga-p05.json).

## Lectura desde la cuenta propietaria

La misma verificación, aplicada a la copia leída desde la cuenta propietaria mediante Google Drive para escritorio, dio 229/229, 248/248 y 114/114 (342 arreglos). Resultado: [verificacion-drive-p05.json](verificacion-drive-p05.json). En esa vista aparecen además 25 archivos `desktop.ini`, que Windows y Drive para escritorio crean localmente en cada carpeta para mostrar su icono; no forman parte de la descarga desde el enlace ni del conjunto.

## Huellas de archivo de los pares

Las huellas de archivo de los pares no coinciden con `pares/manifest.json` de la rama (0/114), pero sí con el `manifest.json` de la propia copia (114/114). La copia procede de una regeneración en una segunda máquina con NumPy 2.4.4 y zlib 1.3.2; los originales se comprimieron con zlib 1.3.1. La compresión cambia los bytes del NPZ sin cambiar los arreglos, como prevé la [ficha del conjunto](https://github.com/anlegogo/muografia-documentada/blob/58f9c12/objetivo-1/FICHA_CONJUNTO_OE1.md). Por eso el criterio aplicable es la huella de contenido, que coincide en todos los casos.

La copia contiene además `dataset-v2/`, derivado para entrenamiento que queda fuera del OE1. Solo a título informativo: sus 19 shards coinciden en contenido con `huellas-contenido.json` (57 arreglos), y `splits.json` declara 5.760, 1.440, 1.440 y 480 pares por partición. No constituye una auditoría de la conversión.

El `LEEME.txt` de la copia registra commits, versiones, huellas de `pares/manifest.json` y `dataset-v2/splits.json` y la verificación de contenido de la regeneración.

## Alcance y limitaciones

- La recuperación se comprobó con una segunda cuenta de uno de los estudiantes. Esto demuestra que el enlace permite descargar la carpeta completa e íntegra fuera de la cuenta propietaria; no comprueba el acceso de cuentas concretas, como la de la dirección.
- No se modificaron los permisos de la carpeta para esta verificación.
- No se reejecutó la simulación ni se regeneraron los pares; se compararon los archivos de la copia con los inventarios existentes.

## Procedimiento reproducible

Entorno: Windows 11, Python 3.14.3 y NumPy 2.5.3 (zlib 1.3.1, implementación zlib-ng). La versión de NumPy no afecta este procedimiento, porque solo se leen y descomprimen arreglos ya generados; no se realiza muestreo binomial.

Para repetir la verificación, descargar la carpeta desde el enlace, descomprimirla en una carpeta nueva y ejecutar [verificar_drive_p05.py](verificar_drive_p05.py) con la carpeta descargada y una réplica de `muografia-documentada` en `f395570` o posterior:

```bash
python verificar_drive_p05.py verificacion-descarga-p05.json RUTA_DESCARGA/datos-oe1-campana-114 RUTA_REPLICA/muografia-documentada
```

La huella de contenido de cada arreglo concatena `dtype.str`, la representación de su forma y sus bytes contiguos en orden C, según la convención de `huellas-contenido.json`.

| Archivo | SHA-256 |
|---|---|
| `verificar_drive_p05.py` | `4a7459654048603d3f440c66bd14305515eb127b2445e0f5e0b584fbe2353d1e` |
| `verificacion-descarga-p05.json` | `d19e7e85a88376e84b6412276f2ddfb6a123e31e86c82b7f883d41260324c382` |
| `verificacion-drive-p05.json` | `604ac3ccc0f3bca197dddb2b6900f155a69f7d904288f0c3cfd7d181bab1f60b` |

Responsable de la verificación: Reinaldo Cárdenas Tirado.
