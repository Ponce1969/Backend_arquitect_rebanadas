#!/usr/bin/env python
"""
Script para actualizar automáticamente las importaciones de los archivos de compatibilidad.

Este script busca importaciones de los archivos de compatibilidad en el código fuente
y las actualiza para que apunten directamente a las nuevas ubicaciones.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Mapeo de importaciones antiguas a nuevas
IMPORT_MAPPINGS = {
    # Entidades
    'from src.domain.shared.entities import Moneda': 'from src.features.monedas.domain.entities import Moneda',
    'from src.domain.shared.entities import TipoDocumento': 'from src.features.tipos_documento.domain.entities import TipoDocumento',
    
    # DTOs
    'from src.domain.shared.dtos import MonedaDto': 'from src.features.monedas.application.dtos import MonedaDto',
    'from src.domain.shared.dtos import MonedaSummaryDto': 'from src.features.monedas.application.dtos import MonedaSummaryDto',
    'from src.domain.shared.dtos import CrearMonedaCommand': 'from src.features.monedas.application.dtos import CrearMonedaCommand',
    'from src.domain.shared.dtos import ActualizarMonedaCommand': 'from src.features.monedas.application.dtos import ActualizarMonedaCommand',
    
    # DTOs Tipo Documento
    'from src.domain.shared.dtos_tipo_documento import TipoDocumentoDto': 'from src.features.tipos_documento.application.dtos import TipoDocumentoDto',
    'from src.domain.shared.dtos_tipo_documento import TipoDocumentoSummaryDto': 'from src.features.tipos_documento.application.dtos import TipoDocumentoSummaryDto',
    'from src.domain.shared.dtos_tipo_documento import CrearTipoDocumentoCommand': 'from src.features.tipos_documento.application.dtos import CrearTipoDocumentoCommand',
    'from src.domain.shared.dtos_tipo_documento import ActualizarTipoDocumentoCommand': 'from src.features.tipos_documento.application.dtos import ActualizarTipoDocumentoCommand',
    
    # Casos de uso
    'from src.domain.shared.use_cases import ObtenerMonedaUseCase': 'from src.features.monedas.application.use_cases import ObtenerMonedaUseCase',
    'from src.domain.shared.use_cases import ObtenerMonedaPorCodigoUseCase': 'from src.features.monedas.application.use_cases import ObtenerMonedaPorCodigoUseCase',
    'from src.domain.shared.use_cases import ListarMonedasUseCase': 'from src.features.monedas.application.use_cases import ListarMonedasUseCase',
    'from src.domain.shared.use_cases import CrearMonedaUseCase': 'from src.features.monedas.application.use_cases import CrearMonedaUseCase',
    'from src.domain.shared.use_cases import ActualizarMonedaUseCase': 'from src.features.monedas.application.use_cases import ActualizarMonedaUseCase',
    'from src.domain.shared.use_cases import EliminarMonedaUseCase': 'from src.features.monedas.application.use_cases import EliminarMonedaUseCase',
    
    # Casos de uso Tipo Documento
    'from src.domain.shared.use_cases_tipo_documento import ObtenerTipoDocumentoUseCase': 'from src.features.tipos_documento.application.use_cases import ObtenerTipoDocumentoUseCase',
    'from src.domain.shared.use_cases_tipo_documento import ObtenerTipoDocumentoPorCodigoUseCase': 'from src.features.tipos_documento.application.use_cases import ObtenerTipoDocumentoPorCodigoUseCase',
    'from src.domain.shared.use_cases_tipo_documento import ObtenerTipoDocumentoDefaultUseCase': 'from src.features.tipos_documento.application.use_cases import ObtenerTipoDocumentoDefaultUseCase',
    'from src.domain.shared.use_cases_tipo_documento import ListarTiposDocumentoUseCase': 'from src.features.tipos_documento.application.use_cases import ListarTiposDocumentoUseCase',
    'from src.domain.shared.use_cases_tipo_documento import CrearTipoDocumentoUseCase': 'from src.features.tipos_documento.application.use_cases import CrearTipoDocumentoUseCase',
    'from src.domain.shared.use_cases_tipo_documento import ActualizarTipoDocumentoUseCase': 'from src.features.tipos_documento.application.use_cases import ActualizarTipoDocumentoUseCase',
    'from src.domain.shared.use_cases_tipo_documento import EliminarTipoDocumentoUseCase': 'from src.features.tipos_documento.application.use_cases import EliminarTipoDocumentoUseCase',
    
    # Modelos
    'from src.infrastructure.database.models import Moneda': 'from src.features.monedas.infrastructure.models import Moneda',
    'from src.infrastructure.database.models import TipoDocumento': 'from src.features.tipos_documento.infrastructure.models import TipoDocumento',
}

# Patrones para detectar importaciones con múltiples elementos
MULTI_IMPORT_PATTERNS = [
    (r'from src\.domain\.shared\.entities import ([^\n]+)', {
        'Moneda': 'src.features.monedas.domain.entities',
        'TipoDocumento': 'src.features.tipos_documento.domain.entities'
    }),
    (r'from src\.domain\.shared\.dtos import ([^\n]+)', {
        'MonedaDto': 'src.features.monedas.application.dtos',
        'MonedaSummaryDto': 'src.features.monedas.application.dtos',
        'CrearMonedaCommand': 'src.features.monedas.application.dtos',
        'ActualizarMonedaCommand': 'src.features.monedas.application.dtos'
    }),
    (r'from src\.domain\.shared\.dtos_tipo_documento import ([^\n]+)', {
        'TipoDocumentoDto': 'src.features.tipos_documento.application.dtos',
        'TipoDocumentoSummaryDto': 'src.features.tipos_documento.application.dtos',
        'CrearTipoDocumentoCommand': 'src.features.tipos_documento.application.dtos',
        'ActualizarTipoDocumentoCommand': 'src.features.tipos_documento.application.dtos'
    }),
    (r'from src\.domain\.shared\.use_cases import ([^\n]+)', {
        'ObtenerMonedaUseCase': 'src.features.monedas.application.use_cases',
        'ObtenerMonedaPorCodigoUseCase': 'src.features.monedas.application.use_cases',
        'ListarMonedasUseCase': 'src.features.monedas.application.use_cases',
        'CrearMonedaUseCase': 'src.features.monedas.application.use_cases',
        'ActualizarMonedaUseCase': 'src.features.monedas.application.use_cases',
        'EliminarMonedaUseCase': 'src.features.monedas.application.use_cases'
    }),
    (r'from src\.domain\.shared\.use_cases_tipo_documento import ([^\n]+)', {
        'ObtenerTipoDocumentoUseCase': 'src.features.tipos_documento.application.use_cases',
        'ObtenerTipoDocumentoPorCodigoUseCase': 'src.features.tipos_documento.application.use_cases',
        'ObtenerTipoDocumentoDefaultUseCase': 'src.features.tipos_documento.application.use_cases',
        'ListarTiposDocumentoUseCase': 'src.features.tipos_documento.application.use_cases',
        'CrearTipoDocumentoUseCase': 'src.features.tipos_documento.application.use_cases',
        'ActualizarTipoDocumentoUseCase': 'src.features.tipos_documento.application.use_cases',
        'EliminarTipoDocumentoUseCase': 'src.features.tipos_documento.application.use_cases'
    }),
    (r'from src\.infrastructure\.database\.models import ([^\n]+)', {
        'Moneda': 'src.features.monedas.infrastructure.models',
        'TipoDocumento': 'src.features.tipos_documento.infrastructure.models'
    }),
]

# Archivos de compatibilidad que queremos eliminar
LEGACY_FILES = [
    'src/domain/shared/entities.py',
    'src/domain/shared/dtos.py',
    'src/domain/shared/dtos_tipo_documento.py',
    'src/domain/shared/use_cases.py',
    'src/domain/shared/use_cases_tipo_documento.py',
    'src/infrastructure/database/models.py',
]


def find_python_files(directory: str) -> List[str]:
    """Encuentra todos los archivos Python en el directorio dado."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def update_imports_in_file(file_path: str, dry_run: bool = True) -> List[Tuple[str, str]]:
    """Actualiza las importaciones en un archivo.
    
    Args:
        file_path: Ruta al archivo a actualizar.
        dry_run: Si es True, no se realizan cambios en el archivo.
        
    Returns:
        Lista de tuplas (importación antigua, importación nueva) que se actualizaron.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    updated_imports = []
    
    # Actualizar importaciones directas
    for old_import, new_import in IMPORT_MAPPINGS.items():
        if old_import in content:
            content = content.replace(old_import, new_import)
            updated_imports.append((old_import, new_import))
    
    # Actualizar importaciones múltiples
    for pattern, module_map in MULTI_IMPORT_PATTERNS:
        matches = re.findall(pattern, content)
        for match in matches:
            items = [item.strip() for item in match.split(',')]
            # Agrupar los items por el módulo al que pertenecen
            grouped_items: Dict[str, List[str]] = {}
            for item in items:
                for symbol, module in module_map.items():
                    if item == symbol or item.startswith(f"{symbol} as"):
                        if module not in grouped_items:
                            grouped_items[module] = []
                        grouped_items[module].append(item)
            
            if grouped_items:
                # Crear la nueva importación para cada grupo
                pattern_parts = pattern.split('\\')
                old_import = f"from {pattern_parts[0]}.{pattern_parts[1]}.{pattern_parts[2]} import {match}"
                new_imports = []
                for module, module_items in grouped_items.items():
                    new_imports.append(f"from {module} import {', '.join(module_items)}")
                
                # Reemplazar la importación antigua con las nuevas
                if old_import in content:
                    content = content.replace(old_import, '\n'.join(new_imports))
                    updated_imports.append((old_import, '\n'.join(new_imports)))
    
    # Escribir los cambios al archivo si no es un dry run y se realizaron cambios
    if not dry_run and content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return updated_imports


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <directorio_raíz> [--apply]")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} no es un directorio válido.")
        sys.exit(1)
    
    # Verificar si se debe aplicar los cambios o solo mostrarlos
    dry_run = "--apply" not in sys.argv
    
    python_files = find_python_files(root_dir)
    
    files_updated = 0
    imports_updated = 0
    
    for file_path in python_files:
        # Ignorar los propios archivos de compatibilidad
        if any(legacy_file in file_path for legacy_file in LEGACY_FILES):
            continue
        
        updated = update_imports_in_file(file_path, dry_run)
        if updated:
            files_updated += 1
            imports_updated += len(updated)
            print(f"\n{file_path}:")
            for old_import, new_import in updated:
                print(f"  - {old_import} -> {new_import}")
    
    print(f"\nResumen:")
    print(f"  - Archivos analizados: {len(python_files)}")
    print(f"  - Archivos actualizados: {files_updated}")
    print(f"  - Importaciones actualizadas: {imports_updated}")
    
    if dry_run:
        print("\nEste fue un dry run. Para aplicar los cambios, ejecuta el script con --apply")
    else:
        print("\nLos cambios han sido aplicados.")


if __name__ == '__main__':
    main()
