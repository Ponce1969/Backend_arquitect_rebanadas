# Guía de Migración a Arquitectura de Rebanadas Verticales

## Introducción

Este documento describe el proceso de migración de la arquitectura monolítica original a una arquitectura de rebanadas verticales (vertical slicing) en el proyecto API Seguros. La migración se está realizando de forma gradual para minimizar el impacto en el código existente.

## Archivos de Compatibilidad

Durante la transición, se han creado archivos de compatibilidad que re-exportan entidades, DTOs, casos de uso y modelos desde sus nuevas ubicaciones. Estos archivos están marcados como obsoletos y serán eliminados en futuras versiones.

Los archivos de compatibilidad son:

- `src/domain/shared/entities.py`
- `src/domain/shared/dtos.py`
- `src/domain/shared/dtos_tipo_documento.py`
- `src/domain/shared/use_cases.py`
- `src/domain/shared/use_cases_tipo_documento.py`
- `src/infrastructure/database/models.py`

## Cómo Actualizar las Importaciones

Para preparar tu código para la eliminación de los archivos de compatibilidad, debes actualizar las importaciones siguiendo estas reglas:

### Entidades

```python
# Antes
from src.domain.shared.entities import Moneda
from src.domain.shared.entities import TipoDocumento

# Despues
from src.features.monedas.domain.entities import Moneda
from src.features.tipos_documento.domain.entities import TipoDocumento
```

### DTOs

```python
# Antes
from src.domain.shared.dtos import MonedaDto, MonedaSummaryDto, CrearMonedaCommand, ActualizarMonedaCommand

# Despues
from src.features.monedas.application.dtos import MonedaDto, MonedaSummaryDto, CrearMonedaCommand, ActualizarMonedaCommand
```

```python
# Antes
from src.domain.shared.dtos_tipo_documento import TipoDocumentoDto, TipoDocumentoSummaryDto, CrearTipoDocumentoCommand, ActualizarTipoDocumentoCommand

# Despues
from src.features.tipos_documento.application.dtos import TipoDocumentoDto, TipoDocumentoSummaryDto, CrearTipoDocumentoCommand, ActualizarTipoDocumentoCommand
```

### Casos de Uso

```python
# Antes
from src.domain.shared.use_cases import ObtenerMonedaUseCase, ListarMonedasUseCase, CrearMonedaUseCase, ActualizarMonedaUseCase, EliminarMonedaUseCase

# Despues
from src.features.monedas.application.use_cases import ObtenerMonedaUseCase, ListarMonedasUseCase, CrearMonedaUseCase, ActualizarMonedaUseCase, EliminarMonedaUseCase
```

```python
# Antes
from src.domain.shared.use_cases_tipo_documento import ObtenerTipoDocumentoUseCase, ListarTiposDocumentoUseCase, CrearTipoDocumentoUseCase, ActualizarTipoDocumentoUseCase, EliminarTipoDocumentoUseCase

# Despues
from src.features.tipos_documento.application.use_cases import ObtenerTipoDocumentoUseCase, ListarTiposDocumentoUseCase, CrearTipoDocumentoUseCase, ActualizarTipoDocumentoUseCase, EliminarTipoDocumentoUseCase
```

### Modelos

```python
# Antes
from src.infrastructure.database.models import Moneda, TipoDocumento

# Despues
from src.features.monedas.infrastructure.models import Moneda
from src.features.tipos_documento.infrastructure.models import TipoDocumento
```

## Herramientas de Ayuda

Se han creado dos scripts para ayudar en el proceso de migración:

1. `scripts/utils/find_legacy_imports.py`: Este script analiza el código fuente para encontrar importaciones de los archivos de compatibilidad y sugiere cómo actualizarlas.

   Uso:
   ```bash
   python scripts/utils/find_legacy_imports.py src
   ```

2. `scripts/utils/test_deprecation_warnings.py`: Este script prueba las advertencias de deprecación en los archivos de compatibilidad.

   Uso:
   ```bash
   python scripts/utils/test_deprecation_warnings.py
   ```

## Estructura de la Nueva Arquitectura

La nueva arquitectura sigue el patrón de rebanadas verticales, donde cada característica (feature) tiene su propia estructura completa:

```
src/
  features/
    monedas/
      domain/
        entities.py
        exceptions.py
        types.py
      application/
        dtos.py
        use_cases.py
        interfaces/
          repositories.py
      infrastructure/
        models.py
        repositories.py
        api/
          v1/
            monedas_router.py
    tipos_documento/
      domain/
        entities.py
        exceptions.py
      application/
        dtos.py
        use_cases.py
        interfaces/
          repositories.py
      infrastructure/
        models.py
        repositories.py
        api/
          v1/
            tipos_documento_router.py
```

## Cronograma de Eliminación

### Fase 1: Advertencias de Deprecación (Actual)

Los archivos de compatibilidad se mantienen con advertencias de deprecación para alertar a los desarrolladores sobre la necesidad de actualizar sus importaciones.

### Fase 2: Resolución de Dependencias Circulares

Antes de eliminar los archivos de compatibilidad, es necesario resolver las dependencias circulares entre modelos, especialmente entre `Cliente` y `TipoDocumento`. Esto puede requerir cambios en la estructura de los modelos o en la forma en que se definen las relaciones.

### Fase 3: Eliminación Final

Una vez que todas las pruebas pasen correctamente y se hayan resuelto las dependencias circulares, los archivos de compatibilidad serán eliminados en la próxima versión mayor del proyecto.

Se recomienda actualizar todas las importaciones lo antes posible para evitar problemas cuando estos archivos sean eliminados.

## Contacto

Si tienes alguna pregunta o problema durante el proceso de migración, por favor contacta al equipo de desarrollo.
