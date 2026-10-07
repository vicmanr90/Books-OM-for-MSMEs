# Gestión de Operaciones en MiPymes

Infraestructura para 21 estudios sectoriales y un proyecto integrador. Esta
inicialización no contiene evidencia, datos científicos ni metodología desarrollada.

## Estructura

- `config/proyectos.yml`: registro de los 22 proyectos; los aún no creados son válidos.
- `00_manual_metodologico/`: manual, taxonomía, diccionario, calidad, política de IA y prompts comunes.
- `_template_proyecto/`: plantilla de gobernanza y etapas sectoriales.
- `01_manufactura_estrategico/`: primera instancia creada por el script.
- `22_integrador/`: base maestra, armonización, análisis transversal, síntesis, framework y manuscrito.
- `scripts/`: creación y validación administrativa de la estructura.

Los maestros definen esquemas comunes; cada proyecto conserva sus artefactos y
registros propios. Los identificadores y versiones permitirán integrar los 21
estudios. TODO: aprobar esos esquemas y las correspondencias de armonización.

## Uso

Python 3.10 o posterior con las dependencias de `pyproject.toml` previamente disponibles.
No se instalan paquetes automáticamente. Quarto será necesario cuando se rendericen los `.qmd`.
Desde esta carpeta, tanto en PowerShell como en terminal estándar:

```sh
python scripts/crear_proyecto.py 02
python scripts/validar_estructura.py
```

Desde la raíz Git: `cd gestion_operaciones_mipymes`. Los scripts también funcionan
desde cualquier directorio porque resuelven la raíz a partir de su propia ubicación.
En PowerShell, para un ejecutable con espacios: `& "C:/ruta/python.exe" scripts/validar_estructura.py`.

Crear rechaza destinos existentes. `--force` reemplaza la instancia y conserva una
copia previa en `.respaldos/` (local, ignorada por Git). El proyecto 22 tiene una
estructura propia y ya existe; no se genera desde la plantilla sectorial.
Los errores de validación o creación devuelven un código distinto de cero.

## Cambios y reproducibilidad

No modificar manualmente la plantilla después de iniciar un proyecto sin registrar
el cambio en `registro_cambios_protocolo.csv` del proyecto afectado (y una decisión
en `registro_decisiones.csv` cuando corresponda). Los cambios de plantilla no migran
automáticamente las instancias existentes. Conservar una referencia Git de cada versión usada.
Registrar decisiones reales y ejecuciones de IA; nunca agregar registros ficticios.

Mantener datos originales y derivados separados en `07_extraccion/`, scripts de
análisis en `08_sintesis/analisis/`, síntesis en `08_sintesis/sintesis/` y escritura en
`11_manuscrito/`. En el integrador usar las etapas equivalentes. Preferir CSV UTF-8
o Parquet para datos; Excel es la interfaz humana del esquema de variables.
Registrar insumos, versiones, parámetros y salidas al desarrollar análisis.
Las salidas regenerables van en `resultados_temporales/`; los datos de investigación
no se excluyen indiscriminadamente de Git. No versionar credenciales.

## Pendientes

TODO: desarrollar y aprobar manual, criterios, taxonomía, variables, política de IA,
prompts, protocolos, fichas científicas y reglas de integración. La validación
estructural no certifica calidad científica ni verifica el contenido de los TODO.

El repositorio Git está en la carpeta padre. No se crea un repositorio anidado ni
se realizan commits automáticamente. Las dependencias están declaradas, sin lockfile;
TODO: fijar un entorno probado cuando se introduzcan análisis reproducibles.
