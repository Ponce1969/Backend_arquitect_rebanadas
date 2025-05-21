# Importamos las entidades desde sus respectivos slices para mantener compatibilidad
from src.features.monedas.domain.entities import Moneda
from src.features.tipos_documento.domain.entities import TipoDocumento

# Estas importaciones permiten que el cu00f3digo existente siga funcionando sin cambios
# mientras refactorizamos la arquitectura para seguir el patru00f3n de vertical slicing
