# Este archivo se mantiene para compatibilidad con código existente
# Las definiciones de modelos se han movido a sus respectivos slices

# Importamos los modelos desde sus nuevas ubicaciones
from src.features.monedas.infrastructure.models import Moneda
from src.features.tipos_documento.infrastructure.models import TipoDocumento

# Importamos las entidades de dominio desde sus nuevas ubicaciones
from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.tipos_documento.domain.entities import TipoDocumento as TipoDocumentoEntity

# Nota: Este archivo será eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente los modelos
# desde sus nuevas ubicaciones en los slices correspondientes.