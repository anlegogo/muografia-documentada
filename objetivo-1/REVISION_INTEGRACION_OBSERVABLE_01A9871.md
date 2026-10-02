# Revisión de integración SC3 y definición de la imagen

2026-10-02, Colombia. Entrega revisada: rama `oe1/justificacion-fisica-produccion`, commit **01a98718ba381797f6d4616e25d42ad533cad6f1**. [Entrega congelada](https://github.com/anlegogo/muografia-documentada/tree/01a98718ba381797f6d4616e25d42ad533cad6f1/objetivo-1/entregas/2026-10-01-justificacion-fisica-produccion). [Evidencia independiente](evidencias/revision-integracion-01a9871.json).

**Resultado: la comprobación solicitada de las herramientas sobre dos bloques en SC3 queda respaldada. La propuesta física avanzó y corrige conclusiones anteriores, pero requiere ajustes antes de ejecutar C3 o habilitar producción.** No se necesitan nuevos muones para corregir esos puntos de diseño. La rama estudiantil se conserva sin fusionar; esta revisión no redefine ni declara completo el OE1.

## Comprobación técnica recibida

El trabajo 30631 registra cinco segundos de ejecución satisfactoria en SC3, usando bloques existentes. No genera muones nuevos. Se contrastaron:

- Las huellas de **39 archivos Python** utilizados, todas iguales a los objetos Git del commit `c4b6e4c`.
- **23 archivos de entrada**, cuyas huellas coinciden y se mantienen iguales antes y después de ejecutar las herramientas.
- Los cinco códigos de salida cero y sus archivos de error vacíos. Los recibos registran dos publicaciones y una repetición reconocida como `already_verified`.
- Los hashes de la fusión y exportación, la matriz NPZ frente al CSV y frente a la suma independiente de los bloques: **200.000 primarios, 69.995 registros con E_cin > 3 GeV y 130.190 de todas las energías**.
- La fusión ejecutada de nuevo localmente, sin aceptar conversiones CRLF: reproduce exactamente las huellas de imagen y metadatos de SC3.

Se acepta esta verificación de publicación, fusión y exportación para los dos bloques. No equivale a validar el lanzador automático de campaña, su interacción con la cola o todos los fallos del almacenamiento. Tampoco certifica física. Las 78 pruebas locales anteriores siguen como antecedente; no se presentan como pruebas nuevas de esta revisión.

## Corrección de la observación T-01

Se confirma la observación de los estudiantes: **las 204 entradas de los seis manifiestos originales coinciden con los objetos Git de `f9a77ef`**. La revisión anterior comparó una copia extraída que había sufrido conversión de finales de línea; atribuir el problema a los «bytes versionados» fue un error de la revisión.

Se corrige el informe anterior. No hay que pedirles recuperar ni reemplazar datos SC3 por esta observación. La regla `-text` ya incorporada protege las futuras extracciones; se conserva la auditoría anterior como registro de lo ocurrido en la copia local.

## Avance en la definición física

Se reprodujo `relacion_conteos_exposicion.py`: **113 valores numéricos** coinciden a tolerancia absoluta/relativa `1e-10` (Python 3.12.14, NumPy 2.4.4). Esto confirma el cálculo, no todas sus interpretaciones.

La nueva documentación distingue correctamente la contención en planos grandes de la equivalencia con un detector de 1,2 m. Retira la conclusión de que C3 no era necesario y mantiene abiertos los bordes con corte energético. Propone un **conteo direccional sintético con exposición convencional**, sin presentarlo como días de un instrumento real. Es una propuesta concreta que la dirección debe valorar frente al alcance académico; todavía no constituye una definición final aprobada.

## Ajustes antes de nuevas corridas

### 1. El presupuesto de C3 no satisface su propio criterio estadístico

Se propone equivalencia si cuatro intervalos simultáneos al 95 % caben dentro de una tolerancia de ±5 %, pero se dimensiona con 1.600 cuentas de panel, usando la precisión de una sola cuenta Poisson.

Con Bonferroni para cuatro bandas, el factor normal es 2,4977. Aun con una referencia sin incertidumbre, 1.600 cuentas dan una semiamplitud aproximada de **6,24 %**, superior a 5 %. Si la referencia tuviera 1.707 cuentas, sería aproximadamente **8,69 %**. Esa última cifra es ilustrativa: el diseño nuevo restringe direcciones y exige correr una referencia compatible; no puede reutilizar c01 sin justificarlo.

Como aproximación de planificación cerca de R=1, se requieren unas 2.496 cuentas si la otra referencia fuese exacta, o unas 4.991 en cada brazo si ambos tienen igual estadística, solamente para que la anchura nominal se acerque al umbral. **Estos números no son un presupuesto aprobado ni garantizan potencia de equivalencia.** Fijar método de intervalo para la razón, potencia, cuatro bandas exactas, cuentas en ambos brazos y regla de parada antes de recalcular primarios y coste. Aclarar también qué cuarta banda se evalúa: el intervalo direccional declarado de 30–200 mil g/cm² abarca tres de las bandas listadas.

### 2. La referencia de cielo no está medida en toda la imagen

`np.interp` prolonga con un valor constante la eficiencia de cielo hacia elevaciones donde esta geometría no ofrece píxeles de cielo abierto. Hay referencia observada desde **6,94°**, pero la imagen comienza a 2°: **28 filas** quedan por debajo. Para la selección de roca con columna ≥10.000 g/cm², **7.122 de 16.322 píxeles (43,6 %)** utilizan esa prolongación.

Por ello, la figura puede conservarse como diagnóstico con la extrapolación explícita, pero no permite afirmar todavía una transmisión física directamente comparable con el surrogate en toda la imagen. Definir una referencia de cielo compatible por dirección, espectro, corte y superficie de inyección; evaluar primero si puede calcularse con las tablas y datos existentes. Si se requiere una referencia simulada, justificarla dentro del mismo protocolo, sin ordenar una campaña adicional por defecto. El cociente cercano a uno de la identidad conteos/exposición usa una eficiencia calculada de esos mismos conteos: comprueba consistencia interna, no una validación independiente.

### 3. Delimitar qué probaría C3 antes de implementarlo

La contención de muones generados sobre el panel ayuda a proponer el tamaño inicial de una fuente amplia, pero no demuestra que se haya incluido todo el flujo que entra desde fuera. Tampoco está demostrado que restringir direcciones con un margen de 2° conserve esa contribución. El protocolo debe justificar o comprobar la estabilidad frente al dominio espacial y angular; sus costes actuales omiten el aumento por ese margen. No basta declarar que el recorte «no pierde» entradas.

Antes de gastar SC3, decidir la afirmación que se quiere respaldar. Si se adopta el estimador idealizado sin afirmar equivalencia instrumental, C3 no debe convertirse automáticamente en requisito de esa equivalencia excluida del producto. Si se afirma que representa el panel físico, C3 u otra demostración adecuada sí necesita resolver esa cuestión. En ambos casos permanecen la referencia de normalización, la definición de fuente y el criterio de bordes con corte.

## Siguiente paso acotado

1. Dar por recibida la prueba técnica de los dos bloques y la corrección de T-01; no repetirlas.
2. Dirección y estudiantes: acordar la definición del producto del OE1 y ajustar sobre papel los puntos anteriores. No lanzar C3 con el presupuesto actual.
3. Con esa definición, cerrar un protocolo único con criterios y presupuesto. Implementar solo lo necesario y decidir el piloto P0; la campaña de 114 vistas sigue condicionada a esa aceptación.

No se accedió directamente a SC3 ni se ejecutó Geant4 durante esta revisión. Se verificaron los archivos y registros entregados y se reprodujeron análisis/fusión localmente. No se enviaron mensajes a los estudiantes.
