# Motivo del primer intento de K0

El primer intento de K0 (trabajo 30564, 30 de septiembre de 2026, de 19:33 a 19:35 UTC) terminó con `TOTAL rc=1`: fallaron cruces, banco sintético, inercia del modo legado y pruebas de Python; la salida anticipada y la auditoría de aleatorios pasaron.
Las pruebas de C++ se compilaron contra el paquete del piloto de `fuentes/A2`, donde `third_party/` está en la raíz del paquete, y no encontraron `json.hpp`.
Las pruebas de Python no encontraron `../simulation/geant4_app/tables` (106 pruebas ejecutadas, 24 errores).
El segundo intento (trabajo 30565, `../k0/`) ejecutó las mismas pruebas en la disposición del repositorio, extraída con `git archive` de A2 `fdaef4b`, TOOLS `3315f82` y A `9520170`.
Antes de ejecutar, los archivos de P2 se comprobaron contra `P2-instrumentacion.sha256` (en `codigo/`); el resultado está en `../k0/procedencia.txt`.
El código bajo prueba no cambió entre ambos intentos.
