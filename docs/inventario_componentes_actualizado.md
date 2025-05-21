# Inventario de Componentes (Actualizado)

Este documento proporciona un inventario actualizado de todos los componentes del sistema y su ubicación actual en la arquitectura de rebanadas verticales.

## Componentes Compartidos

| Componente | Ubicación Actual | Estado |
|------------|-----------------|--------|
| Validadores | `/src/domain/shared/validators/` | ✅ Correcto |
| Excepciones | `/src/domain/shared/exceptions.py` | ✅ Correcto |
| Mappers Base | `/src/infrastructure/mappers.py` | ✅ Correcto |
| Interfaces de Repositorios | `/src/infrastructure/interfaces/repositories.py` | ✅ Correcto |
| Utilidades de Fecha/Hora | `/src/infrastructure/utils/datetime.py` | ✅ Correcto |
| Utilidades de Validación | `/src/infrastructure/utils/validation.py` | ✅ Correcto |
| Seguridad (JWT, Contraseñas) | `/src/infrastructure/security/` | ✅ Correcto |
| Configuraciones | `/src/config/settings.py` | ✅ Correcto |

## Características (Features)

Cada característica sigue la estructura de rebanadas verticales:

```
src/features/[feature]/
├── application/
│   ├── interfaces/
│   ├── use_cases.py
│   └── dtos.py
├── domain/
│   ├── entities.py
│   └── exceptions.py
└── infrastructure/
    ├── api/
    │   └── v1/
    ├── models.py
    ├── repositories.py
    └── mappers.py
```

## Archivos Eliminados

Los siguientes archivos obsoletos han sido eliminados correctamente:

| Archivo | Reemplazo |
|---------|------------|
| `/src/domain/shared/entities.py` | Entidades específicas en cada característica |
| `/src/domain/shared/dtos.py` | DTOs específicos en cada característica |
| `/src/domain/shared/dtos_tipo_documento.py` | DTOs específicos en cada característica |
| `/src/domain/shared/use_cases.py` | Casos de uso específicos en cada característica |
| `/src/domain/shared/use_cases_tipo_documento.py` | Casos de uso específicos en cada característica |
| `/src/infrastructure/database/models.py` | Modelos específicos en cada característica |
| Carpeta `/src/features/shared` | Componentes migrados a ubicaciones correctas |

## Código Duplicado Eliminado

Se han eliminado las siguientes duplicaciones de código:

| Función | Ubicaciones Antiguas | Ubicación Actual |
|------------|----------------------|-----------------|
| `get_utc_now()` | Múltiples archivos de modelos | `/src/infrastructure/utils/datetime.py` |

## Configuración Centralizada

Se ha centralizado la configuración de variables de entorno en un único archivo `.env` en la raíz del proyecto que contiene:

1. **Configuración de PostgreSQL**: Credenciales y conexión
2. **Configuración de FastAPI**: Nombre, CORS, prefijo de API
3. **Configuración de seguridad**: Tokens y encriptación
4. **Configuración de email**: Servidor SMTP y credenciales
5. **Credenciales de administrador**: Datos iniciales y login

## Seguridad Mejorada

Se ha migrado el sistema de hashing de contraseñas de bcrypt a Argon2:

| Componente | Estado |
|------------|--------|
| Implementación de Argon2 | ✅ Completado |
| Compatibilidad con hashes bcrypt existentes | ✅ Completado |
| Migración automática de hashes bcrypt a Argon2 | ✅ Completado |
