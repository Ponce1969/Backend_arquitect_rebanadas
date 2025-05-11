from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.features.corredores.application.dtos import (
    CorredorCreate,
    CorredorDto,
    CorredorSearchParams,
    CorredorUpdate
)
from src.features.corredores.application.use_cases import (
    ActualizarCorredorUseCase,
    BuscarCorredoresUseCase,
    CrearCorredorUseCase,
    EliminarCorredorUseCase,
    ListarCorredoresUseCase,
    ObtenerCorredorPorDocumentoUseCase,
    ObtenerCorredorPorEmailUseCase,
    ObtenerCorredorPorIdUseCase,
    ObtenerCorredorPorNumeroUseCase
)
from src.features.corredores.infrastructure.repositories import SQLAlchemyCorredorRepository
from src.infrastructure.database import get_db

# Crear el router para corredores
router = APIRouter(
    prefix="/corredores",
    tags=["corredores"],
    responses={404: {"description": "No encontrado"}}
)


@router.post("/", response_model=CorredorDto, status_code=status.HTTP_201_CREATED)
def crear_corredor(
    corredor: CorredorCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo corredor."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = CrearCorredorUseCase(repository)
    
    try:
        return use_case.execute(corredor)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{corredor_id}", response_model=CorredorDto)
def obtener_corredor_por_id(
    corredor_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un corredor por su ID técnico."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = ObtenerCorredorPorIdUseCase(repository)
    
    corredor = use_case.execute(corredor_id)
    if not corredor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Corredor con ID {corredor_id} no encontrado"
        )
    
    return corredor


@router.get("/numero/{numero}", response_model=CorredorDto)
def obtener_corredor_por_numero(
    numero: int,
    db: Session = Depends(get_db)
):
    """Obtiene un corredor por su número (identificador de negocio)."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = ObtenerCorredorPorNumeroUseCase(repository)
    
    corredor = use_case.execute(numero)
    if not corredor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Corredor con número {numero} no encontrado"
        )
    
    return corredor


@router.get("/documento/{documento}", response_model=CorredorDto)
def obtener_corredor_por_documento(
    documento: str,
    db: Session = Depends(get_db)
):
    """Obtiene un corredor por su número de documento."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = ObtenerCorredorPorDocumentoUseCase(repository)
    
    corredor = use_case.execute(documento)
    if not corredor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Corredor con documento {documento} no encontrado"
        )
    
    return corredor


@router.get("/email/{email}", response_model=CorredorDto)
def obtener_corredor_por_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Obtiene un corredor por su dirección de correo electrónico."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = ObtenerCorredorPorEmailUseCase(repository)
    
    corredor = use_case.execute(email)
    if not corredor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Corredor con email {email} no encontrado"
        )
    
    return corredor


@router.get("/", response_model=List[CorredorDto])
def listar_corredores(
    db: Session = Depends(get_db)
):
    """Lista todos los corredores."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = ListarCorredoresUseCase(repository)
    
    return use_case.execute()


@router.put("/{numero}", response_model=CorredorDto)
def actualizar_corredor(
    numero: int,
    corredor_data: CorredorUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un corredor existente."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = ActualizarCorredorUseCase(repository)
    
    try:
        corredor = use_case.execute(numero, corredor_data)
        if not corredor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Corredor con número {numero} no encontrado"
            )
        
        return corredor
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{corredor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_corredor(
    corredor_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un corredor por su ID técnico."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = EliminarCorredorUseCase(repository)
    
    result = use_case.execute(corredor_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Corredor con ID {corredor_id} no encontrado"
        )


@router.get("/search/", response_model=List[CorredorDto])
def buscar_corredores(
    query: Optional[str] = Query(None, description="Término de búsqueda para filtrar corredores"),
    esta_activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    """Busca corredores según criterios específicos."""
    repository = SQLAlchemyCorredorRepository(db)
    use_case = BuscarCorredoresUseCase(repository)
    
    search_params = CorredorSearchParams(
        query=query,
        esta_activo=esta_activo
    )
    
    return use_case.execute(search_params)
