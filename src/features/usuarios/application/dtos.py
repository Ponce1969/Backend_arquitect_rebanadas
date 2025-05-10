from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

# Importamos el Enum de Roles
from src.domain.shared.custom_types import Role


# DTO para el registro de usuario (entrada a RegistrarUsuarioUseCase)
class RegistroUsuarioCommand(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=64)
    apellido: str = Field(..., min_length=1, max_length=64)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=8)  # Contraseña plana en la entrada
    is_active: bool = True
    is_superuser: bool = False
    role: Role = Role.CORREDOR  # Usamos el Enum
    corredor_numero: int | None = None  # Campo para asociar si el rol es corredor
    comision_porcentaje: float | None = 0.0
    telefono: str | None = Field(None, max_length=20)

    @validator('role', 'corredor_numero')
    def validate_role_corredor(cls, v, values, **kwargs):
        # Si el campo es 'role' y es CORREDOR, verificamos que corredor_numero esté presente
        if kwargs.get('field').name == 'role' and v == Role.CORREDOR:
            if not values.get('corredor_numero'):
                raise ValueError("Un usuario con rol CORREDOR debe tener un número de corredor asociado")
        # Si el campo es 'corredor_numero' y role es CORREDOR, verificamos que no sea None
        if kwargs.get('field').name == 'corredor_numero' and values.get('role') == Role.CORREDOR:
            if v is None:
                raise ValueError("Un usuario con rol CORREDOR debe tener un número de corredor asociado")
        return v


# DTO para actualizar un usuario (entrada a ActualizarUsuarioUseCase)
class ActualizarUsuarioCommand(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=64)
    apellido: str | None = Field(None, min_length=1, max_length=64)
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=64)
    is_active: bool | None = None
    is_superuser: bool | None = None
    role: Role | None = None
    corredor_numero: int | None = None
    comision_porcentaje: float | None = None
    telefono: str | None = Field(None, max_length=20)


# DTO para cambiar la contraseña (entrada a CambiarContrasenaUseCase)
class CambiarContrasenaCommand(BaseModel):
    usuario_id: int
    contrasena_actual: str
    nueva_contrasena: str = Field(..., min_length=8)


# DTO para representar un Usuario (salida de Use Cases y API)
class UsuarioDto(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    username: str
    is_active: bool
    is_superuser: bool
    role: Role  # Retornamos el Enum
    corredor_numero: int | None = None
    comision_porcentaje: float | None = None
    telefono: str | None = None
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True  # Permite mapear desde la Entidad de Dominio


# DTO para la autenticación (entrada a AutenticarUsuarioUseCase)
class LoginCommand(BaseModel):
    username: str
    password: str  # Contraseña plana en la entrada


# DTO para el token de autenticación (salida de AutenticarUsuarioUseCase/API)
class TokenDto(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Tiempo de expiración en segundos
    usuario: UsuarioDto  # Incluimos información básica del usuario
