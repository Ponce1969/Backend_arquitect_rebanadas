#!/usr/bin/env python
"""
Script para encontrar todas las importaciones de los archivos de compatibilidad
y sugerir cómo actualizarlas a las nuevas ubicaciones.
"""

import os
import re
import sys
from pathlib import Path

# Mapeo de importaciones antiguas a nuevas
IMPORT_MAPPINGS = {
    # Entidades
    'from src.domain.shared.entities import Moneda': 'from src.features.monedas.domain.entities import Moneda',
    'from src.domain.shared.entities import TipoDocumento': 'from src.features.tipos_documento.domain.entities import TipoDocumento',
    
    # DTOs
    'from src.domain.shared.dtos import MonedaDto': 'from src.features.monedas.application.dtos import MonedaDto',
    'from src.domain.shared.dtos import TipoDocumentoDto': 'from src.features.tipos_documento.application.dtos import TipoDocumentoDto',
    'from src.domain.shared.dtos import TipoDocumentoSummaryDto': 'from src.features.tipos_documento.application.dtos import TipoDocumentoSummaryDto',
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
    (r'from src\.domain\.shared\.entities import ([^\n]+)', 'src.features.monedas.domain.entities', 'src.features.tipos_documento.domain.entities'),
    (r'from src\.domain\.shared\.dtos import ([^\n]+)', 'src.features.monedas.application.dtos', 'src.features.tipos_documento.application.dtos'),
    (r'from src\.domain\.shared\.dtos_tipo_documento import ([^\n]+)', 'src.features.tipos_documento.application.dtos'),
    (r'from src\.domain\.shared\.use_cases import ([^\n]+)', 'src.features.monedas.application.use_cases'),
    (r'from src\.domain\.shared\.use_cases_tipo_documento import ([^\n]+)', 'src.features.tipos_documento.application.use_cases'),
    (r'from src\.infrastructure\.database\.models import ([^\n]+)', 'src.features.monedas.infrastructure.models', 'src.features.tipos_documento.infrastructure.models'),
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


def find_python_files(directory):
    """Encuentra todos los archivos Python en el directorio dado."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def check_file_for_imports(file_path):
    """Verifica si el archivo contiene importaciones de los archivos de compatibilidad."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    found_imports = []
    
    # Buscar importaciones directas
    for old_import, new_import in IMPORT_MAPPINGS.items():
        if old_import in content:
            found_imports.append((old_import, new_import))
    
    # Buscar importaciones múltiples
    for pattern, *new_modules in MULTI_IMPORT_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                items = [item.strip() for item in match.split(',')]
                found_imports.append((f"Multiple import: {items}", f"Consider splitting into imports from {', '.join(new_modules)}"))
    
    return found_imports


def main():
    """Función principal."""
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <directorio_raiz>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} no es un directorio válido.")
        sys.exit(1)
    
    python_files = find_python_files(root_dir)
    
    files_with_imports = {}
    for file_path in python_files:
        # Ignorar los propios archivos de compatibilidad
        if any(legacy_file in file_path for legacy_file in LEGACY_FILES):
            continue
        
        imports = check_file_for_imports(file_path)
        if imports:
            files_with_imports[file_path] = imports
    
    if not files_with_imports:
        print("No se encontraron importaciones de los archivos de compatibilidad.")
        print("Es seguro eliminar los siguientes archivos:")
        for legacy_file in LEGACY_FILES:
            print(f"  - {legacy_file}")
        return
    
    print(f"Se encontraron {len(files_with_imports)} archivos con importaciones de los archivos de compatibilidad:")
    for file_path, imports in files_with_imports.items():
        print(f"\n{file_path}:")
        for old_import, new_import in imports:
            print(f"  - {old_import} -> {new_import}")
    
    print("\nPara eliminar los archivos de compatibilidad, actualiza las importaciones en los archivos mencionados.")


if __name__ == '__main__':
    main()
