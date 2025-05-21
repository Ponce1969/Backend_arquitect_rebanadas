# Este archivo se mantiene para compatibilidad con cu00f3digo existente
# Las definiciones de DTOs se han movido a sus respectivos slices

# Importamos los DTOs desde sus nuevas ubicaciones
from src.features.tipos_documento.application.dtos import (
    TipoDocumentoDto,
    TipoDocumentoSummaryDto,
    CrearTipoDocumentoCommand,
    ActualizarTipoDocumentoCommand
)

# Nota: Este archivo seru00e1 eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente los DTOs
# desde sus nuevas ubicaciones en los slices correspondientes.
