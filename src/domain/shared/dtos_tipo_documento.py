import warnings

# Emitir una advertencia de que este archivo está obsoleto
warnings.warn(
    "El archivo 'src/domain/shared/dtos_tipo_documento.py' está obsoleto y será eliminado en futuras versiones. "\
    "Por favor, actualice sus importaciones para usar directamente los DTOs desde sus nuevas ubicaciones.",
    DeprecationWarning, stacklevel=2
)

# Este archivo se mantiene para compatibilidad con código existente
# Las definiciones de DTOs se han movido a sus respectivos slices

# Importamos los DTOs desde sus nuevas ubicaciones
from src.features.tipos_documento.application.dtos import (
    TipoDocumentoDto,
    TipoDocumentoSummaryDto,
    CrearTipoDocumentoCommand,
    ActualizarTipoDocumentoCommand
)

# Nota: Este archivo será eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente los DTOs
# desde sus nuevas ubicaciones en los slices correspondientes.
