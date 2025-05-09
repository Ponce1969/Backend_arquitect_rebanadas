from typing import List, Optional, UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from infrastructure.database.database import get_db
from features.clientes.application.dtos import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteSearchParams,
)
from features.clientes.application.use_cases import (
    CrearClienteUseCase,
    ObtenerClienteUseCase,
    ObtenerClientePorNumeroUseCase,
    ObtenerClientePorDocumentoUseCase,
    ListarClientesUseCase,
    BuscarClientesUseCase,
    ActualizarClienteUseCase,
    EliminarClienteUseCase,
)
from features.clientes.infrastructure.repositories import SQLAlchemyClienteRepository


router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    cliente: ClienteCreate, db: Session = Depends(get_db)
) -> ClienteResponse:
    """Crea un nuevo cliente."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = CrearClienteUseCase(repository)
        return use_case.execute(cliente)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: UUID, db: Session = Depends(get_db)) -> ClienteResponse:
    """Obtiene un cliente por su ID."""
    repository = SQLAlchemyClienteRepository(db)
    use_case = ObtenerClienteUseCase(repository)
    cliente = use_case.execute(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado",
        )
    return cliente


@router.get("/numero/{numero_cliente}", response_model=ClienteResponse)
def obtener_cliente_por_numero(
    numero_cliente: int, db: Session = Depends(get_db)
) -> ClienteResponse:
    """Obtiene un cliente por su número de cliente."""
    repository = SQLAlchemyClienteRepository(db)
    use_case = ObtenerClientePorNumeroUseCase(repository)
    cliente = use_case.execute(numero_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con número {numero_cliente} no encontrado",
        )
    return cliente


@router.get("/documento/{numero_documento}", response_model=ClienteResponse)
def obtener_cliente_por_documento(
    numero_documento: str, db: Session = Depends(get_db)
) -> ClienteResponse:
    """Obtiene un cliente por su número de documento."""
    repository = SQLAlchemyClienteRepository(db)
    use_case = ObtenerClientePorDocumentoUseCase(repository)
    cliente = use_case.execute(numero_documento)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con documento {numero_documento} no encontrado",
        )
    return cliente


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    query: Optional[str] = Query(None, description="Término de búsqueda"),
    db: Session = Depends(get_db)
) -> List[ClienteResponse]:
    """Lista todos los clientes o busca por término."""
    repository = SQLAlchemyClienteRepository(db)
    
    if query:
        # Si hay un término de búsqueda, usamos el caso de uso de búsqueda
        use_case = BuscarClientesUseCase(repository)
        search_params = ClienteSearchParams(query=query)
        return use_case.execute(search_params)
    else:
        # Si no hay término de búsqueda, listamos todos los clientes
        use_case = ListarClientesUseCase(repository)
        return use_case.execute()


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: UUID, cliente: ClienteUpdate, db: Session = Depends(get_db)
) -> ClienteResponse:
    """Actualiza un cliente existente."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = ActualizarClienteUseCase(repository)
        updated_cliente = use_case.execute(cliente_id, cliente)
        if not updated_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado",
            )
        return updated_cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)) -> None:
    """Elimina un cliente."""
    repository = SQLAlchemyClienteRepository(db)
    use_case = EliminarClienteUseCase(repository)
    deleted = use_case.execute(cliente_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado",
        )
