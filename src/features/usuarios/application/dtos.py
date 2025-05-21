from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator

# Importamos las clases base y utilidades
from src.core.domain.base_dto import AuditableDto, validar_contrasena_segura, validar_porcentaje, validar_telefono

# Importamos el Enum de Roles
from src.features.usuarios.domain.types import Role


# DTO para el registro de usuario (entrada a RegistrarUsuarioUseCase)
class RegistroUsuarioCommand(AuditableDto):
    """DTO para el registro de un nuevo usuario.
    
    Atributos:
        nombre: Nombre del usuario (1-64 caracteres)
        apellido: Apellido del usuario (1-64 caracteres)
        email: Correo electrónico del usuario (único)
        username: Nombre de usuario (único, 3-64 caracteres)
        password: Contraseña (mínimo 8 caracteres, debe incluir mayúsculas, minúsculas, números y caracteres especiales)
        is_active: Indica si el usuario está activo
        is_superuser: Indica si el usuario es superusuario
        role: Rol del usuario (corredor, admin, etc.)
        corredor_numero: Número de corredor asociado (requerido si el rol es CORREDOR)
        comision_porcentaje: Porcentaje de comisión (0-100)
        telefono: Número de teléfono (8-15 dígitos, opcional)
    """
    nombre: str = Field(..., min_length=1, max_length=64, description="Nombre del usuario")
    apellido: str = Field(..., min_length=1, max_length=64, description="Apellido del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    username: str = Field(..., min_length=3, max_length=64, description="Nombre de usuario único")
    password: str = Field(..., min_length=8, description="Contraseña del usuario")
    is_active: bool = Field(True, description="Indica si el usuario está activo")
    is_superuser: bool = Field(False, description="Indica si el usuario es superusuario")
    role: Role = Field(Role.CORREDOR, description="Rol del usuario en el sistema")
    corredor_numero: int | None = Field(
        None, 
        description="Número de corredor asociado (requerido si el rol es CORREDOR)"
    )
    comision_porcentaje: float | None = Field(
        0.0, 
        ge=0, 
        le=100, 
        description="Porcentaje de comisión (0-100)"
    )
    telefono: str | None = Field(
        None, 
        max_length=20, 
        description="Número de teléfono de contacto"
    )

    # Validaciones personalizadas
    @field_validator('role', 'corredor_numero')
    @classmethod
    def validate_role_corredor(cls, v, values, **kwargs):
        """Valida que los corredores tengan un número de corredor asociado."""
        field_name = kwargs.get('field').name
        
        # Si el campo es 'role' y es CORREDOR, verificamos que corredor_numero esté presente
        if field_name == 'role' and v == Role.CORREDOR:
            if not values.get('corredor_numero'):
                raise ValueError("Un usuario con rol CORREDOR debe tener un número de corredor asociado")
        
        # Si el campo es 'corredor_numero' y role es CORREDOR, verificamos que no sea None
        if field_name == 'corredor_numero' and values.get('role') == Role.CORREDOR:
            if v is None:
                raise ValueError("Un usuario con rol CORREDOR debe tener un número de corredor asociado")
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Valida que la contraseña cumpla con los requisitos de seguridad."""
        return validar_contrasena_segura(v)
    
    @field_validator('comision_porcentaje')
    @classmethod
    def validate_comision_porcentaje(cls, v: Optional[float]) -> Optional[float]:
        """Valida que el porcentaje de comisión esté entre 0 y 100."""
        if v is not None:
            return validar_porcentaje(v)
        return v
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono_format(cls, v: Optional[str]) -> Optional[str]:
        """Valida el formato del número de teléfono."""
        if v:
            return validar_telefono(v)
        return v


# DTO para actualizar un usuario (entrada a ActualizarUsuarioUseCase)
class ActualizarUsuarioCommand(AuditableDto):
    """DTO para actualizar un usuario existente.
    
    Atributos:
        nombre: Nombre del usuario (1-64 caracteres)
        apellido: Apellido del usuario (1-64 caracteres)
        email: Correo electrónico del usuario (único)
        username: Nombre de usuario (único, 3-64 caracteres)
        is_active: Indica si el usuario está activo
        is_superuser: Indica si el usuario es superusuario
        role: Rol del usuario (corredor, admin, etc.)
        corredor_numero: Número de corredor asociado (requerido si el rol es CORREDOR)
        comision_porcentaje: Porcentaje de comisión (0-100)
        telefono: Número de teléfono (8-15 dígitos, opcional)
    """
    nombre: str | None = Field(None, min_length=1, max_length=64, description="Nombre del usuario")
    apellido: str | None = Field(None, min_length=1, max_length=64, description="Apellido del usuario")
    email: EmailStr | None = Field(None, description="Correo electrónico del usuario")
    username: str | None = Field(None, min_length=3, max_length=64, description="Nombre de usuario único")
    is_active: bool | None = Field(None, description="Indica si el usuario está activo")
    is_superuser: bool | None = Field(None, description="Indica si el usuario es superusuario")
    role: Role | None = Field(None, description="Rol del usuario en el sistema")
    corredor_numero: int | None = Field(
        None, 
        description="Número de corredor asociado (requerido si el rol es CORREDOR)"
    )
    comision_porcentaje: float | None = Field(
        None, 
        ge=0, 
        le=100, 
        description="Porcentaje de comisión (0-100)"
    )
    telefono: str | None = Field(
        None, 
        max_length=20, 
        description="Número de teléfono de contacto"
    )

    # Validaciones personalizadas
    @field_validator('comision_porcentaje')
    @classmethod
    def validate_comision_porcentaje(cls, v: Optional[float]) -> Optional[float]:
        """Valida que el porcentaje de comisión esté entre 0 y 100."""
        if v is not None:
            return validar_porcentaje(v)
        return v
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono_format(cls, v: Optional[str]) -> Optional[str]:
        """Valida el formato del número de teléfono."""
        if v:
            return validar_telefono(v)
        return v


# DTO para cambiar la contraseña (entrada a CambiarContrasenaUseCase)
class CambiarContrasenaCommand(AuditableDto):
    """DTO para cambiar la contraseña de un usuario.
    
    Atributos:
        usuario_id: ID del usuario que desea cambiar su contraseña
        contrasena_actual: Contraseña actual del usuario
        nueva_contrasena: Nueva contraseña (debe cumplir con los requisitos de seguridad)
    """
    usuario_id: int = Field(..., description="ID del usuario")
    contrasena_actual: str = Field(..., description="Contraseña actual del usuario")
    nueva_contrasena: str = Field(
        ..., 
        min_length=8, 
        description="Nueva contraseña del usuario"
    )
    
    @field_validator('nueva_contrasena')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Valida que la nueva contraseña cumpla con los requisitos de seguridad."""
        return validar_contrasena_segura(v)


# DTO para representar un Usuario (salida de Use Cases y API)
class UsuarioDto(AuditableDto):
    """DTO para representar un usuario en las respuestas de la API.
    
    Atributos:
        id: Identificador único del usuario
        nombre: Nombre del usuario
        apellido: Apellido del usuario
        email: Correo electrónico del usuario
        username: Nombre de usuario
        is_active: Indica si el usuario está activo
        is_superuser: Indica si el usuario es superusuario
        role: Rol del usuario en el sistema
        corredor_numero: Número de corredor asociado (si aplica)
        comision_porcentaje: Porcentaje de comisión (si aplica)
        telefono: Número de teléfono de contacto
        fecha_creacion: Fecha de creación del usuario
        fecha_actualizacion: Fecha de la última actualización del usuario
    """
    id: int = Field(..., description="Identificador único del usuario")
    nombre: str = Field(..., description="Nombre del usuario")
    apellido: str = Field(..., description="Apellido del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    username: str = Field(..., description="Nombre de usuario")
    is_active: bool = Field(..., description="Indica si el usuario está activo")
    is_superuser: bool = Field(..., description="Indica si el usuario es superusuario")
    role: Role = Field(..., description="Rol del usuario en el sistema")
    corredor_numero: int | None = Field(
        None, 
        description="Número de corredor asociado (si aplica)"
    )
    comision_porcentaje: float | None = Field(
        None, 
        description="Porcentaje de comisión (si aplica)"
    )
    telefono: str | None = Field(
        None, 
        description="Número de teléfono de contacto"
    )
    
    # Sobrescribimos el nombre del campo para mantener compatibilidad
    fecha_actualizacion: datetime = Field(..., alias="fecha_modificacion")
    
    class Config(AuditableDto.Config):
        # Configuración adicional específica de UsuarioDto
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@ejemplo.com",
                "username": "jperez",
                "is_active": True,
                "is_superuser": False,
                "role": "corredor",
                "corredor_numero": 123,
                "comision_porcentaje": 10.5,
                "telefono": "+541112345678",
                "fecha_creacion": "2025-01-01T00:00:00",
                "fecha_modificacion": "2025-01-01T00:00:00"
            }
        }


# DTO para la autenticación (entrada a AutenticarUsuarioUseCase)
class LoginCommand(AuditableDto):
    """DTO para el inicio de sesión de un usuario.
    
    Atributos:
        username: Nombre de usuario
        password: Contraseña del usuario
    """
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña del usuario")


# DTO para el token de autenticación (salida de AutenticarUsuarioUseCase/API)
class TokenDto(AuditableDto):
    """DTO para la respuesta de autenticación.
    
    Atributos:
        access_token: Token de acceso JWT
        token_type: Tipo de token (siempre "bearer")
        expires_in: Tiempo de expiración en segundos
        usuario: Información básica del usuario autenticado
    """
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field("bearer", description="Tipo de token (siempre 'bearer')")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    usuario: UsuarioDto = Field(..., description="Información del usuario autenticado")
    
    class Config(AuditableDto.Config):
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "usuario": {
                    "id": 1,
                    "nombre": "Juan",
                    "apellido": "Pérez",
                    "email": "juan.perez@ejemplo.com",
                    "username": "jperez",
                    "is_active": True,
                    "is_superuser": False,
                    "role": "corredor",
                    "corredor_numero": 123,
                    "comision_porcentaje": 10.5,
                    "telefono": "+541112345678",
                    "fecha_creacion": "2025-01-01T00:00:00",
                    "fecha_modificacion": "2025-01-01T00:00:00"
                }
            }
        }
