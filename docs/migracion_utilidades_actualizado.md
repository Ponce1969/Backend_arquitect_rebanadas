# Migración de Utilidades Comunes (Actualizado)

## Objetivo

Centralizar las utilidades comunes que estaban duplicadas en diferentes partes del código en las ubicaciones correctas siguiendo la arquitectura de rebanadas verticales.

## Utilidades Migradas

### 1. Utilidades de Fecha y Hora (✅ Completado)

- **Función `get_utc_now()`**: Se ha migrado de múltiples implementaciones duplicadas a una única implementación centralizada.
- **Ubicación actual**: `src/infrastructure/utils/datetime.py`
- **Archivos actualizados**:
  - `/src/features/monedas/infrastructure/models.py`
  - `/src/features/clientes/infrastructure/models.py`
  - `/src/features/tipos_seguros/infrastructure/models.py`
  - `/src/features/tipos_seguros/application/use_cases.py`
  - `/src/features/sustituciones_corredores/infrastructure/models.py`
  - `/src/features/aseguradoras/infrastructure/models.py`
  - `/src/features/corredores/infrastructure/models.py`
  - `/src/features/usuarios/infrastructure/models.py`

### 2. Utilidades de Validación (✅ Completado)

- **Validación de modelos Pydantic**: Se ha centralizado en un módulo compartido.
- **Ubicación actual**: `src/infrastructure/utils/validation.py`

### 3. Sistema de Seguridad de Contraseñas (✅ Completado)

- **Migración a Argon2**: Se ha actualizado el sistema para usar Argon2 en lugar de bcrypt para los nuevos hashes.
- **Compatibilidad con hashes existentes**: Se mantiene la compatibilidad con hashes bcrypt existentes.
- **Ubicación**: `src/infrastructure/security/password.py`

## Estado de la Migración

### Fase 1: Preparación (✅ Completada)

1. ✅ Crear las nuevas utilidades en `src/infrastructure/utils/`
2. ✅ Documentar las nuevas utilidades
3. ✅ Asegurarse de que las nuevas utilidades sean compatibles con el código existente

### Fase 2: Migración Gradual (✅ Completada)

1. ✅ Identificar componentes específicos para migrar
2. ✅ Actualizar componentes para usar las nuevas utilidades
3. ✅ Ejecutar pruebas para asegurar el correcto funcionamiento

### Fase 3: Deprecación (✅ Completada)

1. ✅ Agregar advertencias de obsolescencia en código legado (bcrypt)
2. ✅ Mantener compatibilidad durante el periodo de transición

### Fase 4: Eliminación (✅ Completada)

1. ✅ Eliminar las utilidades antiguas y código duplicado
2. ✅ Eliminar carpetas obsoletas (`src/features/shared`)

## Ejemplo de Uso de las Nuevas Utilidades

### Utilidades de Fecha y Hora

```python
from src.infrastructure.utils.datetime import get_utc_now, get_today, is_future_date

# Obtener la fecha y hora actual en UTC
fecha_hora_actual = get_utc_now()

# Obtener la fecha actual
fecha_actual = get_today()

# Verificar si una fecha es futura
es_futura = is_future_date(fecha)
```

### Utilidades de Validación

```python
from src.infrastructure.utils.validation import validate_model, validate_required_fields
from src.features.usuarios.application.dtos import UsuarioDTO

# Validar datos contra un modelo Pydantic
usuario = validate_model(UsuarioDTO, datos)

# Validar campos requeridos
validate_required_fields(datos, ["nombre", "email", "password"])
```

### Sistema de Contraseñas con Argon2

```python
from src.infrastructure.security.password import PasswordHelper

# Generar hash con Argon2
hashed_password = PasswordHelper.hash_password("mi_contraseña_segura")

# Verificar contraseña (funciona con hashes de Argon2 y bcrypt)
es_valida = PasswordHelper.verify_password("mi_contraseña_segura", hashed_password)
```

## Trabajos Futuros

1. **Migración automática de hashes**: ✅ Implementado un mecanismo para actualizar automáticamente los hashes bcrypt a Argon2 cuando los usuarios inicien sesión.
2. **Script de migración masiva**: Considerar la implementación de un script para migrar masivamente todas las contraseñas existentes.
3. **Eliminación completa de bcrypt**: Tras un periodo de transición, eliminar completamente el soporte para bcrypt.
