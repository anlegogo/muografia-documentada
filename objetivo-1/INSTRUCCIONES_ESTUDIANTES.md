# Primera entrega de los estudiantes — cierre técnico del OE1

**Encargo actual:** implementar y reportar la etapa 1 del [protocolo del segundo ensayo v1.0](PROTOCOLO_SEGUNDO_ENSAYO_OE1.md). Este archivo conserva las instrucciones de la primera entrega y su seguimiento histórico.

**Actualización del 29 de septiembre de 2026:** esta primera entrega ya fue recibida y [revisada con observaciones](REVISION_ENTREGA_2026-09-29.md). Conservar este documento como encargo histórico. El paso vigente es [diseñar el siguiente ensayo](DISENO_SIGUIENTE_ENSAYO_OE1.md); no repetir automáticamente el piloto ni ampliar la campaña.

**Propósito:** determinar el impacto de los defectos geométricos sobre la campaña sintética. Este encargo no incluye entrenamiento ni evaluación de redes. No repetir todavía la campaña completa.

## 1. Entorno y copia de trabajo

Trabajar en el supercomputador, sobre una copia separada del código recibido. Conservar la campaña y los shards originales. Registrar revisión Git, cambios sin confirmar si los hubiera, compilador, CMake, versión efectiva de Geant4, bibliotecas/datos de física, módulos cargados, lista de física FTFP_BERT, cortes, tratamiento de secundarios, tablas del generador y número de hilos. La campaña declara 11.4.2; el Docker recibido declara 11.3.2. Reproducir primero el entorno de campaña o documentar expresamente la diferencia.

No cambiar simultáneamente el generador, la física, el detector y la geometría: impediría identificar la causa de las diferencias.

## 2. Decisión geométrica y corrección

Leer el [diagnóstico](DIAGNOSTICO_GEOMETRIAS.md). Primer caso: **geo-train-06, vista 0**, evitando comenzar por la partición reservada de prueba. Hay una intersección conducto/cuerpo denso demostrada y un log histórico explícito.

Entregar una explicación física de qué material ocupa la intersección. El motor analítico asigna prioridad a la última anomalía del JSON y recorta al edificio; Geant4 coloca sólidos hermanos completos. Esa diferencia exige una decisión documentada, no simplemente mover anomalías hasta silenciar advertencias.

Una alternativa coherente con el campo analítico es construir cada anomalía como su intersección con el edificio, restándole las anomalías posteriores. Requiere revisar coordenadas locales, transformaciones y sólidos vacíos. Otra alternativa es un catálogo sin intersecciones, pero cambia el escenario físico y debe versionarse como tal. **No hay una corrección de transporte validada incluida en esta entrega.**

Conservar código/configuración A (recibida) y B (corregida), sus huellas y el diff. Mantener el mismo identificador en las salidas del ensayo y distinguir variantes por carpetas. Si el cambio exige otro identificador, adaptar el comparador explícitamente.

## 3. Control geométrico antes del transporte

La aplicación recibida no acepta archivos de macros ni un modo `--check-geometry`; no pasar opciones inexistentes. Añadir en la copia de trabajo un control explícito después de `Initialize()` y antes de `BeamOn()`, con salida que permita ejecutar solo el control:

```cpp
// Esquema que debe integrarse y compilarse en la copia derivada.
// Requiere #include "G4PhysicalVolumeStore.hh" y la cabecera del volumen.
bool overlaps = false;
for (auto* pv : *G4PhysicalVolumeStore::GetInstance()) {
    if (pv->GetMotherLogical() != nullptr) {
        overlaps = pv->CheckOverlaps(100000, 0., true, 100) || overlaps;
    }
}
// En el modo de control: devolver error si overlaps, y salir sin BeamOn.
```

Registrar resolución, tolerancia, semilla y versión. Revisar **todos los volúmenes de las 19 geometrías** (y las seis vistas cuando cambia la colocación del detector). Conservar logs íntegros. Una comprobación aleatoria sin advertencias aumenta la evidencia, pero no es demostración matemática universal. No aumentar la tolerancia para ocultar defectos de metros. La corrida A puede conservar advertencias únicamente como diagnóstico del comportamiento histórico; no es una referencia física válida.

Fuente técnica: [control de solapamientos de Geant4](https://geant4.web.cern.ch/documentation/dev/bfad_html/ForApplicationDevelopers/Detector/Geometry/geomOverlap.html).

## 4. Ensayo piloto acotado

Después de revisar y documentar B, ejecutar A y B sobre `geo-train-06`, vista 0, **1.000.000 de eventos por corrida**, con tres semillas: `2026092801`, `2026092802`, `2026092803`. Son parámetros propuestos para el piloto, no umbrales del plan aprobado ni garantía de potencia estadística.

Usar igual presupuesto, tablas, hilos y física por variante. Semillas iguales permiten organizar pares de corridas, pero no garantizan trayectorias idénticas después de cambiar navegación geométrica. Las semillas entre réplicas deben ser distintas; no promediar píxeles como si fueran volcanes independientes.

Se incluye [ejecutor SLURM](../herramientas/ejecutar_piloto_oe1.sbatch). Revisarlo y ajustar recursos/partición a las reglas vigentes de SC3; no enviará trabajos adicionales por sí mismo. Ejecuta una variante y tres réplicas en serie. `BIN`, `GEOMETRY`, `TABLES`, `OUTROOT` deben ser rutas absolutas a la copia derivada y a una carpeta de resultados nueva.

```bash
# Ejecutar desde la raíz de esta réplica después de cargar el entorno SC3.
# Sustituir las rutas de ejemplo y verificar el ejecutable antes de enviar.
sbatch --partition=PARTICION_AUTORIZADA --export=ALL,VARIANT=original,BIN=/ruta/A/muography_sim,GEOMETRY=/ruta/catalogo/geo-train-06.json,TABLES=/ruta/tablas,OUTROOT=/ruta/nueva/piloto-oe1 herramientas/ejecutar_piloto_oe1.sbatch
sbatch --partition=PARTICION_AUTORIZADA --export=ALL,VARIANT=corregida,BIN=/ruta/B/muography_sim,GEOMETRY=/ruta/catalogo-corregido/geo-train-06.json,TABLES=/ruta/tablas,OUTROOT=/ruta/nueva/piloto-oe1 herramientas/ejecutar_piloto_oe1.sbatch
```

Confirmar finalización de las seis corridas, conteos reales, ausencia de salidas truncadas y consistencia de metadatos. Si el tiempo asignado resulta insuficiente, registrar el fallo y ajustar recursos; no reutilizar carpetas parciales como resultados válidos.

## 5. Comparación y entrega

Con Python/NumPy, ejecutar desde la raíz de esta réplica:

```bash
python herramientas/comparar_piloto_oe1.py /ruta/nueva/piloto-oe1 --out /ruta/nueva/resumen-piloto.json
```

El comparador comprueba estructura y metadatos y calcula eficiencia global y diferencias por semilla, además de diferencias espaciales descriptivas. No establece equivalencia física ni un criterio automático de aceptación. Adjuntar mapas de conteos por evento, diferencias firmadas y regiones de interés definidas por la geometría **antes** de examinar diferencias. Para una valoración local sólida, aportar variación entre réplicas en esas regiones; los mapas por píxel pueden ser muy ruidosos a este presupuesto.

Rellenar la [plantilla de entrega](PLANTILLA_ENTREGA_OE1.md) con enlaces a código A/B, diff, logs, CSV, metadatos, resumen y SHA-256. Los binarios pesados van al almacenamiento compartido; los Markdown, configuraciones y manifiestos al repositorio acordado. Si no tienen acceso a este repositorio privado, entregar el paquete por su canal habitual para que el director lo incorpore. Estas instrucciones no conceden acceso nuevo.

## 6. Criterio de revisión y siguiente fase

- La corrección tiene una interpretación física explícita y controles geométricos documentados.
- Se conoce exactamente qué cambió y qué se mantuvo constante.
- Las diferencias globales y locales se reportan con variabilidad entre réplicas; no basta decir «se ven iguales».
- Si la precisión del piloto no permite decidir, el resultado es inconcluso. Establecer con el director una tolerancia físicamente justificada y un presupuesto mayor **antes** de la siguiente corrida; ausencia de diferencia significativa no demuestra equivalencia.
- Incluir después un control sin defectos identificados (`geo-train-01`) y ampliar a las seis vistas y restantes geometrías afectadas. Si A/B cambia también ese control, investigar qué más cambió.
- Una diferencia relevante o un defecto geométrico no resuelto impide cerrar la validación. La decisión de regenerar datos y su alcance debe quedar documentada; una vista favorable no certifica toda la campaña.

Esta primera entrega aborda P-01/P-02. P-03/P-04 continúan abiertos para completar insumos históricos y controles físicos de flujo/normalización.
