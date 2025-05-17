from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.features.clientes.application.dtos import (
    ClienteCreate,
    ClienteResponse,
    ClienteSearchParams,
    ClienteUpdate,
)
from src.features.clientes.application.use_cases import (
    ActualizarClienteUseCase,
    BuscarClientesUseCase,
    CrearClienteUseCase,
    EliminarClienteUseCase,
    ListarClientesUseCase,
    ObtenerClientePorDocumentoUseCase,
    ObtenerClientePorNumeroUseCase,
    ObtenerClienteUseCase,
)
from src.features.clientes.domain.exceptions import (
    ClienteException,
    ClienteNotFoundException,
    ClienteNumeroNotFoundException,
    ClienteDocumentoNotFoundException,
    ClienteDocumentoExistsException,
    ClienteEmailExistsException,
)
from src.features.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    cliente: ClienteCreate, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden crear clientes
) -> ClienteResponse:
    """Crea un nuevo cliente."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = CrearClienteUseCase(repository)
        return use_case.execute(cliente)
    except ClienteDocumentoExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ClienteEmailExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ClienteException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(
    cliente_id: UUID, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver clientes
) -> ClienteResponse:
    """Obtiene un cliente por su ID."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = ObtenerClienteUseCase(repository)
        return use_case.execute(cliente_id)
    except ClienteNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.get("/numero/{numero_cliente}", response_model=ClienteResponse)
def obtener_cliente_por_numero(
    numero_cliente: int, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver clientes
) -> ClienteResponse:
    """Obtiene un cliente por su número de cliente."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = ObtenerClientePorNumeroUseCase(repository)
        return use_case.execute(numero_cliente)
    except ClienteNumeroNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente por número: {str(e)}",
        )


@router.get("/documento/{numero_documento}", response_model=ClienteResponse)
def obtener_cliente_por_documento(
    numero_documento: str, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver clientes
) -> ClienteResponse:
    """Obtiene un cliente por su número de documento."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = ObtenerClientePorDocumentoUseCase(repository)
        return use_case.execute(numero_documento)
    except ClienteDocumentoNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente por documento: {str(e)}",
        )


@router.get("/tipo-documento/{tipo_documento_id}/documento/{numero_documento}", response_model=ClienteResponse)
def obtener_cliente_por_tipo_y_numero_documento(
    tipo_documento_id: int, 
    numero_documento: str, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver clientes
) -> ClienteResponse:
    """Obtiene un cliente por su tipo y número de documento."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        cliente = repository.get_by_documento(tipo_documento_id, numero_documento)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con tipo de documento {tipo_documento_id} y número {numero_documento} no encontrado",
            )
        return ClienteResponse(
            id=cliente.id,
            numero_cliente=cliente.numero_cliente,
            nombres=cliente.nombres,
            apellidos=cliente.apellidos,
            tipo_documento_id=cliente.tipo_documento_id,
            numero_documento=cliente.numero_documento,
            fecha_nacimiento=cliente.fecha_nacimiento,
            direccion=cliente.direccion,
            localidad=cliente.localidad,
            telefonos=cliente.telefonos,
            movil=cliente.movil,
            mail=cliente.mail,
            observaciones=cliente.observaciones,
            creado_por_id=cliente.creado_por_id,
            modificado_por_id=cliente.modificado_por_id,
            fecha_creacion=cliente.fecha_creacion,
            fecha_modificacion=cliente.fecha_modificacion,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar cliente: {str(e)}",
        )


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    query: str | None = Query(None, description="Término de búsqueda"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar clientes
) -> list[ClienteResponse]:
    """Lista todos los clientes o busca por término."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        
        # Si hay un término de búsqueda, usar el caso de uso de búsqueda
        if query:
            search_params = ClienteSearchParams(query=query)
            use_case = BuscarClientesUseCase(repository)
            return use_case.execute(search_params)
        
        # Si no hay término de búsqueda, listar todos los clientes
        use_case = ListarClientesUseCase(repository)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar clientes: {str(e)}",
        )


@router.get("/buscar/", response_model=list[ClienteResponse])
def buscar_clientes(
    query: str | None = Query(None, description="Término de búsqueda en nombres, apellidos, documento o email"),
    tipo_documento_id: int | None = Query(None, description="ID del tipo de documento"),
    localidad: str | None = Query(None, description="Localidad del cliente"),
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden buscar clientes
) -> list[ClienteResponse]:
    """Busca clientes según criterios específicos.
    
    Permite realizar búsquedas avanzadas combinando diferentes criterios.
    """
    try:
        repository = SQLAlchemyClienteRepository(db)
        search_params = ClienteSearchParams(
            query=query,
            tipo_documento_id=tipo_documento_id,
            localidad=localidad
        )
        use_case = BuscarClientesUseCase(repository)
        return use_case.execute(search_params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes: {str(e)}",
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: UUID, 
    cliente: ClienteUpdate, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden actualizar clientes
) -> ClienteResponse:
    """Actualiza un cliente existente."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = ActualizarClienteUseCase(repository)
        return use_case.execute(cliente_id, cliente)
    except ClienteNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ClienteDocumentoExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ClienteEmailExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ClienteException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(
    cliente_id: UUID, 
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar clientes
) -> None:
    """Elimina un cliente."""
    try:
        repository = SQLAlchemyClienteRepository(db)
        use_case = EliminarClienteUseCase(repository)
        use_case.execute(cliente_id)
    except ClienteNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
