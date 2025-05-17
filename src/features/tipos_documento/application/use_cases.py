from src.features.tipos_documento.domain.entities import TipoDocumento
from src.features.tipos_documento.application.dtos import (
    TipoDocumentoDto, 
    CrearTipoDocumentoCommand, 
    ActualizarTipoDocumentoCommand
)
from src.features.tipos_documento.application.interfaces.repositories import AbstractTipoDocumentoRepository


class ObtenerTipoDocumentoUseCase:
    """Caso de uso para obtener un tipo de documento por su ID."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self, tipo_id: int) -> TipoDocumentoDto:
        """Obtiene un tipo de documento por su ID."""
        tipo_documento = self.tipo_documento_repository.get_by_id(tipo_id)
        if not tipo_documento:
            return None
        return TipoDocumentoDto.model_validate(tipo_documento)


class ObtenerTipoDocumentoPorCodigoUseCase:
    """Caso de uso para obtener un tipo de documento por su cu00f3digo."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self, codigo: str) -> TipoDocumentoDto:
        """Obtiene un tipo de documento por su cu00f3digo."""
        tipo_documento = self.tipo_documento_repository.get_by_codigo(codigo)
        if not tipo_documento:
            return None
        return TipoDocumentoDto.model_validate(tipo_documento)


class ObtenerTipoDocumentoDefaultUseCase:
    """Caso de uso para obtener el tipo de documento marcado como default."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self) -> TipoDocumentoDto:
        """Obtiene el tipo de documento marcado como default."""
        tipo_documento = self.tipo_documento_repository.get_default()
        if not tipo_documento:
            return None
        return TipoDocumentoDto.model_validate(tipo_documento)


class ListarTiposDocumentoUseCase:
    """Caso de uso para listar todos los tipos de documento."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self) -> list[TipoDocumentoDto]:
        """Lista todos los tipos de documento activos."""
        tipos_documento = self.tipo_documento_repository.get_all()
        return [TipoDocumentoDto.model_validate(tipo) for tipo in tipos_documento]


class CrearTipoDocumentoUseCase:
    """Caso de uso para crear un nuevo tipo de documento."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self, command: CrearTipoDocumentoCommand) -> TipoDocumentoDto:
        """Crea un nuevo tipo de documento."""
        # Verificar si ya existe un tipo de documento con el mismo cu00f3digo
        existing = self.tipo_documento_repository.get_by_codigo(command.codigo)
        if existing:
            raise ValueError(f"Ya existe un tipo de documento con el cu00f3digo '{command.codigo}'")
        
        # Si es_default es True, desactivar cualquier otro tipo de documento por defecto
        if command.es_default:
            default_tipo = self.tipo_documento_repository.get_default()
            if default_tipo:
                default_tipo.es_default = False
                self.tipo_documento_repository.update(default_tipo)
        
        # Crear el nuevo tipo de documento
        nuevo_tipo = TipoDocumento(
            id=0,  # El ID seru00e1 asignado por la base de datos
            codigo=command.codigo,
            nombre=command.nombre,
            descripcion=command.descripcion,
            es_default=command.es_default,
            esta_activo=command.esta_activo
        )
        
        created_tipo = self.tipo_documento_repository.add(nuevo_tipo)
        return TipoDocumentoDto.model_validate(created_tipo)


class ActualizarTipoDocumentoUseCase:
    """Caso de uso para actualizar un tipo de documento existente."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self, tipo_id: int, command: ActualizarTipoDocumentoCommand) -> TipoDocumentoDto:
        """Actualiza un tipo de documento existente."""
        # Obtener el tipo de documento existente
        tipo_documento = self.tipo_documento_repository.get_by_id(tipo_id)
        if not tipo_documento:
            raise ValueError(f"No se encontru00f3 un tipo de documento con ID {tipo_id}")
        
        # Verificar si se estu00e1 cambiando el cu00f3digo y si el nuevo cu00f3digo ya existe
        if command.codigo and command.codigo != tipo_documento.codigo:
            existing = self.tipo_documento_repository.get_by_codigo(command.codigo)
            if existing and existing.id != tipo_id:
                raise ValueError(f"Ya existe un tipo de documento con el cu00f3digo '{command.codigo}'")
        
        # Si es_default es True, desactivar cualquier otro tipo de documento por defecto
        if command.es_default and command.es_default != tipo_documento.es_default:
            default_tipo = self.tipo_documento_repository.get_default()
            if default_tipo and default_tipo.id != tipo_id:
                default_tipo.es_default = False
                self.tipo_documento_repository.update(default_tipo)
        
        # Actualizar los campos
        if command.codigo is not None:
            tipo_documento.codigo = command.codigo
        if command.nombre is not None:
            tipo_documento.nombre = command.nombre
        if command.descripcion is not None:
            tipo_documento.descripcion = command.descripcion
        if command.es_default is not None:
            tipo_documento.es_default = command.es_default
        if command.esta_activo is not None:
            tipo_documento.esta_activo = command.esta_activo
        
        updated_tipo = self.tipo_documento_repository.update(tipo_documento)
        return TipoDocumentoDto.model_validate(updated_tipo)


class EliminarTipoDocumentoUseCase:
    """Caso de uso para eliminar un tipo de documento (marcarlo como inactivo)."""
    
    def __init__(self, tipo_documento_repository: AbstractTipoDocumentoRepository):
        self.tipo_documento_repository = tipo_documento_repository
    
    def execute(self, tipo_id: int) -> bool:
        """Elimina un tipo de documento (marcu00e1ndolo como inactivo)."""
        # Obtener el tipo de documento existente
        tipo_documento = self.tipo_documento_repository.get_by_id(tipo_id)
        if not tipo_documento:
            raise ValueError(f"No se encontru00f3 un tipo de documento con ID {tipo_id}")
        
        # No permitir eliminar el tipo de documento por defecto
        if tipo_documento.es_default:
            raise ValueError("No se puede eliminar el tipo de documento por defecto")
        
        # Marcar como inactivo
        return self.tipo_documento_repository.delete(tipo_id)
