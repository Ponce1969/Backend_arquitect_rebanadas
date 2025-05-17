# Este archivo se mantiene para compatibilidad con código existente
# Las definiciones de casos de uso se han movido a sus respectivos slices

# Importamos los casos de uso desde sus nuevas ubicaciones
from src.features.monedas.application.use_cases import (
    ObtenerMonedaUseCase,
    ObtenerMonedaPorCodigoUseCase,
    ListarMonedasUseCase,
    CrearMonedaUseCase,
    ActualizarMonedaUseCase,
    EliminarMonedaUseCase
)

# Nota: Este archivo será eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente los casos de uso
# desde sus nuevas ubicaciones en los slices correspondientes.
