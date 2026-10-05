# Opacidad nominal del catálogo y alcance de la evaluación

2026-10-04, Colombia. Diagnóstico de la dirección sobre fuentes del repositorio `64ca8b25b0ac16a93f8b23fca0e0c28daafec839`, posterior al complemento OE3-C1. No se ejecutó entrenamiento, inferencia adicional ni transporte de muones. No se modifican la entrega ni los umbrales de calidad.

## Qué se pudo calcular

Los JSON geométricos proporcionan densidad de roca, densidad de anomalías y dimensiones. Los rayos centrales y las intersecciones analíticas del evaluador permiten construir una **opacidad nominal del edificio**, declarada por ese modelo geométrico. No es opacidad inferida por la red ni integral sobre las trayectorias efectivas de los muones dispersados.

Para un rayo de longitud total L dentro del edificio y longitud l dentro de una única anomalía, con longitudes en metros y densidades en g/cm³:

$$X_A=100\,[\rho_r(L-l)+\rho_a l]\quad [\mathrm{g/cm^2}].$$

El factor 100 convierte metros a centímetros. La referencia homogénea del **mismo rayo**, sin reemplazo de material, sería X_h = 100 rho_r L. Por tanto:

$$\Delta X_{\mathrm{densidad}}=X_A-X_h=100(\rho_a-\rho_r)l.$$

Una anomalía menos densa reduce la opacidad nominal y una más densa la aumenta. Esta afirmación geométrica no demuestra que la red recupere dichas diferencias.

## Correspondencia con los controles C2

Se reprodujeron las máscaras y los índices del registro C2, conservando los cinco donantes por píxel. Se verificó que los donantes no atraviesan anomalías y que los objetivos seleccionados no atraviesan otras anomalías. Así se evita sumar de forma incorrecta densidades en solapamientos. Las filas sin soporte se conservan.

Los controles son otros rayos, con longitudes próximas pero no idénticas. La diferencia entre sus opacidades medias se descompone exactamente como:

$$\overline X_A-\overline X_B=100(\rho_a-\rho_r)\overline l+100\rho_r(\overline L_A-\overline L_B).$$

El segundo término registra la diferencia geométrica del control. La tabla separa ambos términos y no atribuye toda la diferencia a la anomalía. La media de donantes conserva las ponderaciones de C2, incluidas las repeticiones utilizadas para estimar esa media.

## Resultados y verificaciones

- Se conservan **54 filas** de anomalía/vista, de las cuales **48** cumplen el soporte C2.
- Pasan cuatro casos analíticos de unidades y composición de materiales: roca homogénea, inclusión parcial, longitud de anomalía cero y ocupación completa. Se admite únicamente redondeo numérico de 10⁻¹⁰ en esos casos.
- Se verificaron las huellas de geometrías/datos mediante el contrato EF-01 y la reproducción de los 54 registros C2.
- El residuo máximo de la descomposición anterior es **1,0004 × 10⁻¹⁰ g/cm²**.
- En las 48 filas elegibles, el término nominal de densidad varía entre **−17.242,01 y +5.616,20 g/cm²**. El término de longitud del control no cambia su signo en esas filas. Estas cifras describen el catálogo y el soporte elegido; no son errores de reconstrucción ni umbrales de detección.

La [tabla completa](evidencias/opacidad-nominal-v1/opacidad_nominal.csv) incluye opacidades, longitudes, densidades, términos separados y contraste de cuentas de la referencia. Se adjuntan [verificaciones y fuentes](evidencias/opacidad-nominal-v1/resultado.json) e [inventario](evidencias/opacidad-nominal-v1/inventario.json).

## Precisión sobre el material de una cavidad

`geo-gen-01`, anomalía 2, declara rho = **0,048 g/cm³**. El constructor versionado en [DetectorConstruction.cc](../objetivo-1/originales/scripts/simulation/geant4_app/src/DetectorConstruction.cc) contiene una sustitución explícita: para rho < 0,05 retorna `G4_AIR`, en lugar de crear el material con la densidad solicitada.

Por ello se marcan sus **seis filas elegibles** con `material_override_G4_AIR_in_repository=true`. Los números de esta tabla usan el JSON y no se presentan como opacidad efectiva de Geant4 para esas filas. Antes de utilizar una referencia de opacidad efectiva habría que vincular el constructor y la densidad de `G4_AIR` a la versión realmente ejecutada en producción. Esta revisión no certifica esa vinculación ni supone un valor de densidad del aire no extraído del entorno de producción.

No se concluye que esta convención haya causado el desempeño observado de las redes ni que obligue a repetir la campaña. Las métricas anteriores comparan las matrices recibidas con sus referencias y permanecen verificadas. El hallazgo delimita la interpretación física de una futura referencia de opacidad.

## Qué no puede obtenerse mediante un cambio de unidades

El contraste evaluado es C_N = media(N_A)/media(N_B) − 1. El contraste nominal de esta tabla es C_X = media(X_A)/media(X_B) − 1. Ambos son cocientes adimensionales, pero corresponden a magnitudes diferentes. No existe aquí una calibración que permita sustituir uno por otro.

En una descripción general, el conteo esperado de un píxel depende del espectro incidente y de la respuesta del transporte/detector:

$$\mathbb E[N_p]=t\int\Phi(E,\Omega)\,K_p(E,\Omega;\rho,\mathrm{materiales},\mathrm{detector})\,\mathrm dE\,\mathrm d\Omega.$$

Para invertir cuentas en opacidad debe fijarse y verificarse esa respuesta o una aproximación calibrada. No basta multiplicar el contraste por una densidad, aplicar un logaritmo de transmisión sin modelo o ajustar una relación a las mismas reservas y declararla validación independiente. Tampoco se equipara automáticamente el signo del contraste de medias con la respuesta de cada trayectoria: hay promediado angular, estadística finita y transporte.

La distinción entre opacidad como integral de densidad y medición de flujo está respaldada por [Jourde et al. (2016)](https://www.nature.com/articles/srep23054). No se trasladan al volcán sus constantes de calibración ni sus resultados temporales.

## Decisión y avance del pendiente

**OE3-P06 avanza, pero permanece parcial:** ya hay SNR/CNR, contraste de cuentas y una referencia nominal de opacidad del catálogo en el soporte evaluado. Falta una inversión/calibración de las imágenes a opacidad y la trazabilidad del material efectivo en el caso señalado. No se afirma que la red haya reconstruido opacidad ni se cierra ese compromiso mediante una nueva etiqueta.

Antes de solicitar cómputo adicional, procede revisar los metadatos de producción y el modelo de respuesta existente. Si no hay una calibración utilizable, debe registrarse la limitación o diseñarse expresamente una validación nueva; repetir el complemento o prolongar el entrenamiento no resuelve esa carencia por sí solo. El resultado negativo del benchmark OE3-C1 y sus conclusiones se conservan.

## Reproducción

El [script](herramientas/diagnosticar_opacidad_nominal.py) usa las herramientas geométricas y el contrato EF-01 congelados. El directorio de salida debe ser nuevo:

```bash
python objetivo-3/herramientas/diagnosticar_opacidad_nominal.py \
  --repo . --data /ruta/insumos \
  --registry objetivo-2/evidencias/ef01-c2/controles.json \
  --output /ruta/opacidad-nominal
```

Incidencias de preparación: se reemplazó una igualdad binaria en un caso analítico por comparación con tolerancia de redondeo. El control de densidad detuvo inicialmente el caso 0,048; se conservó después como referencia nominal del JSON con marca explícita de sustitución de material, sin inventar densidad efectiva ni omitir el caso. No se alteraron datos ni resultados de las redes.
