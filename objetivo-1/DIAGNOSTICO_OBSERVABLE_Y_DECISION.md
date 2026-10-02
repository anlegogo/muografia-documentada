# Observable y bordes: avance local con los datos existentes

2026-10-02. Complemento a la [revisión física](REVISION_FISICA_PRODUCCION_2026-10-02.md), posterior a las [correcciones técnicas](CORRECCIONES_LOCALES_FUSION_CONFIGURACION.md). No se ejecutaron nuevas simulaciones. Datos de la entrega `f9a77eff49c01bfd073c00d7d62414e3ce962f9d`.

## Una comparación útil que ya estaba disponible

La corrida `c01-anidado-cono` registra simultáneamente cuadrados de distintos tamaños para los mismos 20 millones de primarios. Se analizaron los conteos con energía cinética superior a 3 GeV, geo-train-01, vista 0, inyección próxima al cono y sin margen angular.

| Columna de roca (10³ g/cm²) | Panel 1,2 m | Plano 100 m | Plano 600 m | Panel / 600 m | 100 / 600 m |
|---|---:|---:|---:|---:|---:|
| 10–30 | 1.920 | 2.725 | 2.726 | 70,43 % | 99,96 % |
| 30–60 | 191 | 1.705 | 1.707 | 11,19 % | 99,88 % |
| 60–100 | 238 | 1.610 | 1.620 | 14,69 % | 99,38 % |
| 100–200 | 250 | 1.703 | 1.721 | 14,53 % | 98,95 % |
| >200, hasta el límite 10⁷ g/cm² del análisis | 12 | 330 | 333 | 3,60 % | 99,10 % |

**Interpretación:** casi todos los muones que alcanzan el plano de 600 m también están dentro del de 100 m; eso no implica que estén dentro del panel de 1,2 m. En bandas intermedias solo entre el 11 % y el 15 % de esos registros quedan en el panel pequeño para esta fuente.

**Límite esencial:** la fuente sigue restringida a trayectorias dirigidas nominalmente al panel. Faltan los muones que podrían entrar desde otras posiciones de una fuente espacial amplia. Por ello, estos cocientes **no son eficiencias de un detector real**, no miden por sí solos el sesgo del estimador grande y no deben usarse para multiplicar/corregir imágenes. Tampoco demuestran que una compensación de entradas y salidas sea imposible; muestran que todavía debe justificarse. No extrapolar el resultado a otras geometrías/vistas o al margen de 5°.

Este resultado acota F-01 con datos Geant4 ya conservados: no es necesario repetir la comparación 100/600 para volver a demostrar contención. La pregunta pendiente es la equivalencia del observable.

## Bordes evaluados sobre la selección de energía

Se aplicó el mismo diagnóstico descriptivo de C4 a histogramas sin corte y con E_cin > 3 GeV: razón por columna entre llegadas y generaciones nominales en elevaciones de 30 a 42°, diferencia con columnas interiores, y extrapolación lineal a las cinco filas superiores. Se usó la máscara de cielo abierto del helper geométrico de los estudiantes, cuya huella se conserva.

| Corrida | Primarios | Margen | Máxima desviación sin corte | Con corte de 3 GeV |
|---|---:|---:|---:|---:|
| c01, cuadrados anidados; se selecciona el de 600 m | 20.000.000 | 0° | 4,19 pp | 1,64 pp |
| c02, plano de 600 m | 2.000.000 | 5° | 1,65 pp | 2,84 pp |

Los valores con corte superan descriptivamente el umbral de 1 pp de los estudiantes, pero **no constituyen una decisión estadística de aprobación/rechazo físico**. La extrapolación lineal no es una referencia física validada para el espectro cortado. Los tamaños de muestra son diferentes, no se calculó una comparación pareada y las llegadas pueden migrar de píxel. No usar `sqrt(p(1-p)/n)` como si cada razón de llegada/generación nominal fuera una eficiencia binomial; incluso puede haber entradas desde otros bins.

No se concluye que el margen de 5° empeore la imagen ni se selecciona otro margen con estos máximos. Sí se confirma que el 1,65 pp publicado para todos los muones no describe automáticamente la imagen de producción con corte.

## Decisión física preparada, aún no adoptada

Antes de fijar días de exposición o un tamaño de campaña, la ficha debe distinguir dos posibles productos:

| Definición | Lo que puede declararse | Evidencia adicional necesaria |
|---|---|---|
| Imagen de un estimador direccional sintético bajo una fuente y selección explícitas | Conteos del estimador, N transportado, geometría, malla, inyección, margen y E_cin > 3 GeV | Justificar su utilidad como dato de transmisión para OE1, sus límites y su sensibilidad a configuración. No llamarlo conteo calibrado del panel. |
| Imagen de cuentas de un detector físico de 1,2 m | Conteos esperados de ese panel y exposición física | Fuente espacial/energética adecuada o pesos demostrados; compensación de entradas/salidas, área proyectada y normalización consistentes. |

No se redefine aquí el objetivo ni se adopta unilateralmente la primera opción para evitar una validación. La dirección y los estudiantes deben explicitar qué alcance es coherente con el informe y OE1.

La normalización también puede adelantarse documentalmente: especificar superficie de fuente, energía total o cinética, densidad conjunta de energía/dirección, área normal o proyectada, selección en el detector y tratamiento del aire. La coincidencia de tasas integradas o la supervivencia casi completa cerca del panel no resuelve una diferencia de forma espectral.

**Propuesta provisional de etiquetado:** mientras no se cierre esa definición, conservar `exposure_days=-1` para los bloques N fijo. Si se informa k·30 días, identificarlo expresamente como escala convencional heredada; no escribirlo como duración física calibrada. No se cambia S0, no se elimina su umbral y no se aplica un factor nuevo en este avance.

## Qué debe demostrar un siguiente control, si resulta necesario

1. **Referencia común:** definir el observable de salida, el corte de 3 GeV, fuente, normalización y referencia contra la que se compara. No comparar el plano grande y pequeño bajo fuentes incompatibles y llamar a eso validación.
2. **Aceptación espacial:** si se pretende representar el panel físico, diseñar una comparación que incluya entradas desde fuera del panel nominal, o una demostración cuantitativa con tolerancia. Los cocientes de la tabla anterior no proporcionan ese control completo.
3. **Aceptación angular:** evaluar los bordes con la selección final y una expectativa apropiada; separar columnas azimutales de la variación física del espectro con elevación. Una referencia de margen mayor también necesita justificar sus pesos fuera de la tabla.
4. **Criterio previo:** si se mantiene la tolerancia de 1 pp, usar intervalos simultáneos para las filas/columnas declaradas, estimados con réplicas independientes o un modelo de covarianza justificado. Declarar equivalencia solo si los intervalos completos caben dentro de la tolerancia; si cruzan el límite, el resultado es inconcluso. No transformar un máximo observado pequeño en prueba de equivalencia.
5. **Presupuesto:** dimensionar N después de estimar la variabilidad para esa comparación. No deducirlo de la desviación binomial de razones con migración ni prescribir ahora otra campaña grande.

Los controles de integridad, la fusión y el empaquetado ya pueden usarse. La entrega siguiente puede empezar por estas definiciones y por adoptar las correcciones técnicas, sin una nueva corrida. El piloto de seis vistas no sustituye automáticamente la aceptación espacial ni la normalización.

## Reproducción

[Herramienta](../herramientas/diagnosticar_observable_angular.py), [resultados y huellas](evidencias/diagnostico-observable-f9a77ef.json), [pruebas](evidencias/pruebas-diagnostico-observable.txt) y [validación](evidencias/validacion-diagnostico-observable.json). La suite local reúne **60 pruebas satisfactorias**, cuatro nuevas del diagnóstico. Reutilizar el helper de geometría de la entrega reproduce su clasificación de columnas; no representa una validación independiente de toda su física.

Desde la raíz de nuestra réplica, con `ENTREGA` apuntando a la carpeta congelada de f9a77ef:

```console
python herramientas/diagnosticar_observable_angular.py ENTREGA --salida DIAGNOSTICO_NUEVO.json
```

El programa verifica las huellas declaradas de los archivos usados, registrando si la coincidencia requiere CRLF→LF. No modifica la entrega ni sobrescribe informes. El alcance está limitado a las dos corridas, geometría y vista indicadas; no es todavía un evaluador general del piloto.
