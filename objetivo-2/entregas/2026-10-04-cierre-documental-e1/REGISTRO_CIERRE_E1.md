# Registro de la consolidación de E1

2026-10-04, Colombia. Entrega de las [instrucciones de cierre de E1](../../INSTRUCCIONES_CIERRE_E1.md). Rama `oe2/cierre-documental-e1`, creada desde `main` en `bd44272ef47b77442a027af09ddd3859d34005c8`. La entrega original [804ce85](https://github.com/anlegogo/muografia-documentada/tree/804ce85f1bcb1e00d0956ae6bef26e69dd50130a/objetivo-2/entregas/2026-10-04-borde-cgan-f05) se conserva sin cambios en su rama `oe2/borde-cgan-f05`; no se fusionó. No se entrenó, no se usó GPU y no se abrieron test ni generalización.

**Contenido:** [discusión del ensayo](DISCUSION_E1.md), reproducción del diagnóstico, reconocimiento de la fe de erratas y verificación del índice de artefactos.

## 1. Reproducción del diagnóstico interior

Se ejecutó en CPU [diagnosticar_interiores_e1.py](../../herramientas/diagnosticar_interiores_e1.py) con el comando de la revisión ([comando.txt](datos/comando.txt)).

| Elemento | Valor |
|---|---|
| Equipo | WSL2 Ubuntu en Windows 11, CPU; sin CUDA |
| Entorno | Python 3.12.15, NumPy 2.3.5, SciPy 1.18.1 y Matplotlib 3.11.1 ([entorno.txt](datos/entorno.txt)) |
| Script | SHA-256 `eff73ab9f1268914ed43f298e29efe4a4f7f47e5ef3cf548531109991d6f1ddc`, idéntico al registrado en la evidencia de la dirección |
| Datos | 30 shards train/val descargados de las copias de Drive y verificados contra el contrato v1: 30 de 30 huellas |
| Predicciones y máscaras | Las seis predicciones finales y la caché de máscaras de la entrega 804ce85, verificadas contra su manifiesto antes de la ejecución; el script comprueba de nuevo las seis huellas contra la auditoría |
| Duración | 13 s de cómputo ([diagnostico.log](datos/diagnostico.log)) |

**Resultado: reproducción concordante.**

- **Conteos:** 252 sesgos comprobados, 126 filas regionales y 378 filas por banda, los esperados.
- **Diferencias:** las tablas completas coinciden con [diagnostico-interiores-e1.json](../../evidencias/diagnostico-interiores-e1.json) y [bandas-interiores-e1.csv](../../evidencias/bandas-interiores-e1.csv). La diferencia absoluta máxima es 1,11×10⁻¹⁶, frente a la tolerancia de 10⁻¹², sin ninguna diferencia en campos no numéricos ([comparacion-reproduccion.json](datos/comparacion-reproduccion.json)).
- **Herramienta de comparación:** [comparar_diagnostico_e1.py](verificacion/comparar_diagnostico_e1.py).
- **Figuras:** se conservan las regeneradas en PNG ([datos/reproduccion/](datos/reproduccion/)). Según las instrucciones, no se exige igualdad binaria de imágenes entre versiones de Matplotlib.

## 2. Reconocimiento de la fe de erratas

Los autores de la entrega 804ce85 reconocen las dos correcciones de la [fe de erratas de la dirección](../../evidencias/fe-erratas-e1.json). Los originales y sus huellas se conservan sin modificar.

1. **Tamaño de los binarios.** El informe original declaró 5.952.730.120 bytes. Esa cifra es el `total_bytes` del inventario, que incluye también los archivos de texto. La suma de los 55 binarios es **5.910.537.694 bytes**, una diferencia de 42.192.426 bytes. No falta ningún binario; esta cifra coincide con la suma de `binarios.tamanos.txt` de la entrega.
2. **Rutas de siete registros.** Las consolas `B1/B2/B3-tecnica-consola.log`, `B1/B2/B3-piloto-consola.log` y `evaluacion-sintesis-consola.log` figuran en el inventario como `logs-locales/…`, pero en GitHub están en la raíz de `datos/ensayo-borde-e1/`. Sus bytes y SHA-256 coinciden.

La lectura corregida es la de la fe de erratas. Para trabajos posteriores, los totales de binarios se calcularán a partir de las entradas con `storage: drive` del inventario.

## 3. Índice de artefactos finales

Se revisó el [índice de artefactos finales](../../INDICE_ARTEFACTOS_E1.md) de la revisión `bd44272`, sin rehacer el inventario ni renombrar o sustituir binarios.

- **Huellas:** las seis parejas de pesos y predicciones del índice coinciden en ruta, tamaño y SHA-256 con `binarios.sha256` y `binarios.tamanos.txt` de la entrega.
- **Identificadores:** coinciden con los de la carpeta pública de Drive ([ids-drive-e1.json](datos/ids-drive-e1.json)).
- **Acceso:** los 12 enlaces se abrieron sin sesión iniciada. Cada uno devolvió el inicio del archivo binario esperado (contenedor ZIP para `last.pt` y cabecera NumPy para `predicciones-val.npy`), no una página de inicio de sesión ([acceso-enlaces-indice.json](datos/acceso-enlaces-indice.json), [verificar_enlaces_indice.py](verificacion/verificar_enlaces_indice.py)). Si el acceso es público, cualquier integrante del grupo puede abrirlos sin permisos adicionales.

## 4. Estado

| Punto de las instrucciones | Estado |
|---|---|
| 1. Rama nueva y commit base | `oe2/cierre-documental-e1` desde `bd44272`; 804ce85 conservada |
| 2. Reproducción CPU del diagnóstico | Concordante: 252/126/378, diferencia máxima 1,11×10⁻¹⁶ |
| 3. `DISCUSION_E1.md` | [Redactada](DISCUSION_E1.md): tres parejas, las 54 vistas (anexo), las 72 filas de anomalías y los límites |
| 4. Fe de erratas | Reconocida en la sección 2 |
| 5. Índice de artefactos | Coincidente y accesible sin sesión |
| 6. Publicación | Textos, JSON, CSV, figuras y registro de comparación en Git; pesos y predicciones en Drive |

Las huellas de esta entrega están en [huellas.sha256](huellas.sha256).
