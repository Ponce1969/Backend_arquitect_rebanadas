from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from src.features.usuarios.domain.entities import Usuario as UsuarioEntity
from src.features.usuarios.application.use_cases import ObtenerUsuarioUseCase
from src.features.usuarios.infrastructure.repositories import SQLAlchemyUsuarioRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.jwt import decode_access_token

# Configuración de seguridad OAuth2
# La URL debe ser relativa a la raíz de la API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/usuarios/login")


def get_usuario_repository(db: Session = Depends(get_db)) -> SQLAlchemyUsuarioRepository:
    """Obtiene una instancia del repositorio de usuarios."""
    return SQLAlchemyUsuarioRepository(db)


def get_obtener_usuario_use_case(
    repository: SQLAlchemyUsuarioRepository = Depends(get_usuario_repository)
) -> ObtenerUsuarioUseCase:
    """Obtiene una instancia del caso de uso para obtener un usuario."""
    return ObtenerUsuarioUseCase(repository)


# Dependencia para obtener el usuario actual
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    use_case: ObtenerUsuarioUseCase = Depends(get_obtener_usuario_use_case)
) -> UsuarioEntity:
    """
    Verifica el token JWT y devuelve el usuario autenticado.
    Esta dependencia se usa para proteger endpoints que requieren autenticación.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        if not payload:
            raise credentials_exception
            
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
            
        # Obtener el usuario por su nombre de usuario
        usuario = use_case.repository.get_by_username(username)
        if not usuario:
            raise credentials_exception
            
        return usuario
        
    except Exception as e:
        print(f"Error al obtener el usuario actual: {str(e)}")
        raise credentials_exception


# Dependencia para verificar si el usuario es superusuario
async def get_admin_user(
    current_user: UsuarioEntity = Depends(get_current_user)
) -> UsuarioEntity:
    """
    Verifica que el usuario autenticado sea un administrador.
    Esta dependencia se usa para proteger endpoints que requieren permisos de administrador.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos suficientes para realizar esta acción"
        )
    return current_user


# Dependencia para verificar si el usuario es un corredor
async def get_corredor_user(
    current_user: UsuarioEntity = Depends(get_current_user)
) -> UsuarioEntity:
    """
    Verifica que el usuario autenticado tenga rol de corredor.
    Esta dependencia se usa para proteger endpoints que requieren permisos de corredor.
    """
    if current_user.role != "corredor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de corredor para acceder a este recurso"
        )
    return current_user
