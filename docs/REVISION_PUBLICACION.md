# Revisión previa a publicación

Fecha: 2026-10-26 (Colombia). Revisión de la propuesta #3 sobre `5173cde81e9a8a5c63be5fcf1da073b76548be20`.

## Dictamen

Se completó la revisión documental y técnica descrita abajo. No se identificaron credenciales ni un impedimento concreto de publicación en el alcance examinado. Se recomienda integrar las licencias y conservar las limitaciones de reproducción declaradas. Este dictamen no cambia la visibilidad del repositorio ni certifica la inexistencia absoluta de secretos o derechos de terceros.

La dirección confirmó autorización de los autores y ausencia de restricciones institucionales conocidas. No se infiere que las licencias de terceros sean reemplazables ni que el contenido esté libre de datos personales.

## Alcance y controles

- Se inspeccionaron los objetos Git de la copia local no superficial: 166 commits, 1.482 árboles y 5.080 versiones de archivos. La lectura se hizo desde objetos Git, sin incorporar modificaciones locales.
- Se cotejaron las puntas de las ramas históricas con GitHub. Los cinco commits remotos posteriores a `e6f139e406d47c07a210dc87e08314271bc5dcf4` se revisaron mediante sus cambios completos; son documentales. Las ramas remotas enumeradas quedaron cubiertas por ambos recorridos.
- Se buscaron marcadores de claves privadas, tokens GitHub/Google/servicios, identificadores de claves de nube, asignaciones de credenciales entre comillas y URL con credenciales. No hubo coincidencias en el barrido local. Los cambios remotos se inspeccionaron adicionalmente.
- Se abrieron 165 contenedores ZIP/NPZ del recorrido histórico, incluidos contenedores anidados y el paquete de 121 archivos del informe. No se registraron errores de apertura ni omisiones por el límite de tamaño configurado. No se ejecutaron sus contenidos.
- Se extrajo texto de los 32 PDF del árbol local versionado, con 382.000 caracteres en total. Se comprobó identidad de cada PDF con su objeto Git antes de leerlo. No se encontraron patrones de credenciales ni términos de documentos de identidad o teléfono en esa extracción. Esta comprobación no incluye OCR de imágenes.
- Se revisaron las fuentes LaTeX, las declaraciones de procedencia de figuras, los scripts editables y los avisos de código de terceros. No se alteraron fuentes originales ni se recompiló o reemplazó el informe.
- Se revisó el alcance de las licencias y la separación entre acceso a Drive, autorización de reutilización y verificación científica.

## Material ajeno y atribución

| Material | Hallazgo y tratamiento |
|---|---|
| EcoMug.h | Cabecera GPL v3 o posterior y autoría conservadas; texto completo incluido. Integración directa delimitada en LICENSE.md. |
| nlohmann/json 3.11.3 | MIT y avisos internos preservados, incluidos otros contribuyentes; textos MIT y Apache-2.0 disponibles. |
| Geant4 | Dependencia externa localizada por CMake; conserva su propia licencia y reconocimiento. No se declara su código como propio. |
| Figuras científicas del informe | Las fuentes revisadas las atribuyen a elaboración de los autores o a registros del proyecto; se conservan scripts, TikZ y datos de procedencia. No se identificó una figura de artículo externo presentada como propia. Esta constatación documental no prueba por sí sola la originalidad de cada trazo. |
| Logotipo UIS | Se identifica específicamente como material institucional procedente de la plantilla; queda fuera de CC BY y no se concede permiso de reutilización ni respaldo institucional. Se conserva en el contexto académico original. No se verificó una autorización independiente de marca; se cuenta con la declaración de ausencia de restricciones institucionales conocidas. |
| Bibliografía y cita histórica | Se conservan referencias y atribuciones; la licencia de la tesis no se aplica a las obras citadas ni concede derechos sobre ellas. |
| Dependencias y paquetes LaTeX | Conservan sus licencias. La revisión no autoriza redistribuir un entorno o ejecutable completo sin revisar sus componentes. |

## Información identificativa conservada

El repositorio contiene nombres de autores, dirección y personas mencionadas en dedicatorias y agradecimientos, códigos estudiantiles en la fuente y el PDF del informe, correos de autoría/contribución y de terceros, y rutas o nombres de usuario/host asociados al entorno de cómputo. Son datos identificativos y de procedencia, no credenciales de autenticación por sí mismos.

Se conservan dentro del material académico autorizado y de los avisos de atribución. No se publican aquí listados adicionales de esos datos. No se modificaron bitácoras, correos del historial, dedicatorias ni archivos originales. El barrido no identificó documentos nacionales de identidad, contraseñas o teléfonos mediante los controles descritos.

## Limitaciones que permanecen

- No se realizó una auditoría forense, OCR integral, análisis de todos los formatos binarios ni detección de toda posible credencial sin formato reconocible.
- No se inspeccionaron artefactos ajenos a los objetos Git revisados, como adjuntos de issues, releases, registros de Actions o todos los binarios de Drive.
- La versión exacta de EcoMug ejecutada en UIS y la verificación íntegra de pesos/datos continúan pendientes como aspectos de procedencia y reproducción; no se presentan como completadas.
- La autorización declarada no sustituye una investigación jurídica independiente. Se mantienen las exclusiones explícitas de material ajeno.
- El cambio de visibilidad es una acción posterior, distinta de esta revisión y de la integración de licencias.

Se conserva el estado científico del trabajo: no se acredita un factor favorable de reducción de adquisición ni validación física general. La publicación facilita su consulta y evaluación crítica, no modifica esas conclusiones.
