# Este archivo se mantiene para compatibilidad con cu00f3digo existente
# Las definiciones de casos de uso se han movido a sus respectivos slices

# Importamos los casos de uso desde sus nuevas ubicaciones
from src.features.tipos_documento.application.use_cases import (
    ObtenerTipoDocumentoUseCase,
    ObtenerTipoDocumentoPorCodigoUseCase,
    ObtenerTipoDocumentoDefaultUseCase,
    ListarTiposDocumentoUseCase,
    CrearTipoDocumentoUseCase,
    ActualizarTipoDocumentoUseCase,
    EliminarTipoDocumentoUseCase
)

# Nota: Este archivo seru00e1 eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente los casos de uso
# desde sus nuevas ubicaciones en los slices correspondientes.
