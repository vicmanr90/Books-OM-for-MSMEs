"""Contrato administrativo; cambiarlo requiere registrar la decisión."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
CSV_HEADERS = {'registro_decisiones.csv': ['decision_id', 'fecha', 'etapa', 'tema', 'decision', 'alternativas_consideradas', 'justificacion', 'responsable', 'impacto', 'observaciones'], 'registro_cambios_protocolo.csv': ['change_id', 'fecha', 'version_anterior', 'version_nueva', 'seccion', 'regla_anterior', 'regla_nueva', 'justificacion', 'impacto', 'responsable'], 'registro_prompts.csv': ['prompt_run_id', 'fecha', 'etapa', 'tarea', 'prompt_id', 'prompt_version', 'modelo', 'archivo_entrada', 'archivo_salida', 'validado_por', 'estado_validacion', 'observaciones']}
SECTOR_DIRS = ['00_gobernanza', '01_delimitacion', '02_protocolo', '03_busqueda', '04_screening', '05_fulltext', '06_calidad', '07_extraccion', '08_sintesis', '09_orientaciones', '10_validacion', '11_manuscrito']
INTEGRATOR_DIRS = ['00_gobernanza', '01_base_maestra', '02_armonizacion', '03_analisis_transversal', '04_sintesis', '05_framework', '06_manuscrito']
FICHA_FIELDS = ['project_id', 'slug', 'titulo_provisional', 'sector', 'subsectores', 'nivel_decisional', 'poblacion_objetivo', 'objeto_estudio', 'unidad_analisis', 'pregunta_central', 'objetivo_general', 'objetivos_especificos', 'investigadores', 'fecha_inicio', 'estado', 'version_protocolo', 'version_taxonomia', 'observaciones']
TAX_HEADERS = ['taxonomy_id', 'version', 'nivel_1', 'nivel_2', 'nivel_3', 'nombre', 'definicion', 'sinonimos', 'nivel_decisional', 'sector_aplicable', 'estado', 'fuente', 'notas']
VARIABLE_HEADERS = ['variable_id', 'variable_name', 'label', 'description', 'data_type', 'allowed_values', 'missing_value', 'source_level', 'required', 'version', 'notes']
CATALOG_HEADERS = ['catalog_id', 'value', 'label', 'definition', 'active', 'version']

def read_yaml(path):
    with path.open(encoding="utf-8-sig") as stream:
        return yaml.safe_load(stream)

def load_projects():
    data = read_yaml(ROOT / "config/proyectos.yml")
    if not isinstance(data, dict) or not isinstance(data.get("proyectos"), list):
        raise ValueError("El registro debe contener una lista 'proyectos'.")
    records = data["proyectos"]
    ids, slugs = set(), set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Registro de proyecto inválido.")
        for key in ("id", "slug", "sector", "nivel_decisional", "tipo", "estado"):
            if key not in record:
                raise ValueError(f"Falta {key} en el registro.")
        ident, slug = record["id"], record["slug"]
        if type(ident) is not int or not 1 <= ident <= 22:
            raise ValueError(f"ID inválido: {ident!r}")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", slug):
            raise ValueError(f"Slug inválido: {slug!r}")
        if ident in ids or slug in slugs:
            raise ValueError("ID o slug duplicado.")
        ids.add(ident); slugs.add(slug)
        if record["tipo"] != ("integrador" if ident == 22 else "sectorial"):
            raise ValueError(f"Tipo incoherente para {ident}.")
        for key in ("sector", "nivel_decisional", "estado"):
            if not isinstance(record[key], str) or not record[key].strip():
                raise ValueError(f"{key} inválido para {ident}.")
    if ids != set(range(1, 23)):
        raise ValueError("Deben registrarse exactamente los proyectos 1 a 22.")
    return {p["id"]: p for p in records}

def folder_name(project):
    return f'{project["id"]:02d}_{project["slug"]}'
