from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

# Importamos la dependencia de base de datos
from src.infrastructure.database import get_db

# Importamos los DTOs
from src.features.tipos_seguros.application.dtos import (
    CreateTipoSeguroCommand,
    UpdateTipoSeguroCommand,
    TipoSeguroDto,
    TipoSeguroSummaryDto
)

# Importamos los casos de uso
from src.features.tipos_seguros.application.use_cases import (
    CrearTipoSeguroUseCase,
    ObtenerTipoSeguroUseCase,
    ObtenerTipoSeguroPorCodigoUseCase,
    ListarTiposSeguroUseCase,
    ListarTiposSeguroPorAseguradoraUseCase,
    ActualizarTipoSeguroUseCase,
    EliminarTipoSeguroUseCase
)

# Importamos los repositorios concretos
from src.features.tipos_seguros.infrastructure.repositories import SQLAlchemyTipoSeguroRepository
from src.features.aseguradoras.infrastructure.repositories import SQLAlchemyAseguradoraRepository

# Importamos las dependencias de seguridad (para proteger endpoints)
# from src.infrastructure.security.dependencies import get_current_user, get_admin_user
# from src.features.usuarios.application.dtos import UsuarioDto

# Creamos el router
router = APIRouter(prefix="/tipos-seguro", tags=["Tipos de Seguro"])


@router.post("/", response_model=TipoSeguroDto, status_code=status.HTTP_201_CREATED)
async def crear_tipo_seguro(
    command: CreateTipoSeguroCommand,
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden crear tipos de seguro
):
    """Crea un nuevo tipo de seguro."""
    # Inicializamos los repositorios
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    aseguradora_repository = SQLAlchemyAseguradoraRepository(db)
    
    # Inicializamos el caso de uso
    use_case = CrearTipoSeguroUseCase(
        tipo_seguro_repository,
        aseguradora_repository
    )
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(command)
    except ValueError as e:
        # Manejo de errores de validación
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear tipo de seguro: {str(e)}"
        )


@router.get("/", response_model=List[TipoSeguroSummaryDto])
async def listar_tipos_seguro(
    aseguradora_id: Optional[int] = Query(None, description="ID de la aseguradora para filtrar tipos de seguro"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar tipos de seguro
):
    """Lista todos los tipos de seguro o filtra por aseguradora."""
    # Inicializamos el repositorio
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    
    try:
        if aseguradora_id:
            # Listar tipos de seguro por aseguradora
            use_case = ListarTiposSeguroPorAseguradoraUseCase(tipo_seguro_repository)
            return use_case.execute(aseguradora_id)
        else:
            # Listar todos los tipos de seguro
            use_case = ListarTiposSeguroUseCase(tipo_seguro_repository)
            return use_case.execute()
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar tipos de seguro: {str(e)}"
        )


@router.get("/{tipo_seguro_id}", response_model=TipoSeguroDto)
async def obtener_tipo_seguro(
    tipo_seguro_id: int = Path(..., description="ID del tipo de seguro a obtener"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver tipos de seguro
):
    """Obtiene un tipo de seguro por su ID."""
    # Inicializamos el repositorio
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerTipoSeguroUseCase(tipo_seguro_repository)
    
    # Ejecutamos el caso de uso
    tipo_seguro = use_case.execute(tipo_seguro_id)
    
    if not tipo_seguro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de seguro con ID {tipo_seguro_id} no encontrado"
        )
    
    return tipo_seguro


@router.get("/codigo/{codigo}", response_model=TipoSeguroDto)
async def obtener_tipo_seguro_por_codigo(
    codigo: str = Path(..., description="Código del tipo de seguro a obtener"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver tipos de seguro
):
    """Obtiene un tipo de seguro por su código."""
    # Inicializamos el repositorio
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ObtenerTipoSeguroPorCodigoUseCase(tipo_seguro_repository)
    
    # Ejecutamos el caso de uso
    tipo_seguro = use_case.execute(codigo.upper())
    
    if not tipo_seguro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de seguro con código {codigo} no encontrado"
        )
    
    return tipo_seguro


@router.put("/{tipo_seguro_id}", response_model=TipoSeguroDto)
async def actualizar_tipo_seguro(
    tipo_seguro_id: int = Path(..., description="ID del tipo de seguro a actualizar"),
    command: UpdateTipoSeguroCommand = None,
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden actualizar tipos de seguro
):
    """Actualiza un tipo de seguro existente."""
    # Aseguramos que el ID en el path coincida con el ID en el comando
    if command.id != tipo_seguro_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID en la URL no coincide con el ID en el cuerpo de la solicitud"
        )
    
    # Inicializamos los repositorios
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    aseguradora_repository = SQLAlchemyAseguradoraRepository(db)
    
    # Inicializamos el caso de uso
    use_case = ActualizarTipoSeguroUseCase(
        tipo_seguro_repository,
        aseguradora_repository
    )
    
    try:
        # Ejecutamos el caso de uso
        return use_case.execute(command)
    except ValueError as e:
        # Manejo de errores de validación
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar tipo de seguro: {str(e)}"
        )


@router.delete("/{tipo_seguro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_tipo_seguro(
    tipo_seguro_id: int = Path(..., description="ID del tipo de seguro a eliminar"),
    db: Session = Depends(get_db),
    # current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar tipos de seguro
):
    """Elimina un tipo de seguro."""
    # Inicializamos el repositorio
    tipo_seguro_repository = SQLAlchemyTipoSeguroRepository(db)
    
    # Inicializamos el caso de uso
    use_case = EliminarTipoSeguroUseCase(tipo_seguro_repository)
    
    try:
        # Ejecutamos el caso de uso
        use_case.execute(tipo_seguro_id)
        return None  # 204 No Content
    except ValueError as e:
        # Manejo de errores de validación
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar tipo de seguro: {str(e)}"
        )
