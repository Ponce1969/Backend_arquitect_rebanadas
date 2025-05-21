from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
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
from src.features.usuarios.domain.entities import Usuario as UsuarioEntity
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
from src.features.usuarios.domain.services.autenticacion_service import AutenticacionService
from src.features.usuarios.infrastructure.repositories import SQLAlchemyUsuarioRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.infrastructure.security.jwt import create_access_token
from src.infrastructure.security.password import Argon2PasswordHelper as PasswordHelper

# Configuración de bloqueo de cuentas
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME_MINUTES = 30

# Configuración del router
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# Configuración de autenticación OAuth2 para Swagger
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login",
    scheme_name="JWT"
)

@router.post("/", response_model=UsuarioDto, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    command: RegistroUsuarioCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioEntity = Depends(get_admin_user)
) -> UsuarioDto:
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
    current_user: UsuarioEntity = Depends(get_admin_user)
) -> List[UsuarioDto]:
    """Lista todos los usuarios (solo administradores)."""
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = ListarUsuariosUseCase(repository)
    return use_case.execute()


@router.get("/corredor/{corredor_numero}", response_model=list[UsuarioDto])
async def listar_usuarios_por_corredor(
    corredor_numero: int,
    db: Session = Depends(get_db),
    current_user: UsuarioEntity = Depends(get_admin_user)
) -> List[UsuarioDto]:
    """Lista usuarios asociados a un corredor (solo administradores)."""
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = ListarUsuariosPorCorredorUseCase(repository)
    return use_case.execute(corredor_numero)


@router.get("/me", response_model=UsuarioDto)
async def obtener_usuario_actual(current_user: UsuarioEntity = Depends(get_current_user)) -> UsuarioDto:
    """Obtiene la información del usuario autenticado."""
    # Convertir la entidad de dominio a DTO
    from src.features.usuarios.application.dtos import UsuarioDto
    return UsuarioDto.from_orm(current_user)


@router.get("/{usuario_id}", response_model=Optional[UsuarioDto])
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioEntity = Depends(get_admin_user)
) -> UsuarioDto:
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
    current_user: UsuarioEntity = Depends(get_admin_user)
) -> UsuarioDto:
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
    current_user: UsuarioEntity = Depends(get_admin_user)
):
    """
    Elimina un usuario (solo administradores).
    
    Devuelve 204 No Content si se eliminó correctamente.
    Devuelve 404 Not Found si el usuario no existe.
    """
    repository = SQLAlchemyUsuarioRepository(db)
    use_case = EliminarUsuarioUseCase(repository)
    result = use_case.execute(usuario_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    # No devolvemos nada ya que usamos status_code=204


@router.post("/cambiar-contrasena", status_code=status.HTTP_200_OK)
async def cambiar_contrasena(
    command: CambiarContrasenaCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioEntity = Depends(get_current_user)
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


@router.post("/login", response_model=TokenDto, include_in_schema=True)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> TokenDto:
    """
    Autentica un usuario y devuelve un token JWT.
    
    Implementa bloqueo de cuenta después de múltiples intentos fallidos.
    """
    try:
        # Obtener la dirección IP del cliente
        client_host = request.client.host if request.client else "unknown"
        
        # Registrar el intento de inicio de sesión
        print(f"Intento de inicio de sesión para usuario: {form_data.username} desde IP: {client_host}")
        
        # Crear el repositorio y el servicio de autenticación
        repository = SQLAlchemyUsuarioRepository(db)
        autenticacion_service = AutenticacionService(repository)
        
        # Verificar si la cuenta está bloqueada
        usuario = repository.get_by_username(form_data.username)
        if usuario and usuario.bloqueado_hasta and usuario.bloqueado_hasta > datetime.utcnow():
            tiempo_restante = usuario.bloqueado_hasta - datetime.utcnow()
            minutos_restantes = int(tiempo_restante.total_seconds() // 60)
            segundos_restantes = int(tiempo_restante.total_seconds() % 60)
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cuenta bloqueada temporalmente. Intente de nuevo en {minutos_restantes} minutos y {segundos_restantes} segundos."
            )
        
        # Autenticar al usuario
        use_case = AutenticarUsuarioUseCase(repository, autenticacion_service)
        usuario_autenticado, mensaje_error = use_case.execute(
            LoginCommand(
                username=form_data.username,
                password=form_data.password
            )
        )
        
        if not usuario_autenticado:
            # Incrementar el contador de intentos fallidos
            if usuario:
                usuario.intentos_fallidos += 1
                usuario.ultimo_intento_fallido = datetime.utcnow()
                
                # Bloquear la cuenta si se supera el número máximo de intentos
                if usuario.intentos_fallidos >= MAX_LOGIN_ATTEMPTS:
                    usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=LOCKOUT_TIME_MINUTES)
                    db.commit()
                    
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Demasiados intentos fallidos. Cuenta bloqueada por {LOCKOUT_TIME_MINUTES} minutos.",
                        headers={"WWW-Authenticate": "Bearer"}
                    )
                
                db.commit()
            
            # Devolver error de autenticación
            print(f"Error en el inicio de sesión para {form_data.username} desde {client_host}: {mensaje_error}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Si la autenticación fue exitosa, reiniciar los contadores
        if usuario:
            usuario.intentos_fallidos = 0
            usuario.ultimo_intento_fallido = None
            usuario.bloqueado_hasta = None
            db.commit()
        
        # Crear el token de acceso
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": usuario_autenticado.username, "user_id": usuario_autenticado.id},
            expires_delta=access_token_expires
        )
        
        # Registrar el inicio de sesión exitoso
        print(f"Inicio de sesión exitoso para el usuario {usuario_autenticado.username} desde {client_host}")
        
        # Calcular el tiempo de expiración en segundos
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        
        return TokenDto(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
            usuario=usuario_autenticado
        )
        
    except HTTPException:
        # Re-lanzar las excepciones HTTP que ya manejamos
        raise
        
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"Error inesperado en el inicio de sesión: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al procesar la autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )
