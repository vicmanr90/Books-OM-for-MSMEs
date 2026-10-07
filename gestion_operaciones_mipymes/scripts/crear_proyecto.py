"""Crear una instancia sectorial: python scripts/crear_proyecto.py 02 [--force].

La copia se prepara antes de publicar el destino. --force conserva un respaldo
local completo; no migra contenidos científicos de la instancia anterior.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import yaml
from _estructura import ROOT, SECTOR_DIRS, CSV_HEADERS, FICHA_FIELDS, load_projects, folder_name, read_yaml


def create(ident, force=False):
    projects = load_projects()
    project = projects.get(ident)
    if project is None:
        raise ValueError(f"Proyecto desconocido: {ident}")
    if project['tipo'] != 'sectorial':
        raise ValueError('El integrador tiene estructura propia; no usa la plantilla sectorial.')
    template = ROOT / '_template_proyecto'
    destination = ROOT / folder_name(project)
    if destination.is_symlink():
        raise ValueError('No se reemplazan enlaces simbólicos.')
    if destination.exists() and not force:
        raise ValueError(f'Ya existe {destination.name}. Use --force para reemplazar con respaldo.')
    if destination.exists() and not destination.is_dir():
        raise ValueError('El destino existente no es una carpeta.')
    for stage in SECTOR_DIRS:
        if not (template / stage).is_dir():
            raise ValueError(f'Plantilla incompleta: {stage}')
    for name in CSV_HEADERS:
        if not (template / '00_gobernanza' / name).is_file():
            raise ValueError(f'Plantilla incompleta: {name}')
    ficha_path = Path('00_gobernanza/ficha_proyecto.yml')
    ficha = read_yaml(template / ficha_path)
    if not isinstance(ficha, dict) or not set(FICHA_FIELDS).issubset(ficha):
        raise ValueError('Ficha de plantilla incompleta.')
    backup = None
    with tempfile.TemporaryDirectory(prefix='.crear-', dir=ROOT) as temporary:
        staged = Path(temporary) / destination.name
        shutil.copytree(template, staged)
        # Sustituir solamente metadatos administrativos, conservando comentarios.
        text = (staged / ficha_path).read_text(encoding='utf-8')
        mapping = {'project_id': project['id'], **{k: project[k] for k in ('slug','sector','nivel_decisional','estado')}}
        lines = text.splitlines(keepends=True)
        for key, value in mapping.items():
            matches = [i for i,line in enumerate(lines) if line.startswith(key + ':')]
            if len(matches) != 1:
                raise ValueError(f'La plantilla requiere exactamente un campo {key}.')
            lines[matches[0]] = yaml.safe_dump({key:value}, allow_unicode=True, sort_keys=False)
        (staged / ficha_path).write_text(''.join(lines), encoding='utf-8', newline='\n')
        if destination.exists():
            backup_root = ROOT / '.respaldos'
            backup_root.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = backup_root / f'{destination.name}_{stamp}'
            destination.rename(backup)
        try:
            staged.rename(destination)
        except OSError:
            if backup is not None:
                backup.rename(destination)
            raise
    print(f'Creado: {destination}\nID: {ident:02d}; sector: {project["sector"]}; nivel: {project["nivel_decisional"]}; estado: {project["estado"]}')
    if backup:
        print(f'Respaldo local: {backup}')
    print('Metadatos administrativos actualizados; ficha científica pendiente.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id', type=int, help='ID del registro maestro, con o sin cero inicial.')
    parser.add_argument('--force', action='store_true', help='Reemplazar instancia conservando respaldo local.')
    args = parser.parse_args()
    try:
        create(args.project_id, args.force)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
