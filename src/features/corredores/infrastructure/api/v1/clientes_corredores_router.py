from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
from src.features.corredores.infrastructure.repositories_cliente_corredor import SQLAlchemyClienteCorredorRepository
from src.features.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.features.corredores.infrastructure.repositories import SQLAlchemyCorredorRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto

router = APIRouter(prefix="/clientes-corredores", tags=["clientes-corredores"])


@router.post("/", response_model=ClienteCorredorDto, status_code=status.HTTP_201_CREATED)
def asignar_cliente_corredor(
    command: AsignarClienteCorredorCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden asignar clientes a corredores
) -> ClienteCorredorDto:
    """Asigna un cliente a un corredor."""
    try:
        cliente_repository = SQLAlchemyClienteRepository(db)
        corredor_repository = SQLAlchemyCorredorRepository(db)
        cliente_corredor_repository = SQLAlchemyClienteCorredorRepository(db)
        
        use_case = AsignarClienteCorredorUseCase(
            cliente_repository, corredor_repository, cliente_corredor_repository
        )
        
        return use_case.execute(command)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar cliente a corredor: {str(e)}"
        )


@router.post("/reasignar", response_model=ClienteCorredorDto)
def reasignar_cliente(
    command: ReasignarClienteCommand,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden reasignar clientes
) -> ClienteCorredorDto:
    """Reasigna un cliente de un corredor a otro."""
    try:
        cliente_repository = SQLAlchemyClienteRepository(db)
        corredor_repository = SQLAlchemyCorredorRepository(db)
        cliente_corredor_repository = SQLAlchemyClienteCorredorRepository(db)
        
        use_case = ReasignarClienteUseCase(
            cliente_repository, corredor_repository, cliente_corredor_repository
        )
        
        return use_case.execute(command)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reasignar cliente: {str(e)}"
        )


@router.delete("/cliente/{cliente_id}/corredor/{corredor_numero}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asignacion_cliente_corredor(
    cliente_id: UUID,
    corredor_numero: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar asignaciones
) -> None:
    """Elimina la asignación de un cliente a un corredor."""
    try:
        cliente_corredor_repository = SQLAlchemyClienteCorredorRepository(db)
        use_case = EliminarAsignacionClienteCorredorUseCase(cliente_corredor_repository)
        
        use_case.execute(cliente_id, corredor_numero)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar asignación: {str(e)}"
        )


@router.get("/corredor/{corredor_numero}", response_model=list[ClienteCorredorDto])
def listar_clientes_por_corredor(
    corredor_numero: int,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar clientes por corredor
) -> list[ClienteCorredorDto]:
    """Lista todos los clientes asignados a un corredor específico."""
    try:
        cliente_corredor_repository = SQLAlchemyClienteCorredorRepository(db)
        use_case = ListarClientesPorCorredorUseCase(cliente_corredor_repository)
        
        return use_case.execute(corredor_numero)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar clientes por corredor: {str(e)}"
        )


@router.get("/cliente/{cliente_id}", response_model=list[ClienteCorredorDto])
def listar_corredores_por_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_db),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar corredores por cliente
) -> list[ClienteCorredorDto]:
    """Lista todos los corredores asignados a un cliente específico."""
    try:
        cliente_corredor_repository = SQLAlchemyClienteCorredorRepository(db)
        use_case = ListarCorredoresPorClienteUseCase(cliente_corredor_repository)
        
        return use_case.execute(cliente_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar corredores por cliente: {str(e)}"
        )
