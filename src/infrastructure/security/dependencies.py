from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.features.usuarios.application.dtos import UsuarioDto
from src.features.usuarios.application.use_cases import ObtenerUsuarioUseCase
from src.features.usuarios.infrastructure.repositories import SQLAlchemyUsuarioRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.jwt import decode_access_token

# Configuración de seguridad OAuth2
# La URL debe ser relativa a la raíz de la API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/usuarios/login")


# Dependencia para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Verifica el token JWT y devuelve el usuario autenticado.
    Esta dependencia se usa para proteger endpoints que requieren autenticación.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise credentials_exception
    
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = ObtenerUsuarioUseCase(repository)
    usuario = use_case.execute(int(usuario_id))
    
    if usuario is None:
        raise credentials_exception
    
    return usuario


# Dependencia para verificar si el usuario es superusuario
async def get_admin_user(current_user: UsuarioDto = Depends(get_current_user)):
    """
    Verifica que el usuario autenticado sea un administrador.
    Esta dependencia se usa para proteger endpoints que requieren permisos de administrador.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para realizar esta acción"
        )
    return current_user


# Dependencia para verificar si el usuario es un corredor
async def get_corredor_user(current_user: UsuarioDto = Depends(get_current_user)):
    """
    Verifica que el usuario autenticado tenga rol de corredor.
    Esta dependencia se usa para proteger endpoints que requieren permisos de corredor.
    """
    if current_user.role != "corredor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta acción solo puede ser realizada por corredores"
        )
    return current_user
