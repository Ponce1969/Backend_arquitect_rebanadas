from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.features.tipos_documento.application.dtos import (
    TipoDocumentoDto, TipoDocumentoSummaryDto, CrearTipoDocumentoCommand, ActualizarTipoDocumentoCommand
)
from src.features.tipos_documento.application.use_cases import (
    ListarTiposDocumentoUseCase, ObtenerTipoDocumentoUseCase, ObtenerTipoDocumentoPorCodigoUseCase,
    ObtenerTipoDocumentoDefaultUseCase, CrearTipoDocumentoUseCase, ActualizarTipoDocumentoUseCase,
    EliminarTipoDocumentoUseCase
)
from src.features.tipos_documento.infrastructure.repositories import SQLAlchemyTipoDocumentoRepository
from src.infrastructure.database import get_db
from src.infrastructure.security.dependencies import get_current_user, get_admin_user
from src.features.usuarios.application.dtos import UsuarioDto


router = APIRouter(prefix="/tipos-documento", tags=["Tipos de Documento"])


# Dependencias para inyección
def get_tipo_documento_repository(db: Session = Depends(get_db)):
    return SQLAlchemyTipoDocumentoRepository(db)


def get_listar_tipos_documento_use_case(repo = Depends(get_tipo_documento_repository)):
    return ListarTiposDocumentoUseCase(repo)


def get_obtener_tipo_documento_use_case(repo = Depends(get_tipo_documento_repository)):
    return ObtenerTipoDocumentoUseCase(repo)


def get_obtener_tipo_documento_por_codigo_use_case(repo = Depends(get_tipo_documento_repository)):
    return ObtenerTipoDocumentoPorCodigoUseCase(repo)


def get_obtener_tipo_documento_default_use_case(repo = Depends(get_tipo_documento_repository)):
    return ObtenerTipoDocumentoDefaultUseCase(repo)


def get_crear_tipo_documento_use_case(repo = Depends(get_tipo_documento_repository)):
    return CrearTipoDocumentoUseCase(repo)


def get_actualizar_tipo_documento_use_case(repo = Depends(get_tipo_documento_repository)):
    return ActualizarTipoDocumentoUseCase(repo)


def get_eliminar_tipo_documento_use_case(repo = Depends(get_tipo_documento_repository)):
    return EliminarTipoDocumentoUseCase(repo)


# Endpoints
@router.get("/", response_model=list[TipoDocumentoSummaryDto])
async def listar_tipos_documento(
    use_case = Depends(get_listar_tipos_documento_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden listar tipos de documento
):
    """Lista todos los tipos de documento activos."""
    return use_case.execute()


@router.get("/{tipo_id}", response_model=TipoDocumentoDto)
async def obtener_tipo_documento(
    tipo_id: int, 
    use_case = Depends(get_obtener_tipo_documento_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver tipos de documento
):
    """Obtiene un tipo de documento por su ID."""
    tipo = use_case.execute(tipo_id)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el tipo de documento con ID {tipo_id}"
        )
    return tipo


@router.get("/codigo/{codigo}", response_model=TipoDocumentoDto)
async def obtener_tipo_documento_por_codigo(
    codigo: str, 
    use_case = Depends(get_obtener_tipo_documento_por_codigo_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver tipos de documento
):
    """Obtiene un tipo de documento por su codigo."""
    tipo = use_case.execute(codigo)
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el tipo de documento con codigo {codigo}"
        )
    return tipo


@router.get("/default", response_model=TipoDocumentoDto)
async def obtener_tipo_documento_default(
    use_case = Depends(get_obtener_tipo_documento_default_use_case),
    current_user: UsuarioDto = Depends(get_current_user)  # Solo usuarios autenticados pueden ver tipos de documento
):
    """Obtiene el tipo de documento marcado como default."""
    tipo = use_case.execute()
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró un tipo de documento marcado como default"
        )
    return tipo


@router.post("/", response_model=TipoDocumentoDto, status_code=status.HTTP_201_CREATED)
async def crear_tipo_documento(
    command: CrearTipoDocumentoCommand, 
    use_case = Depends(get_crear_tipo_documento_use_case),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden crear tipos de documento
):
    """Crea un nuevo tipo de documento."""
    try:
        return use_case.execute(command)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{tipo_id}", response_model=TipoDocumentoDto)
async def actualizar_tipo_documento(
    tipo_id: int, 
    command: ActualizarTipoDocumentoCommand, 
    use_case = Depends(get_actualizar_tipo_documento_use_case),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden actualizar tipos de documento
):
    """Actualiza un tipo de documento existente."""
    try:
        tipo = use_case.execute(tipo_id, command)
        if not tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el tipo de documento con ID {tipo_id}"
            )
        return tipo
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{tipo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_tipo_documento(
    tipo_id: int, 
    use_case = Depends(get_eliminar_tipo_documento_use_case),
    current_user: UsuarioDto = Depends(get_admin_user)  # Solo administradores pueden eliminar tipos de documento
):
    """Elimina un tipo de documento (marcandolo como inactivo)."""
    try:
        success = use_case.execute(tipo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el tipo de documento con ID {tipo_id}"
            )
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
