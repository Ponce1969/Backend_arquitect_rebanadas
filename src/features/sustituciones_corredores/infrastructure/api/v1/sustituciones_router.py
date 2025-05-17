from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.features.sustituciones_corredores.domain.exceptions import (
    SustitucionCorredorNotFoundException,
    SustitucionCorredorSolapamientoException,
    CorredorAusenteNotFoundException,
    CorredorSustitutoNotFoundException,
    SustitucionCorredorFechasInvalidasException
)

from src.features.sustituciones_corredores.application.dtos import (
    FinalizarSustitucionRequest,
    SustitucionCorredorCreate,
    SustitucionCorredorResponse,
    SustitucionCorredorUpdate
)
from src.features.sustituciones_corredores.application.use_cases import (
    CrearSustitucionCorredorUseCase,
    ObtenerSustitucionCorredorPorIdUseCase,
    ListarSustitucionesCorredorUseCase,
    ListarSustitucionesActivasUseCase,
    ObtenerSustitucionesPorCorredorAusenteUseCase,
    ObtenerSustitucionesPorCorredorSustitutoUseCase,
    ObtenerSustitucionesActivasPorCorredorAusenteUseCase,
    ObtenerSustitucionesActivasPorCorredorSustitutoUseCase,
    ActualizarSustitucionCorredorUseCase,
    EliminarSustitucionCorredorUseCase,
    FinalizarSustitucionCorredorUseCase
)
from src.features.sustituciones_corredores.infrastructure.repositories import SQLAlchemySustitucionCorredorRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto


# Crear el router para sustituciones de corredores
router = APIRouter(
    prefix="/sustituciones-corredores",
    tags=["sustituciones-corredores"],
    responses={404: {"description": "No encontrado"}}
)


@router.post("/", response_model=SustitucionCorredorResponse, status_code=status.HTTP_201_CREATED)
def crear_sustitucion_corredor(
    sustitucion: SustitucionCorredorCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden crear sustituciones
) -> SustitucionCorredorResponse:
    """Crea una nueva sustitución de corredor."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = CrearSustitucionCorredorUseCase(repository)
    
    try:
        return use_case.execute(sustitucion)
    except SustitucionCorredorSolapamientoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except (CorredorAusenteNotFoundException, CorredorSustitutoNotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{sustitucion_id}", response_model=SustitucionCorredorResponse)
def obtener_sustitucion_corredor(
    sustitucion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver sustituciones
) -> SustitucionCorredorResponse:
    """Obtiene una sustitución de corredor por su ID."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ObtenerSustitucionCorredorPorIdUseCase(repository)
    
    sustitucion = use_case.execute(sustitucion_id)
    if not sustitucion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sustitución de corredor con ID {sustitucion_id} no encontrada"
        )
    
    return sustitucion


@router.get("/", response_model=list[SustitucionCorredorResponse])
def listar_sustituciones_corredores(
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar sustituciones
) -> list[SustitucionCorredorResponse]:
    """Lista todas las sustituciones de corredores."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ListarSustitucionesCorredorUseCase(repository)
    
    return use_case.execute()


@router.get("/activas", response_model=list[SustitucionCorredorResponse])
def listar_sustituciones_activas(
    fecha: date | None = Query(None, description="Fecha para verificar sustituciones activas (por defecto, fecha actual)"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar sustituciones activas
) -> list[SustitucionCorredorResponse]:
    """Lista todas las sustituciones activas en la fecha especificada."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ListarSustitucionesActivasUseCase(repository)
    
    return use_case.execute(fecha)


@router.get("/corredor-ausente/{corredor_numero}", response_model=list[SustitucionCorredorResponse])
def obtener_sustituciones_por_corredor_ausente(
    corredor_numero: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver sustituciones
) -> list[SustitucionCorredorResponse]:
    """Obtiene todas las sustituciones donde el corredor especificado está ausente."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ObtenerSustitucionesPorCorredorAusenteUseCase(repository)
    
    return use_case.execute(corredor_numero)


@router.get("/corredor-sustituto/{corredor_numero}", response_model=list[SustitucionCorredorResponse])
def obtener_sustituciones_por_corredor_sustituto(
    corredor_numero: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver sustituciones
) -> list[SustitucionCorredorResponse]:
    """Obtiene todas las sustituciones donde el corredor especificado es sustituto."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ObtenerSustitucionesPorCorredorSustitutoUseCase(repository)
    
    return use_case.execute(corredor_numero)


@router.get("/corredor-ausente/{corredor_numero}/activas", response_model=list[SustitucionCorredorResponse])
def obtener_sustituciones_activas_por_corredor_ausente(
    corredor_numero: int,
    fecha: date | None = Query(None, description="Fecha para verificar sustituciones activas (por defecto, fecha actual)"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver sustituciones
) -> list[SustitucionCorredorResponse]:
    """Obtiene las sustituciones activas donde el corredor especificado está ausente."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ObtenerSustitucionesActivasPorCorredorAusenteUseCase(repository)
    
    return use_case.execute(corredor_numero, fecha)


@router.get("/corredor-sustituto/{corredor_numero}/activas", response_model=list[SustitucionCorredorResponse])
def obtener_sustituciones_activas_por_corredor_sustituto(
    corredor_numero: int,
    fecha: date | None = Query(None, description="Fecha para verificar sustituciones activas (por defecto, fecha actual)"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver sustituciones
) -> list[SustitucionCorredorResponse]:
    """Obtiene las sustituciones activas donde el corredor especificado es sustituto."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ObtenerSustitucionesActivasPorCorredorSustitutoUseCase(repository)
    
    return use_case.execute(corredor_numero, fecha)


@router.put("/{sustitucion_id}", response_model=SustitucionCorredorResponse)
def actualizar_sustitucion_corredor(
    sustitucion_id: int,
    sustitucion_data: SustitucionCorredorUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden actualizar sustituciones
) -> SustitucionCorredorResponse:
    """Actualiza una sustitución de corredor existente."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = ActualizarSustitucionCorredorUseCase(repository)
    
    try:
        return use_case.execute(sustitucion_id, sustitucion_data)
    except SustitucionCorredorNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SustitucionCorredorSolapamientoException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except (CorredorAusenteNotFoundException, CorredorSustitutoNotFoundException, SustitucionCorredorFechasInvalidasException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{sustitucion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sustitucion_corredor(
    sustitucion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar sustituciones
) -> None:
    """Elimina una sustitución de corredor por su ID."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = EliminarSustitucionCorredorUseCase(repository)
    
    try:
        use_case.execute(sustitucion_id)
    except SustitucionCorredorNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{sustitucion_id}/finalizar", response_model=SustitucionCorredorResponse)
def finalizar_sustitucion_corredor(
    sustitucion_id: int,
    request: FinalizarSustitucionRequest,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden finalizar sustituciones
) -> SustitucionCorredorResponse:
    """Finaliza una sustitución de corredor estableciendo su fecha de fin y cambiando su estado a inactiva."""
    repository = SQLAlchemySustitucionCorredorRepository(db)
    use_case = FinalizarSustitucionCorredorUseCase(repository)
    
    try:
        return use_case.execute(sustitucion_id, request)
    except SustitucionCorredorNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SustitucionCorredorFechasInvalidasException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
