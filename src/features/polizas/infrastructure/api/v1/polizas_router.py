import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

# Importamos la dependencia de base de datos
from src.infrastructure.database import get_db

# Importamos los DTOs
from src.features.polizas.application.dtos import (
    EmitirPolizaCommand,
    ActualizarPolizaCommand,
    PolizaDto,
    PolizaSummaryDto
)

# Importamos los casos de uso
from src.features.polizas.application.use_cases import (
    EmitirPolizaUseCase,
    ObtenerPolizaUseCase,
    ObtenerPolizaPorNumeroUseCase,
    ListarPolizasUseCase,
    ListarPolizasPorClienteUseCase,
    ActualizarPolizaUseCase,
    EliminarPolizaUseCase
)

# Importamos las excepciones personalizadas
from src.features.polizas.domain.exceptions import (
    PolizaException,
    PolizaNotFoundException,
    PolizaNumeroExistsException,
    ClienteNotFoundException,
    CorredorNotFoundException,
    TipoSeguroNotFoundException,
    MonedaNotFoundException
)

# Importamos los repositorios concretos
from src.features.polizas.infrastructure.repositories import SQLAlchemyPolizaRepository
from src.features.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.features.corredores.infrastructure.repositories import SQLAlchemyCorredorRepository
from src.features.tipos_seguros.infrastructure.repositories import SQLAlchemyTipoSeguroRepository
# from src.infrastructure.database.repositories import SQLAlchemyMonedaRepository  # Asumimos que existe

# Importamos las dependencias de seguridad (para proteger endpoints)
# from src.infrastructure.security.dependencies import get_current_user, get_admin_user
# from src.features.usuarios.application.dtos import UsuarioDto

# Creamos el router
router = APIRouter(prefix="/polizas", tags=["Polizas"])


@router.post("/", response_model=PolizaDto, status_code=status.HTTP_201_CREATED)
async def emitir_poliza(
    command: EmitirPolizaCommand,
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden emitir polizas
):
    """Emite una nueva póliza."""
    # Inicializamos los repositorios
    poliza_repository = SQLAlchemyPolizaRepository(db)
    cliente_repository = SQLAlchemyClienteRepository(db)
    corredor_repository = SQLAlchemyCorredorRepository(db)
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    # moneda_repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = EmitirPolizaUseCase(
        poliza_repository,
        cliente_repository,
        corredor_repository,
        tipo_seguro_repository,
        # moneda_repository
    )
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(command)
    except PolizaNumeroExistsException as e:
        # Manejo de errores de conflicto (ya existe)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ClienteNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CorredorNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TipoSeguroNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except MonedaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PolizaException as e:
        # Manejo de errores de validación generales
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al emitir póliza: {str(e)}"
        )


@router.get("/", response_model=List[PolizaSummaryDto])
async def listar_polizas(
    cliente_id: Optional[uuid.UUID] = Query(None, description="ID del cliente para filtrar polizas"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar polizas
):
    """Lista todas las polizas o filtra por cliente."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    try:
        if cliente_id:
            # Listar polizas por cliente
            use_case = ListarPolizasPorClienteUseCase(poliza_repository)
            return use_case.execute(cliente_id)
        else:
            # Listar todas las polizas
            use_case = ListarPolizasUseCase(poliza_repository)
            return use_case.execute()
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar polizas: {str(e)}"
        )


@router.get("/{poliza_id}", response_model=PolizaDto)
async def obtener_poliza(
    poliza_id: int = Path(..., description="ID de la póliza a obtener"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver polizas
):
    """Obtiene una póliza por su ID."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerPolizaUseCase(poliza_repository)
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(poliza_id)
    except PolizaNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener póliza: {str(e)}"
        )


@router.get("/numero/{numero_poliza}", response_model=PolizaDto)
async def obtener_poliza_por_numero(
    numero_poliza: str = Path(..., description="Número de la póliza a obtener"),
    carpeta: Optional[str] = Query(None, description="Carpeta de la póliza (opcional)"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver polizas
):
    """Obtiene una póliza por su número."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerPolizaPorNumeroUseCase(poliza_repository)
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(numero_poliza, carpeta)
    except PolizaNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Póliza con número {numero_poliza} no encontrada"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener póliza por número: {str(e)}"
        )


@router.put("/{poliza_id}", response_model=PolizaDto)
async def actualizar_poliza(
    poliza_id: int = Path(..., description="ID de la póliza a actualizar"),
    command: ActualizarPolizaCommand = None,
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden actualizar polizas
):
    """Actualiza una póliza existente."""
    # Aseguramos que el ID en el path coincida con el ID en el comando
    if command.id != poliza_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID en la URL no coincide con el ID en el cuerpo de la solicitud"
        )
    
    # Inicializamos los repositorios
    poliza_repository = SQLAlchemyPolizaRepository(db)
    corredor_repository = SQLAlchemyCorredorRepository(db)
    # moneda_repository = SQLAlchemyMonedaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ActualizarPolizaUseCase(
        poliza_repository,
        corredor_repository,
        # moneda_repository
    )
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(command)
    except PolizaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CorredorNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except MonedaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PolizaException as e:
        # Manejo de errores de validación generales
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar póliza: {str(e)}"
        )


@router.delete("/{poliza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_poliza(
    poliza_id: int = Path(..., description="ID de la póliza a eliminar"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar polizas
):
    """Elimina una póliza."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = EliminarPolizaUseCase(poliza_repository)
    
    try:
        # Ejecutamos el caso de uso
        use_case.execute(poliza_id)
        return None  # 204 No Content
    except PolizaNotFoundException as e:
        # Manejo de errores de entidad no encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PolizaException as e:
        # Manejo de errores de validación generales
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar póliza: {str(e)}"
        )