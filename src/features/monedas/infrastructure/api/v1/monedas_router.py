from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.features.monedas.application.dtos import MonedaDto, CrearMonedaCommand, ActualizarMonedaCommand
from src.features.monedas.application.use_cases import (
    ListarMonedasUseCase, ObtenerMonedaUseCase, ObtenerMonedaPorCodigoUseCase,
    CrearMonedaUseCase, ActualizarMonedaUseCase, EliminarMonedaUseCase
)
from src.features.monedas.domain.exceptions import MonedaNotFoundException, MonedaInvalidaException, MonedaCodigoExistsException
from src.features.monedas.infrastructure.repositories import SQLAlchemyMonedaRepository
from src.domain.shared.exceptions import ValidationError, NotFoundError, ConflictError
from src.infrastructure.database import get_db
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto


router = APIRouter(prefix="/monedas", tags=["Monedas"])


# Dependencias para inyección
def get_moneda_repository(db: Session = Depends(get_db)):
    return SQLAlchemyMonedaRepository(db)


def get_listar_monedas_use_case(repo = Depends(get_moneda_repository)):
    return ListarMonedasUseCase(repo)


def get_obtener_moneda_use_case(repo = Depends(get_moneda_repository)):
    return ObtenerMonedaUseCase(repo)


def get_obtener_moneda_por_codigo_use_case(repo = Depends(get_moneda_repository)):
    return ObtenerMonedaPorCodigoUseCase(repo)


def get_crear_moneda_use_case(repo = Depends(get_moneda_repository)):
    return CrearMonedaUseCase(repo)


def get_actualizar_moneda_use_case(repo = Depends(get_moneda_repository)):
    return ActualizarMonedaUseCase(repo)


def get_eliminar_moneda_use_case(repo = Depends(get_moneda_repository)):
    return EliminarMonedaUseCase(repo)


# Endpoints
@router.get("/", response_model=list[MonedaDto])
async def listar_monedas(
    use_case = Depends(get_listar_monedas_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Cualquier usuario autenticado puede listar monedas
):
    """Lista todas las monedas activas."""
    return use_case.execute()


@router.get("/{moneda_id}", response_model=MonedaDto)
async def obtener_moneda(
    moneda_id: int, 
    use_case = Depends(get_obtener_moneda_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Cualquier usuario autenticado puede ver monedas
):
    """Obtiene una moneda por su ID."""
    try:
        return use_case.execute(moneda_id)
    except MonedaNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/codigo/{codigo}", response_model=MonedaDto)
async def obtener_moneda_por_codigo(
    codigo: str, 
    use_case = Depends(get_obtener_moneda_por_codigo_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Cualquier usuario autenticado puede ver monedas
):
    """Obtiene una moneda por su código."""
    try:
        return use_case.execute(codigo)
    except (MonedaNotFoundException, MonedaInvalidaException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=MonedaDto, status_code=status.HTTP_201_CREATED)
async def crear_moneda(
    request: Request,
    use_case = Depends(get_crear_moneda_use_case),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden crear monedas
):
    """Crea una nueva moneda."""
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = await request.json()
        
        # Validar y crear el comando
        command = CrearMonedaCommand.validate_and_create(data)
        
        # Ejecutar el caso de uso
        return use_case.execute(command)
    except ValidationError as e:
        # Error de validación (422)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": {"message": "Error de validación", "details": e.details}}
        )
    except MonedaCodigoExistsException as e:
        # Error de conflicto (409)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": {"message": str(e), "details": {"codigo": str(e)}}}
        )


@router.put("/{moneda_id}", response_model=MonedaDto)
async def actualizar_moneda(
    moneda_id: int,
    request: Request,
    use_case = Depends(get_actualizar_moneda_use_case),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden actualizar monedas
):
    """Actualiza una moneda existente."""
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = await request.json()
        
        # Asegurarse de que el ID del path coincida con el del comando
        data["id"] = moneda_id
        
        # Validar y crear el comando
        command = ActualizarMonedaCommand.validate_and_create(data)
        
        # Ejecutar el caso de uso
        return use_case.execute(command)
    except ValidationError as e:
        # Error de validación (422)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": {"message": "Error de validación", "details": e.details}}
        )
    except MonedaNotFoundException as e:
        # Error de recurso no encontrado (404)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": {"message": str(e), "details": {"moneda_id": moneda_id}}}
        )
    except MonedaCodigoExistsException as e:
        # Error de conflicto (409)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": {"message": str(e), "details": {"codigo": str(e)}}}
        )


@router.delete("/{moneda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_moneda(
    moneda_id: int, 
    use_case = Depends(get_eliminar_moneda_use_case),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar monedas
):
    """Elimina una moneda (marcándola como inactiva)."""
    try:
        use_case.execute(moneda_id)
        return None
    except MonedaNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
