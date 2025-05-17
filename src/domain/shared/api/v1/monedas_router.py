from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.domain.shared.dtos import MonedaDto, CrearMonedaCommand, ActualizarMonedaCommand
from src.domain.shared.exceptions import MonedaNotFoundException, MonedaInvalidaException, MonedaCodigoExistsException
from src.domain.shared.use_cases import (
    CrearMonedaUseCase,
    ActualizarMonedaUseCase,
    EliminarMonedaUseCase,
    ListarMonedasUseCase,
    ObtenerMonedaUseCase,
    ObtenerMonedaPorCodigoUseCase
)
from src.infrastructure.database import get_db
from src.infrastructure.database.repositories import SQLAlchemyMonedaRepository
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto

# Creamos el router
router = APIRouter(prefix="/monedas", tags=["monedas"])


@router.post("/", response_model=MonedaDto, status_code=status.HTTP_201_CREATED)
async def crear_moneda(
    command: CrearMonedaCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden crear monedas
):
    """Crea una nueva moneda."""
    # Inicializamos el repositorio
    repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = CrearMonedaUseCase(repository)
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(command)
    except MonedaCodigoExistsException as e:
        # Manejo de errores de conflicto (ya existe)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/", response_model=list[MonedaDto])
async def listar_monedas(
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Cualquier usuario autenticado puede listar monedas
):
    """Lista todas las monedas activas."""
    # Inicializamos el repositorio
    repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ListarMonedasUseCase(repository)
    
    # Ejecutamos el caso de uso
    return use_case.execute()


@router.get("/{moneda_id}", response_model=MonedaDto)
async def obtener_moneda(
    moneda_id: int = Path(..., description="ID de la moneda a obtener"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Cualquier usuario autenticado puede ver monedas
):
    """Obtiene una moneda por su ID."""
    # Inicializamos el repositorio
    repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerMonedaUseCase(repository)
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(moneda_id)
    except MonedaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/codigo/{codigo}", response_model=MonedaDto)
async def obtener_moneda_por_codigo(
    codigo: str = Path(..., description="Código de la moneda a obtener"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Cualquier usuario autenticado puede ver monedas
):
    """Obtiene una moneda por su código."""
    # Inicializamos el repositorio
    repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerMonedaPorCodigoUseCase(repository)
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(codigo)
    except MonedaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except MonedaInvalidaException as e:
        # Manejo de errores de entidad inválida
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{moneda_id}", response_model=MonedaDto)
async def actualizar_moneda(
    moneda_id: int = Path(..., description="ID de la moneda a actualizar"),
    command: ActualizarMonedaCommand = None,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden actualizar monedas
):
    """Actualiza una moneda existente."""
    # Aseguramos que el ID en el path coincida con el ID en el comando
    if command.id != moneda_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID en la URL no coincide con el ID en el cuerpo de la solicitud"
        )
    
    # Inicializamos el repositorio
    repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ActualizarMonedaUseCase(repository)
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(command)
    except MonedaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except MonedaCodigoExistsException as e:
        # Manejo de errores de conflicto (ya existe)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{moneda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_moneda(
    moneda_id: int = Path(..., description="ID de la moneda a eliminar"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar monedas
):
    """Elimina una moneda (marcándola como inactiva)."""
    # Inicializamos el repositorio
    repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = EliminarMonedaUseCase(repository)
    
    try:
        # Ejecutamos el caso de uso
        use_case.execute(moneda_id)
        return None  # 204 No Content
    except MonedaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
