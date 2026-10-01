# Revisión independiente del complemento R2-01

Revisión: 1 de octubre de 2026, Colombia. Ejecución declarada por estudiantes: 30 de septiembre de 2026, SC3, trabajo 30580. Se revisa exclusivamente OE1.

## Dictamen y alcance

**Resultado favorable para el mecanismo de asignación de materiales en los casos dirigidos de R2-01.** El transporte está entregado y su análisis se reprodujo localmente. La prueba no estima la frecuencia del defecto bajo la fuente representativa, no valida toda la campaña y no cierra OE1 ni P-01…P-04.

Entrega inmutable: [a4d7b79, informe y registros](https://github.com/anlegogo/muografia-documentada/tree/a4d7b79aeb9bd861516e81afa25d7950d2245488/objetivo-1/entregas/2026-09-30-complemento-r2-01). Comparador: repositorio de estudiantes, commit `0d97beb5287ebc0e43ecc63ad1c4c43fa0d87e46`. Las ramas se mantienen separadas.

## Qué verificamos

- Seis corridas de 12 primarios: A/B por tres semillas, 72 transportes y 36 pares. Es la misma lista congelada de 12 muones de 10 TeV; no son 72 primarios independientes de la fuente.
- Integridad del manifiesto: todos los archivos concuerdan; `.gitattributes` concuerda al normalizar CRLF a LF tras la extracción Windows. Los datos científicos se comprobaron byte a byte sin normalización.
- Identidad de los primarios mediante FNV recalculado, SHA de la lista, IDs y estado aleatorio inicial A/B; reconstrucción independiente de los seis histogramas desde los registros individuales.
- El comparador de los estudiantes termina `OK`, sin contratos bloqueantes fallidos. Sus dos CSV de resultados se reproducen byte a byte y la cobertura JSON coincide. La comprobación de eficiencia frente a la campaña no aplica a esta fuente dirigida.
- [Auditoría propia](evidencias/revision-complemento-r201.json): 103 controles, 103 satisfactorios. No se ejecutó Geant4 localmente.

## Resultados

| Grupo planificado | Pares A/B | Material de A en el solape | Material de B en el solape | Detección |
|---|---:|---|---|---|
| Entrada desde conducto, IDs 0–5 | 18 | Conducto, A0 | Cuerpo denso, A1 | 18 detectados en ambas |
| Entrada desde cuerpo denso, IDs 6–11 | 18 | Cuerpo denso, A1 | Cuerpo denso, A1 | 17 detectados en ambas; 1 no detectado en ambas |

Las longitudes asignadas concuerdan con la longitud del solape a tolerancia absoluta de 1 micrómetro. Los 18 controles del segundo grupo tienen registros idénticos A/B salvo la etiqueta de variante.

En el primer grupo, B presenta menor energía de salida en 17/18 pares. Al calcular por separado la pérdida dentro de Z, `(Ein−Eout)B−(Ein−Eout)A`, también es mayor en 17/18. Son magnitudes diferentes: no debe identificarse automáticamente diferencia de energía de salida con diferencia de pérdida. Las energías de borde son interpolaciones registradas dentro del paso.

Tres pares cambian un bin del histograma: ID 0/semilla 1026093011, ID 1/1026093011 e ID 0/1026093012. Ningún par cambia su condición de detección. Esto evidencia sensibilidad del transporte y del píxel a la corrección en estos casos; no cuantifica un cambio poblacional de imagen.

## Precisión sobre la cobertura y la interpretación física

En A, `mat_in` distingue los lados de entrada observados. En B, el registro agregado no identifica directamente el lado: la entrada se infiere del diseño y las comprobaciones geométricas, como reconoce el informe. El material A1 sí está registrado en B para las 36 comparaciones. El desplazamiento lateral local cerca del solape no es una cota de la desviación acumulada de toda la trayectoria. Por ello aceptamos evidencia del mecanismo en los casos dirigidos, sin afirmar que se haya reconstruido la trayectoria real completa de B ni demostrado directamente cada lado de entrada en B.

La atribución de pérdidas individuales a procesos radiativos concretos exige información por pasos/procesos; el registro agregado permite medir diferencias, pero no atribuir por sí solo cada pérdida a un proceso específico. Esta precisión no invalida el resultado de asignación de material.

## Reproducción local

Con Python 3.12.14, numpy 2.4.4 y pandas 3.0.6, desde el directorio de trabajo superior al repositorio:

```powershell
tmp/muography-audit-venv/Scripts/python.exe tmp/codigo-r201/scripts/analysis/oe1_r201_compare.py compare --attempt tmp/revision-r201-a4d7b79/objetivo-1/entregas/2026-09-30-complemento-r2-01/corridas/intento-01 --inputs muografia-documentada/objetivo-1/ensayos/complemento-r2-01-v1 --mask tmp/revision-entrega-3a49770/objetivo-1/entregas/2026-09-30-segundo-ensayo-etapa-1/analisis/roi/R_int.mask.txt --out tmp/reproduccion-r201-director
tmp/muography-audit-venv/Scripts/python.exe muografia-documentada/herramientas/revisar_complemento_r201.py --entrega tmp/revision-r201-a4d7b79/objetivo-1/entregas/2026-09-30-complemento-r2-01 --inputs muografia-documentada/objetivo-1/ensayos/complemento-r2-01-v1 --reproduccion tmp/reproduccion-r201-director --out muografia-documentada/objetivo-1/evidencias/revision-complemento-r201.json
```

Las rutas `tmp` son extracciones locales de las revisiones citadas. El comparador exige un directorio de salida nuevo; para repetirlo elegir otra ruta y pasarla también al auditor.

## Siguiente paso

Actualizar el diseño de etapa 2: fuente representativa, criterio de precisión estadística, tamaño de muestra y almacenamiento disponible en SC3. El complemento no aporta una tasa utilizable para dimensionar esa muestra. No procede repetir automáticamente las 114 vistas ni considerar aprobados los parámetros provisionales de etapa 2. Una traza adicional se justificaría si se requiere comprobar directamente el lado real de entrada en B; no se solicita como repetición automática de esta prueba favorable.
