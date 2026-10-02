# Publicación verificada de bloques — 2026-10-02

Complemento operativo al [balance de preparación local](BALANCE_PREPARACION_LOCAL.md). Se preparó [publicar_bloque_angular.py](../herramientas/publicar_bloque_angular.py) para publicar **archivos ya generados**, después de validar su copia. No ejecuta Geant4, no envía trabajos y no cambia la definición física del conjunto.

## Qué evita

Un bloque no debe considerarse publicado por el solo hecho de que el simulador devolvió cero. También deben funcionar la escritura, la copia, las huellas y la publicación final. El script estudiantil requiere adoptar esta comprobación; su versión en SC3 no se modifica automáticamente.

La herramienta:

1. Selecciona una fila inequívoca del manifiesto y valida el bloque con el mismo control estricto de la fusión.
2. Registra las huellas de **todos** los archivos del bloque, incluidos logs y comandos; exige archivos regulares, sin enlaces ni subdirectorios.
3. Adquiere un bloqueo exclusivo por destino. Un segundo publicador que respete este protocolo no puede publicarlo simultáneamente.
4. Copia a un directorio temporal único dentro del sistema de archivos de destino. Comprueba de nuevo los archivos, el origen y el bloque copiado.
5. Escribe un recibo `publicacion-verificada.json` y solo después cambia el nombre del directorio al destino final.
6. Si ya existe un bloque idéntico, validado y con el mismo manifiesto/recibo, devuelve `already_verified`. Si difiere o está incompleto, falla y lo conserva sin sobrescribir.

Los fallos se propagan como salida no satisfactoria. No se borran los archivos de entrada. Los temporales de un intento fallido se conservan para diagnóstico y no son bloques publicados. No deben incluirse manualmente como entradas de fusión.

## Verificación local realizada

**78 pruebas satisfactorias**, nueve nuevas de publicación. Se comprobaron: éxito, repetición idéntica, bloqueo ocupado, origen fallido, destino alterado, raíces anidadas y fallos deliberados de copia, corrupción de copia, escritura del recibo y cambio de nombre. [Registro](evidencias/pruebas-publicacion-verificada.txt) y [huellas](evidencias/validacion-publicacion-verificada.json).

Además, se publicaron en una carpeta local nueva los dos bloques reales de la entrega `f9a77ef` (filas 108 y 109), con la opción explícita para comprobar CRLF→LF:

- Todos los archivos publicados coinciden byte por byte con los recibidos; las entradas permanecen conservadas.
- El validador reconoce ambos bloques como `verified`.
- Repetir la fila 108 devuelve `already_verified`.
- Son los mismos 200.000 primarios ya simulados: **no se generaron datos nuevos ni se sometieron trabajos a SC3**.

[Evidencia del contraste real](evidencias/publicacion-verificada-f9a77ef.json).

## Uso y adopción

Requiere el entorno Python 3.12 y NumPy ya documentado. Mantener juntas las herramientas de nuestra réplica: la publicación importa el validador, lector y contrato de configuración.

Desde la raíz de la réplica:

```console
python herramientas/publicar_bloque_angular.py --manifiesto ENTREGA/datos/sc3/prueba-integracion/manifiesto-prueba.csv --fila 108 --origen ENTREGA/datos/sc3/prueba-integracion/oe1-v1-prueba --destino PUBLICADOS_NUEVOS --aceptar-crlf
python herramientas/publicar_bloque_angular.py --manifiesto ENTREGA/datos/sc3/prueba-integracion/manifiesto-prueba.csv --fila 109 --origen ENTREGA/datos/sc3/prueba-integracion/oe1-v1-prueba --destino PUBLICADOS_NUEVOS --aceptar-crlf
```

El origen y destino son raíces separadas: debajo se espera `geometría/viewN/blockNNNN/`. Los bloques temporales futuros del script SC3 deberán respetar ese diseño antes de llamar a la herramienta. Omitir `--aceptar-crlf` cuando los bytes conservan exactamente sus huellas SC3.

Al integrar en el script de trabajo, llamar al publicador **solo después** de finalizar correctamente simulación, selección del histograma, actualización de metadatos y generación de huellas. Propagar su código de salida; si falla, no imprimir «publicado», no marcar éxito y no reenviar automáticamente el mismo intento sin revisar la causa. El lanzador también debe usar la verificación de integridad antes de omitir un bloque.

Primero comprobar la integración con las pruebas y archivos existentes. No hace falta ejecutar otra simulación para verificar que un fallo de copia se propaga. Las pruebas locales no certifican el comportamiento del sistema de archivos compartido o del planificador de SC3.

## Límites operativos

La promoción usa un cambio de nombre dentro del mismo sistema de archivos y un bloqueo cooperativo. No garantiza durabilidad ante una pérdida eléctrica ni protege contra un proceso externo que ignore el protocolo y modifique los archivos. No se probó en el almacenamiento de SC3.

Una terminación abrupta puede dejar un archivo `.publication.lock`; la herramienta no lo elimina automáticamente por antigüedad. Antes de retirarlo hay que comprobar que el proceso propietario terminó y revisar temporales/destino. Un directorio temporal, aunque contenga un recibo, no equivale al directorio final publicado.

La adopción del flujo remoto, el tratamiento de fallos del lanzador y las decisiones físicas siguen pendientes. Esta mejora resuelve una pieza local de la operación; no habilita la campaña final.
