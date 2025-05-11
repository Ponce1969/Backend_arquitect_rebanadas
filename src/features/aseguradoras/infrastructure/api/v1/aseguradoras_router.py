
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.features.aseguradoras.application.dtos import (
    AseguradoraCreate,
    AseguradoraResponse,
    AseguradoraUpdate,
)
from src.features.aseguradoras.application.use_cases import (
    ActualizarAseguradoraUseCase,
    BuscarAseguradorasUseCase,
    CrearAseguradoraUseCase,
    EliminarAseguradoraUseCase,
    ListarAseguradorasUseCase,
    ObtenerAseguradoraUseCase,
)
from src.features.aseguradoras.infrastructure.repositories import SQLAlchemyAseguradoraRepository
from src.infrastructure.database import get_db

router = APIRouter(prefix="/aseguradoras", tags=["aseguradoras"])


@router.post("/", response_model=AseguradoraResponse, status_code=status.HTTP_201_CREATED)
def crear_aseguradora(
    aseguradora: AseguradoraCreate, db: Session = Depends(get_db)
) -> AseguradoraResponse:
    """Crea una nueva aseguradora."""
    try:
        repository = SQLAlchemyAseguradoraRepository(db)
        use_case = CrearAseguradoraUseCase(repository)
        return use_case.execute(aseguradora)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear aseguradora: {str(e)}",
        )


@router.get("/{aseguradora_id}", response_model=AseguradoraResponse)
def obtener_aseguradora(aseguradora_id: int, db: Session = Depends(get_db)) -> AseguradoraResponse:
    """Obtiene una aseguradora por su ID."""
    repository = SQLAlchemyAseguradoraRepository(db)
    use_case = ObtenerAseguradoraUseCase(repository)
    aseguradora = use_case.execute(aseguradora_id)
    if not aseguradora:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aseguradora con ID {aseguradora_id} no encontrada",
        )
    return aseguradora


@router.get("/", response_model=list[AseguradoraResponse])
def listar_aseguradoras(db: Session = Depends(get_db)) -> list[AseguradoraResponse]:
    """Lista todas las aseguradoras."""
    repository = SQLAlchemyAseguradoraRepository(db)
    use_case = ListarAseguradorasUseCase(repository)
    return use_case.execute()


@router.put("/{aseguradora_id}", response_model=AseguradoraResponse)
def actualizar_aseguradora(
    aseguradora_id: int, aseguradora: AseguradoraUpdate, db: Session = Depends(get_db)
) -> AseguradoraResponse:
    """Actualiza una aseguradora existente."""
    try:
        repository = SQLAlchemyAseguradoraRepository(db)
        use_case = ActualizarAseguradoraUseCase(repository)
        updated_aseguradora = use_case.execute(aseguradora_id, aseguradora)
        if not updated_aseguradora:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aseguradora con ID {aseguradora_id} no encontrada",
            )
        return updated_aseguradora
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar aseguradora: {str(e)}",
        )


@router.delete("/{aseguradora_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_aseguradora(aseguradora_id: int, db: Session = Depends(get_db)) -> None:
    """Elimina una aseguradora."""
    repository = SQLAlchemyAseguradoraRepository(db)
    use_case = EliminarAseguradoraUseCase(repository)
    deleted = use_case.execute(aseguradora_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aseguradora con ID {aseguradora_id} no encontrada",
        )


@router.get("/search/", response_model=list[AseguradoraResponse])
def buscar_aseguradoras(
    query: str = None, esta_activa: bool = None, db: Session = Depends(get_db)
) -> list[AseguradoraResponse]:
    """Busca aseguradoras según criterios específicos.
    
    Args:
        query: Texto para buscar en nombre, identificador fiscal o dirección
        esta_activa: Filtrar por estado activo/inactivo
    """
    try:
        repository = SQLAlchemyAseguradoraRepository(db)
        use_case = BuscarAseguradorasUseCase(repository)
        return use_case.execute(query=query, esta_activa=esta_activa)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar aseguradoras: {str(e)}",
        )
