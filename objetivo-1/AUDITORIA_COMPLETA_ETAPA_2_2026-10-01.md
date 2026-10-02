# Auditoría completa de los archivos de etapa 2

**1 de octubre de 2026, Colombia. Estado: auditoría de crudos completada, sin fallos en los controles de integridad, correspondencia y conteo aplicados.** Se mantiene el resultado físico/estadístico **inconcluso**. Esta auditoría amplía la [revisión del agregado](REVISION_ETAPA_2_2026-10-01.md), que dejó expresamente pendiente la lectura íntegra de archivos grandes.

Entrega congelada: `f88de14`, rama `oe1/segundo-ensayo-etapa-2`. Código de estudiantes: `d8ca749`. Se preservan la entrega y los datos originales. No se ejecutó Geant4 ni se solicitaron nuevas corridas.

## 1. Descarga e integridad

Se recuperaron los **85 archivos previstos, 6.685.463.186 bytes comprimidos** (6,69 GB decimales) de la carpeta compartida de Drive. Las 85 huellas SHA-256 coinciden con `datos-compartidos/SHA256SUMS.txt` de la entrega. [Evidencia de descarga](evidencias/integridad-descargas-etapa2.json).

Los enlaces temporales de parte de las descargas caducaron. Se conservaron los archivos correctos, se usaron los enlaces compartidos y se renovaron los enlaces autenticados restantes. No se aceptó ningún archivo por su nombre/tamaño solamente: todos se verificaron por SHA-256. Los errores de descarga no implicaron discrepancias del contenido científico.

Las **27 listas de primarios y los 55 registros por muón** se descomprimieron completos y sus hashes se contrastaron con las listas congeladas y los manifiestos de cada corrida. Los **737 archivos** de los tres paquetes auxiliares coinciden con la entrega Git; se normalizó LF/CRLF únicamente en archivos `.status` de texto convertidos al extraer en Windows. [Contraste de paquetes](evidencias/contraste-paquetes-etapa2.json).

La copia local completa está en `tmp/datos-etapa2-drive` y la copia descomprimida/auditada en `tmp/auditoria-crudos-etapa2-director`, relativas al directorio superior a este repositorio. Los gigabytes científicos no se incorporan a Git. La preservación de esta entrega queda verificada en Drive y en la copia local; el esquema de almacenamiento para producción futura sigue necesitando definición.

## 2. Comprobaciones independientes

El [auditor de crudos](../herramientas/auditar_crudos_etapa2.py) recorre los archivos en bloques de 100.000 filas. Se verificaron **24,3 millones de primarios distintos**, 24 millones de pares principales, 300.000 pares de control y la repetición técnica de 100.000 registros A/A: **48,7 millones de transportes** respaldados.

- Identificadores completos y ordenados, especie/carga, valores finitos, energía positiva y dirección unitaria de los primarios.
- Huella FNV de cada primario recalculada desde la lista; SHA de lista, caso, réplica y variante en cada registro; correspondencia del estado aleatorio inicial A/B y unicidad por corrida.
- Estados finales válidos, ausencia de ABORTED, consistencia entre detección y estado; índices y pertenencia a ROI recalculados.
- Histogramas reconstruidos desde los registros completos, incluidos los no detectados en el denominador. Coincidencia de las 65.536 celdas por corrida y del mapa agregado.
- Conteos de transiciones por bloque, cruces y cambios de píxel contrastados con los publicados.
- Asignación del material de B en todos los cruces, a tolerancia de 1 µm.
- Comparación exacta de **todas las columnas**, salvo `variant`, para distinguir el detector de discordancias parciales del informe y la igualdad completa de registros.
- Tres bloques A/B de control idénticos en todas las columnas científicas; repetición A/A idéntica byte a byte después de descompresión. La verificación byte a byte respalda también las 100.000 filas de esa repetición.

**Resultado: 6.966 controles satisfactorios, cero fallidos.** [Evidencia completa](evidencias/auditoria-crudos-etapa2-f88de14.json). Se añaden 605 verificaciones de metadatos contra el manifiesto y los insumos congelados: N, semillas, caso/réplica, binarios, máscara, catálogos, tablas y un worker. [Configuración](evidencias/contraste-configuracion-etapa2.json). Esta comprobación de procedencia no es una nueva medición del entorno de SC3.

## 3. Resultado principal confirmado

| Magnitud | Desde los registros completos |
|---|---:|
| Pares principales | 24.000.000 |
| n00 / n01 / n10 / n11 | 23.999.929 / 4 / 1 / 66 |
| Detecciones ROI A / B | 67 / 70 |
| Delta por millón | +0,125 |
| IC95 % conservador, por millón | [−0,229200; +0,469439] |
| Margen prefijado, por millón | ±0,273660 |
| Categoría | Inconcluso |
| Detecciones totales A / B | 18.053.098 / 18.053.099 |
| Cambios de píxel entre detectados en ambas | 10 |
| Cruces en A y B | 151 en cada una; mismos 151 IDs |

Se mantienen el criterio y el tamaño prefijados. No se encontró una discrepancia que cambie el resultado principal. No se demuestra equivalencia dentro del margen ni una diferencia relevante fuera de él. No procede ampliar N automáticamente.

## 4. Qué añade la comparación completa

El informe original cuenta **50 discordancias** comparando seis campos: detección, estado, índices, ROI y estado aleatorio final. Ese conteo se reproduce. Al comparar todas las columnas aparecen **56 pares distintos**, que se separan así:

| Grupo | Pares | Interpretación |
|---|---:|---|
| Entran desde conducto y cruzan Z | 51 | Los 51 cambian en algún campo; 50 cumplen la definición restringida de discordancia |
| Cruzan Z desde cuerpo denso | 100 | Idénticos A/B en todas las columnas salvo variante |
| No registran cruce de Z | 5 | Cambian coordenadas/longitud y, en uno, desplazamiento lateral máximo; no detección, píxel, ROI, estado final ni rng1 |

Por tanto, se confirma E2-01: el ID 212035/r120 no era físicamente idéntico. También se amplía la precisión del informe: «no hay discordancias fuera de Z» es cierto para los seis campos seleccionados, **no para todo el registro**.

### E2-04: cinco diferencias fuera de los cruces registrados

| Réplica / ID | Estado final, igual A/B | Distancia entre puntos finales A/B |
|---|---|---:|
| 102 / 690169 | DECAY | 0,0102 mm |
| 106 / 211011 | DECAY | 0,0140 mm |
| 117 / 123395 | MU_CAPTURE | 8,2413 mm |
| 118 / 423452 | DECAY | 0,00327 mm |
| 120 / 986396 | MU_CAPTURE | 7,1922 mm |

[Valores originales y diferencias por campo](evidencias/diferencias-fuera-Z-etapa2.json). Son muones no detectados en ambas variantes. Cambian las coordenadas finales y `lc_m`; en r118 cambia también `max_lat_mm`. No debe atribuirse automáticamente todo a redondeo, porque dos desplazamientos son milimétricos. La causa concreta no se deduce del registro agregado. Se solicita una explicación basada primero en el código/navegación y estos IDs, sin ampliar la muestra ni lanzar una campaña de trazas indiscriminada. No se observó efecto en conteos para estos cinco casos.

### E2-02: energías y significado de “salida”

Se mantiene la corrección del análisis de las 51 entradas desde conducto: 43 valores `e_out` menores en B, siete mayores y uno igual; al comparar `(e_in−e_out)B−(e_in−e_out)A`, 45 diferencias positivas y seis negativas, usando 10⁻⁹ GeV de tolerancia.

Además, el código `EventAction.cc` asigna `e_out` al final interpolado del último tramo de paso dentro de Z. **No certifica que el muón haya salido físicamente de Z.** Por ejemplo, r119/ID 43210 termina MU_CAPTURE en ambas variantes y registra `e_out=0` en ambas. Conviene escribir «energía al final del último tramo registrado en Z», separando casos que terminan dentro, y conservar los límites de interpolación por cuerda. Las diferencias de energía no alteran por sí mismas el conteo de detección.

## 5. Decisión de seguimiento

La auditoría íntegra de esta entrega queda completada. Ya no está pendiente descargar/verificar los archivos grandes ni reconstruir sus conteos. Se resuelve la duda de preservación de datos de E2-03 para esta entrega, conservando la desviación operativa documentada respecto al almacenamiento inicialmente solicitado.

Quedan precisiones interpretativas E2-01/E2-02/E2-04 para reflejar en el informe de estudiantes; no se repite el ensayo por estas correcciones de redacción/análisis. La reproducción confirma el resultado **inconcluso**, que es una salida válida del diseño.

**Próximo paso: preparar producción con B**, no tratar de demostrar equivalencia de A a cualquier coste. Antes de lanzar: fijar entorno y scripts (P-02/P-03), justificar fuente/área/normalización (P-04), comprobar alcance de geometrías corregidas incluidas las de recorte e intersecciones múltiples, y acordar qué referencias y reducciones se regeneran. Las seis geometrías afectadas por seis vistas son un alcance candidato de 36 referencias; conservar las otras 78 exige compatibilidad documentada. Esta auditoría no inicia la producción ni cierra OE1/P-01…P-04.

## 6. Reproducción

Python 3.12 con numpy, pandas y scipy del entorno local de auditoría. Descargar los 85 archivos de la entrega `f88de14` y verificar su manifiesto. La máscara es la congelada en etapa 1, SHA `e76dcbe5926f9f4aeb61c556729d15c64124cd50a8577dca6beee9ffa317c5fd`.

```text
python herramientas/auditar_crudos_etapa2.py ENTREGA DATOS_GZ ROI SALIDA_NUEVA
python herramientas/detallar_diferencias_etapa2.py SALIDA_NUEVA
```

`SALIDA_NUEVA` debe no existir; requiere espacio para listas y registros descomprimidos. El primer script escribe `auditoria-completa.json`, histogramas reconstruidos en memoria, detalle de cambios y progreso. El segundo obtiene los valores de los cambios fuera de Z. La lista de detalles se limita a 5.000 casos, aunque los conteos siempre recorren todos; en esta entrega hay solo 56, por lo que no se truncó ningún caso.

El código analiza registros ya producidos: no valida automáticamente el modelo físico, la normalización temporal o todas las vistas del catálogo. Mantener separadas verificación de datos, resultado estadístico y alcance científico.
