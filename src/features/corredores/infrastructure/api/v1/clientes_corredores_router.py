from datetime import date
from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.features.corredores.application.dtos_cliente_corredor import (
    ClienteCorredorDto,
    AsignarClienteCorredorCommand,
    ReasignarClienteCommand
)
from src.features.corredores.application.use_cases_cliente_corredor import (
    AsignarClienteCorredorUseCase,
    ReasignarClienteUseCase,
    EliminarAsignacionClienteCorredorUseCase,
    ListarClientesPorCorredorUseCase,
    ListarCorredoresPorClienteUseCase
)
from src.features.corredores.dependencies import (
    get_cliente_repository,
    get_corredor_repository,
    get_cliente_corredor_repository
)
from src.features.corredores.domain.exceptions import (
    ClienteNoEncontradoException,
    CorredorNoEncontradoException,
    ClienteCorredorAsignacionDuplicadaException,
    ClienteCorredorNoEncontradoException,
    FechaAsignacionInvalidaException
)
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto

router = APIRouter(
    prefix="/clientes-corredores",
    tags=["clientes-corredores"],
    responses={404: {"description": "No encontrado"}},
)


@router.post(
    "/",
    response_model=ClienteCorredorDto,
    status_code=status.HTTP_201_CREATED,
    summary="Asignar un cliente a un corredor",
    description="Crea una nueva asignación entre un cliente y un corredor"
)
async def asignar_cliente_corredor(
    command: AsignarClienteCorredorCommand,
    cliente_repository=Depends(get_cliente_repository),
    corredor_repository=Depends(get_corredor_repository),
    cliente_corredor_repository=Depends(get_cliente_corredor_repository),
    current_user: UsuarioDto = Depends(get_current_user)
) -> ClienteCorredorDto:
    """Asigna un cliente a un corredor.
    
    Args:
        command: Datos para la asignación
        cliente_repository: Repositorio de clientes inyectado por dependencia
        corredor_repository: Repositorio de corredores inyectado por dependencia
        cliente_corredor_repository: Repositorio de relaciones cliente-corredor inyectado por dependencia
        current_user: Usuario autenticado
        
    Returns:
        ClienteCorredorDto: Datos de la asignación creada
    """
    use_case = AsignarClienteCorredorUseCase(
        cliente_repository=cliente_repository,
        corredor_repository=corredor_repository,
        cliente_corredor_repository=cliente_corredor_repository
    )
    
    try:
        return use_case.execute(command)
    except ClienteNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el cliente con ID {e.cliente_id}"
        )
    except CorredorNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {e.corredor_numero}"
        )
    except ClienteCorredorAsignacionDuplicadaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente ya está asignado al corredor {e.corredor_numero}"
        )
    except FechaAsignacionInvalidaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La fecha de asignación no puede ser futura: {e.fecha}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al asignar cliente a corredor: {str(e)}"
        )


@router.put(
    "/reasignar",
    response_model=ClienteCorredorDto,
    status_code=status.HTTP_200_OK,
    summary="Reasignar un cliente a otro corredor",
    description="Actualiza la asignación de un cliente de un corredor a otro"
)
async def reasignar_cliente(
    command: ReasignarClienteCommand,
    cliente_repository=Depends(get_cliente_repository),
    corredor_repository=Depends(get_corredor_repository),
    cliente_corredor_repository=Depends(get_cliente_corredor_repository),
    current_user: UsuarioDto = Depends(get_current_user)
) -> ClienteCorredorDto:
    """Reasigna un cliente de un corredor a otro.
    
    Args:
        command: Datos para la reasignación
        cliente_repository: Repositorio de clientes inyectado por dependencia
        corredor_repository: Repositorio de corredores inyectado por dependencia
        cliente_corredor_repository: Repositorio de relaciones cliente-corredor inyectado por dependencia
        current_user: Usuario autenticado
        
    Returns:
        ClienteCorredorDto: Datos de la asignación actualizada
    """
    use_case = ReasignarClienteUseCase(
        cliente_repository=cliente_repository,
        corredor_repository=corredor_repository,
        cliente_corredor_repository=cliente_corredor_repository
    )
    
    try:
        return use_case.execute(command)
    except ClienteNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el cliente con ID {e.cliente_id}"
        )
    except CorredorNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {e.corredor_numero}"
        )
    except ClienteCorredorNoEncontradoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una asignación del cliente {e.cliente_id} al corredor {e.corredor_numero}"
        )
    except ClienteCorredorAsignacionDuplicadaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente ya está asignado al corredor {e.corredor_numero}"
        )
    except FechaAsignacionInvalidaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La fecha de asignación no puede ser futura: {e.fecha}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al reasignar cliente: {str(e)}"
        )


@router.delete(
    "/{cliente_id}/corredor/{corredor_numero}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar asignación de cliente a corredor",
    description="Elimina la asignación de un cliente a un corredor específico"
)
async def eliminar_asignacion_cliente_corredor(
    cliente_id: UUID,
    corredor_numero: int,
    cliente_corredor_repository=Depends(get_cliente_corredor_repository),
    current_user: UsuarioDto = Depends(get_admin_user)
) -> None:
    """Elimina la asignación de un cliente a un corredor.
    
    Args:
        cliente_id: ID del cliente
        corredor_numero: Número del corredor
        cliente_corredor_repository: Repositorio de relaciones cliente-corredor inyectado por dependencia
        current_user: Usuario administrador autenticado
    """
    use_case = EliminarAsignacionClienteCorredorUseCase(
        cliente_corredor_repository=cliente_corredor_repository
    )
    
    try:
        use_case.execute(cliente_id, corredor_numero)
    except ClienteCorredorNoEncontradoException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una asignación del cliente {cliente_id} al corredor {corredor_numero}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al eliminar la asignación: {str(e)}"
        )


@router.get(
    "/corredor/{corredor_numero}/clientes",
    response_model=List[ClienteCorredorDto],
    status_code=status.HTTP_200_OK,
    summary="Listar clientes por corredor",
    description="Obtiene la lista de clientes asignados a un corredor específico"
)
async def listar_clientes_por_corredor(
    corredor_numero: int,
    cliente_corredor_repository=Depends(get_cliente_corredor_repository),
    current_user: UsuarioDto = Depends(get_current_user)
) -> List[ClienteCorredorDto]:
    """Lista todos los clientes asignados a un corredor.
    
    Args:
        corredor_numero: Número del corredor
        cliente_corredor_repository: Repositorio de relaciones cliente-corredor inyectado por dependencia
        current_user: Usuario autenticado
        
    Returns:
        List[ClienteCorredorDto]: Lista de asignaciones de clientes al corredor
    """
    use_case = ListarClientesPorCorredorUseCase(
        cliente_corredor_repository=cliente_corredor_repository
    )
    
    try:
        return use_case.execute(corredor_numero)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al listar clientes por corredor: {str(e)}"
        )


@router.get(
    "/cliente/{cliente_id}/corredores",
    response_model=List[ClienteCorredorDto],
    status_code=status.HTTP_200_OK,
    summary="Listar corredores por cliente",
    description="Obtiene la lista de corredores asignados a un cliente específico"
)
async def listar_corredores_por_cliente(
    cliente_id: UUID,
    cliente_corredor_repository=Depends(get_cliente_corredor_repository),
    current_user: UsuarioDto = Depends(get_current_user)
) -> List[ClienteCorredorDto]:
    """Lista todos los corredores asignados a un cliente.
    
    Args:
        cliente_id: ID del cliente
        cliente_corredor_repository: Repositorio de relaciones cliente-corredor inyectado por dependencia
        current_user: Usuario autenticado
        
    Returns:
        List[ClienteCorredorDto]: Lista de asignaciones de corredores al cliente
    """
    use_case = ListarCorredoresPorClienteUseCase(
        cliente_corredor_repository=cliente_corredor_repository
    )
    
    try:
        return use_case.execute(cliente_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al listar corredores por cliente: {str(e)}"
        )
