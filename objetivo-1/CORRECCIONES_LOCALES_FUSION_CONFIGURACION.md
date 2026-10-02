# Correcciones locales de fusión y configuración — 2026-10-02

Se atienden los pendientes técnicos T-01/T-02/T-03 de la [revisión de la entrega f9a77ef](REVISION_FISICA_PRODUCCION_2026-10-02.md). No se cambia su rama ni la física del simulador. La alternativa nueva está en `herramientas/` de nuestra réplica, disponible para que los estudiantes la adopten. Su lanzador y sus scripts en SC3 no se actualizan automáticamente.

## Resultado comprobado

**56 pruebas satisfactorias**: las 41 anteriores, cuatro pruebas nuevas de compatibilidad y once de fusión. [Registro](evidencias/pruebas-correccion-fusion-configuracion.txt) y [versiones/huellas](evidencias/validacion-correccion-fusion-configuracion.json).

Con los dos bloques reales de integración de geo-train-06/vista 0:

| Magnitud | Resultado |
|---|---:|
| Primarios transportados | 200.000 |
| Registros con corte de 3 GeV | 69.995, matriz idéntica a la entregada |
| Registros de todas las energías | **130.190**, corrige el metadato anterior de 65.050 |
| Media de energía, todas las energías | 17,8362621 GeV, ponderada por conteos de ambos bloques |
| Tiempo de pared sumado / primarios | 0,00002328428884 s/evento |

La media energética del subconjunto con corte no se puede recuperar de estos histogramas. Se elimina el campo ambiguo heredado y se registra `mean_ekin_all_energies_gev`; no se presenta esa media como la del subconjunto. El tiempo sumado de bloques no representa el tiempo transcurrido de una campaña con trabajos paralelos.

La imagen fusionada se exportó y pasó el lector actualizado de empaquetado. **No se creó un paquete real de seis vistas**, porque la entrega de integración solo contiene una. [Evidencia de la ejecución real](evidencias/correccion-fusion-f9a77ef.json).

## T-01: huellas y finales de línea

El comportamiento predeterminado de [fusionar_bloques_angular.py](../herramientas/fusionar_bloques_angular.py) exige coincidencia exacta con `salida.sha256`. Los archivos recibidos que cambiaron de LF a CRLF fallan en ese modo, como debe ocurrir.

Para esta entrega se puede usar **explícitamente** `--aceptar-crlf`. Solo admite el archivo si reemplazar CRLF por LF reproduce exactamente el SHA-256 declarado. Una alteración de los conteos sigue fallando. El informe registra la huella de los bytes recibidos, la esperada y si fue necesaria esa comprobación. Las entradas no se modifican; los nuevos CSV y metadatos se escriben con LF en un directorio nuevo.

Se añadió una regla `-text` para `objetivo-1/entregas/**/datos/sc3/**` en `.gitattributes`, para conservar los bytes de futuras incorporaciones. **No repara los commits antiguos ni restaura archivos que ya habían sido convertidos antes de incorporarlos.** Los estudiantes deben conservar los archivos originales de SC3 y sus manifiestos; si distribuyen versiones convertidas, documentar ambas huellas.

## T-02: fusión estricta

La nueva herramienta valida el lote antes de crear la salida:

- Manifiesto no vacío, columnas e identidades válidas; filas, bloques y semillas sin duplicados. Política actual: semillas distintas en todo el manifiesto.
- Código de salida cero; huellas obligatorias de matriz y metadatos; comparación de geometría, vista, semilla y eventos con el manifiesto.
- Matrices de 256×256 con enteros no negativos, coherentes con sus conteos y sin desbordamiento uint32.
- Mismos insumos por ruta y huella, configuración y número de hilos entre bloques y vistas de una geometría. No sustituye la comprobación externa de los binarios/tablas declarados.
- Sumas de eventos, generación, conteos con/sin corte y tiempos; media energética ponderada cuando todos los bloques la proporcionan.
- Relectura de la salida y manifiesto de procedencia por bloque.

Solo admite bloques de N fijo (`exposure_days=-1`), como los de esta entrega. No deduce días físicos ni suma exposiciones sin una definición acordada. El alcance es el manifiesto recibido: no garantiza por sí solo que incluya todas las vistas de una campaña. Esa completitud se revisa después con el empaquetador.

No sobrescribe salidas. Una interrupción de disco durante la escritura puede dejar un directorio parcial; solo considerar completa una salida con `revision-fusion.json` final.

## T-03: configuración del paquete

[configuracion_angular.py](../herramientas/configuracion_angular.py) define un contrato compartido con el empaquetador. La firma ahora incluye **todas las opciones de `oe1_controles`**, `reference_histogram` y las definiciones explícitas `source_definition` y `normalization` cuando estén presentes. Cambiar inyección, margen, plano, corte o definición de referencia ya no deja una firma idéntica.

Una configuración controlada exige `oe1_controles` válido y `reference_histogram` no vacío. No se mezcla con imágenes sin esos campos. Las referencias anteriores que carecen de ambos siguen siendo legibles como configuración anterior; no se les inventa una receta. Las definiciones de fuente y normalización, si se añaden, deben ser objetos JSON no vacíos; se comparan completas, pero **su contenido físico requiere revisión**. Su ausencia no se interpreta como aprobación física. Se rechazan valores no finitos.

El contrato del informe incorpora `configuration_contract=explicit-recipe-v2`; permanece `physical_validation=false`. Las realizaciones de conteo y su esquema de semillas no cambian.

## Instrucciones para adoptar las correcciones

Desde la raíz de nuestra réplica actualizada, con el entorno Python documentado:

```console
python -m unittest discover -s herramientas -p "test_*angular*.py" -v
python herramientas/fusionar_bloques_angular.py --manifiesto ENTREGA/datos/sc3/prueba-integracion/manifiesto-prueba.csv --salida ENTREGA/datos/sc3/prueba-integracion/oe1-v1-prueba --destino FUSION_NUEVA --aceptar-crlf
python herramientas/preparar_imagen_angular_v1.py FUSION_NUEVA/geo-train-06/geo-train-06_view0_hist.csv --salida IMAGENES_NUEVAS
```

`ENTREGA` representa la carpeta de la entrega f9a77ef descargada de su rama. `FUSION_NUEVA` e `IMAGENES_NUEVAS` deben ser carpetas nuevas. Omitir `--aceptar-crlf` para archivos que conservan las huellas exactas de SC3. No alterar manifiestos para hacer pasar un rechazo.

Para un lote futuro de seis vistas, exportarlas juntas en una única llamada al exportador (seis rutas de histogramas). Después ejecutar el empaquetador con la geometría correspondiente. No copiar la vista actual seis veces ni atribuir a esas copias una simulación nueva.

**Entrega técnica que pueden realizar sin nuevas simulaciones:** aplicar estas herramientas a los dos bloques existentes, guardar el informe de fusión y el de exportación, comprobar 200.000 / 69.995 / 130.190 y documentar la versión utilizada. Conservar sus archivos de SC3. Revisar además la propagación de errores del lanzador/publicación, que no fue reemplazado en este cambio.

## Pendientes físicos que permanecen

F-01/F-02/F-03 siguen abiertos: definición de la imagen y su relación con el detector, normalización y evaluación de bordes para el observable elegido. Las correcciones técnicas no demuestran equivalencia física ni autorizan P0/P1. No se requiere repetir los controles de SC3 por estos cambios de procesamiento.
