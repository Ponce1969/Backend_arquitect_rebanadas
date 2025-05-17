# Este archivo se mantiene para compatibilidad con código existente
# El router se ha movido a su propio slice

# Importamos el router desde su nueva ubicación
from src.features.monedas.infrastructure.api.v1.monedas_router import router

# Nota: Este archivo será eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente el router
# desde su nueva ubicación en el slice correspondiente.
