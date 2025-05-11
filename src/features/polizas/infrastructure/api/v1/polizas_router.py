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
router = APIRouter(prefix="/polizas", tags=["Pu00f3lizas"])


@router.post("/", response_model=PolizaDto, status_code=status.HTTP_201_CREATED)
async def emitir_poliza(
    command: EmitirPolizaCommand,
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden emitir pu00f3lizas
):
    """Emite una nueva pu00f3liza."""
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
    except ValueError as e:
        # Manejo de errores de validaciu00f3n
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al emitir pu00f3liza: {str(e)}"
        )


@router.get("/", response_model=List[PolizaSummaryDto])
async def listar_polizas(
    cliente_id: Optional[uuid.UUID] = Query(None, description="ID del cliente para filtrar pu00f3lizas"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar pu00f3lizas
):
    """Lista todas las pu00f3lizas o filtra por cliente."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    try:
        if cliente_id:
            # Listar pu00f3lizas por cliente
            use_case = ListarPolizasPorClienteUseCase(poliza_repository)
            return use_case.execute(cliente_id)
        else:
            # Listar todas las pu00f3lizas
            use_case = ListarPolizasUseCase(poliza_repository)
            return use_case.execute()
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar pu00f3lizas: {str(e)}"
        )


@router.get("/{poliza_id}", response_model=PolizaDto)
async def obtener_poliza(
    poliza_id: int = Path(..., description="ID de la pu00f3liza a obtener"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver pu00f3lizas
):
    """Obtiene una pu00f3liza por su ID."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerPolizaUseCase(poliza_repository)
    
    # Ejecutamos el caso de uso
    poliza = use_case.execute(poliza_id)
    
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pu00f3liza con ID {poliza_id} no encontrada"
        )
    
    return poliza


@router.get("/numero/{numero_poliza}", response_model=PolizaDto)
async def obtener_poliza_por_numero(
    numero_poliza: str = Path(..., description="Nu00famero de la pu00f3liza a obtener"),
    carpeta: Optional[str] = Query(None, description="Carpeta de la pu00f3liza (opcional)"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver pu00f3lizas
):
    """Obtiene una pu00f3liza por su nu00famero."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerPolizaPorNumeroUseCase(poliza_repository)
    
    # Ejecutamos el caso de uso
    poliza = use_case.execute(numero_poliza, carpeta)
    
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pu00f3liza con nu00famero {numero_poliza} no encontrada"
        )
    
    return poliza


@router.put("/{poliza_id}", response_model=PolizaDto)
async def actualizar_poliza(
    poliza_id: int = Path(..., description="ID de la pu00f3liza a actualizar"),
    command: ActualizarPolizaCommand = None,
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden actualizar pu00f3lizas
):
    """Actualiza una pu00f3liza existente."""
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
    except ValueError as e:
        # Manejo de errores de validaciu00f3n
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar pu00f3liza: {str(e)}"
        )


@router.delete("/{poliza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_poliza(
    poliza_id: int = Path(..., description="ID de la pu00f3liza a eliminar"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar pu00f3lizas
):
    """Elimina una pu00f3liza."""
    # Inicializamos el repositorio
    poliza_repository = SQLAlchemyPolizaRepository(db)
    
    # Inicializamos el caso de uso
    use_case = EliminarPolizaUseCase(poliza_repository)
    
    try:
        # Ejecutamos el caso de uso
        use_case.execute(poliza_id)
        return None  # 204 No Content
    except ValueError as e:
        # Manejo de errores de validaciu00f3n
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar pu00f3liza: {str(e)}"
        )