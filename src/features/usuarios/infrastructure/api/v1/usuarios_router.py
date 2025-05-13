from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.features.usuarios.application.dtos import (
    ActualizarUsuarioCommand,
    CambiarContrasenaCommand,
    LoginCommand,
    RegistroUsuarioCommand,
    TokenDto,
    UsuarioDto,
)
from src.features.usuarios.application.use_cases import (
    ActualizarUsuarioUseCase,
    AutenticarUsuarioUseCase,
    CambiarContrasenaUseCase,
    EliminarUsuarioUseCase,
    ListarUsuariosPorCorredorUseCase,
    ListarUsuariosUseCase,
    ObtenerUsuarioUseCase,
    RegistrarUsuarioUseCase,
)
from src.features.usuarios.infrastructure.repositories import SQLAlchemyUsuarioRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.jwt import create_access_token
from src.infrastructure.security.password import PasswordHelper

# Configuración del router
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# Configuración de seguridad OAuth2
# La URL debe ser relativa a /api/v1/usuarios, que es el prefijo del router
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/usuarios/login")


# Dependencia para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from src.infrastructure.security.jwt import decode_access_token
    
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
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes para realizar esta acción"
        )
    return current_user


@router.post("/", response_model=UsuarioDto, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    command: RegistroUsuarioCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)
):
    """Registra un nuevo usuario (solo administradores)."""
    try:
        repository = SQLAlchemyUsuarioRepository(db)
        password_helper = PasswordHelper()
        use_case = RegistrarUsuarioUseCase(repository, password_helper)
        return use_case.execute(command)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=list[UsuarioDto])
async def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)
):
    """Lista todos los usuarios (solo administradores)."""
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = ListarUsuariosUseCase(repository)
    return use_case.execute()


@router.get("/corredor/{corredor_numero}", response_model=list[UsuarioDto])
async def listar_usuarios_por_corredor(
    corredor_numero: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)
):
    """Lista usuarios asociados a un corredor (solo administradores)."""
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = ListarUsuariosPorCorredorUseCase(repository)
    return use_case.execute(corredor_numero)


@router.get("/me", response_model=UsuarioDto)
async def obtener_usuario_actual(current_user: UsuarioDto = Depends(get_current_user)):
    """Obtiene la información del usuario autenticado."""
    return current_user


@router.get("/{usuario_id}", response_model=Optional[UsuarioDto])
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)
):
    """Obtiene un usuario por su ID (solo administradores)."""
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = ObtenerUsuarioUseCase(repository)
    usuario = use_case.execute(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return usuario


@router.put("/{usuario_id}", response_model=Optional[UsuarioDto])
async def actualizar_usuario(
    usuario_id: int,
    command: ActualizarUsuarioCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)
):
    """Actualiza un usuario existente (solo administradores)."""
    try:
        repository = SQLAlchemyUsuarioRepository(db)
        use_case = ActualizarUsuarioUseCase(repository)
        usuario = use_case.execute(usuario_id, command)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)
):
    """Elimina un usuario (solo administradores)."""
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = EliminarUsuarioUseCase(repository)
    result = use_case.execute(usuario_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return None


@router.post("/cambiar-contrasena", status_code=status.HTTP_200_OK)
async def cambiar_contrasena(
    command: CambiarContrasenaCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)
):
    """Cambia la contraseña del usuario."""
    # Solo permitir cambiar la propia contraseña o ser administrador
    if current_user.id != command.usuario_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para cambiar la contraseña de otro usuario"
        )
    
    try:
        repository = SQLAlchemyUsuarioRepository(db)
        password_helper = PasswordHelper()
        use_case = CambiarContrasenaUseCase(repository, password_helper)
        result = use_case.execute(command)
        if result:
            return {"message": "Contraseña actualizada correctamente"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenDto)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token JWT."""
    repository = SQLAlchemyUsuarioRepository(db)
    password_helper = PasswordHelper()
    use_case = AutenticarUsuarioUseCase(repository, password_helper)
    
    usuario = use_case.execute(LoginCommand(
        username=form_data.username,
        password=form_data.password
    ))
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(usuario.id)},
        expires_delta=access_token_expires
    )
    
    return TokenDto(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        usuario=usuario
    )
