from datetime import datetime, timezone
from typing import List, Optional

# Importamos la interfaz del repositorio
from src.features.tipos_seguros.application.interfaces.repositories import AbstractTipoSeguroRepository
# Importamos la entidad de dominio
from src.features.tipos_seguros.domain.entities import TipoSeguro
# Importamos los DTOs
from src.features.tipos_seguros.application.dtos import (
    CreateTipoSeguroCommand,
    UpdateTipoSeguroCommand,
    TipoSeguroDto,
    TipoSeguroSummaryDto
)

# Importamos el repositorio de aseguradoras
from src.features.aseguradoras.application.interfaces.repositories import AbstractAseguradoraRepository


def get_utc_now():
    """Funciu00f3n helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)


class CrearTipoSeguroUseCase:
    """Caso de uso para crear un nuevo tipo de seguro."""
    
    def __init__(
        self,
        tipo_seguro_repository: AbstractTipoSeguroRepository,
        aseguradora_repository: AbstractAseguradoraRepository
    ):
        self.tipo_seguro_repository = tipo_seguro_repository
        self.aseguradora_repository = aseguradora_repository
    
    def execute(self, command: CreateTipoSeguroCommand) -> TipoSeguroDto:
        # Verificar que la aseguradora existe
        aseguradora = self.aseguradora_repository.get_by_id(command.aseguradora_id)
        if not aseguradora:
            raise ValueError(f"Aseguradora con ID {command.aseguradora_id} no encontrada")
        
        # Verificar que el cu00f3digo no estu00e9 duplicado
        existing_tipo_seguro = self.tipo_seguro_repository.get_by_codigo(command.codigo)
        if existing_tipo_seguro:
            raise ValueError(f"Ya existe un tipo de seguro con el cu00f3digo {command.codigo}")
        
        # Crear la entidad de dominio
        now = get_utc_now()
        tipo_seguro = TipoSeguro(
            codigo=command.codigo,
            nombre=command.nombre,
            descripcion=command.descripcion,
            es_default=command.es_default,
            esta_activo=command.esta_activo,
            categoria=command.categoria,
            cobertura=command.cobertura,
            vigencia_default=command.vigencia_default,
            aseguradora=aseguradora,
            fecha_creacion=now,
            fecha_actualizacion=now
        )
        
        # Persistir la entidad
        self.tipo_seguro_repository.add(tipo_seguro)
        
        # Obtener la entidad persistida y convertirla a DTO
        return self._to_dto(tipo_seguro)
    
    def _to_dto(self, tipo_seguro: TipoSeguro) -> TipoSeguroDto:
        # Convertir la entidad a DTO
        from src.features.aseguradoras.application.dtos import AseguradoraDto
        
        return TipoSeguroDto(
            id=tipo_seguro.id,
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            descripcion=tipo_seguro.descripcion,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            categoria=tipo_seguro.categoria,
            cobertura=tipo_seguro.cobertura,
            vigencia_default=tipo_seguro.vigencia_default,
            aseguradora=AseguradoraDto(
                id=tipo_seguro.aseguradora.id,
                codigo=tipo_seguro.aseguradora.codigo,
                nombre=tipo_seguro.aseguradora.nombre,
                direccion=tipo_seguro.aseguradora.direccion,
                telefono=tipo_seguro.aseguradora.telefono,
                email=tipo_seguro.aseguradora.email,
                sitio_web=tipo_seguro.aseguradora.sitio_web,
                esta_activo=tipo_seguro.aseguradora.esta_activo,
                fecha_creacion=tipo_seguro.aseguradora.fecha_creacion,
                fecha_actualizacion=tipo_seguro.aseguradora.fecha_actualizacion
            ),
            fecha_creacion=tipo_seguro.fecha_creacion,
            fecha_actualizacion=tipo_seguro.fecha_actualizacion
        )


class ObtenerTipoSeguroUseCase:
    """Caso de uso para obtener un tipo de seguro por su ID."""
    
    def __init__(self, tipo_seguro_repository: AbstractTipoSeguroRepository):
        self.tipo_seguro_repository = tipo_seguro_repository
    
    def execute(self, tipo_seguro_id: int) -> Optional[TipoSeguroDto]:
        tipo_seguro = self.tipo_seguro_repository.get_by_id(tipo_seguro_id)
        if not tipo_seguro:
            return None
        
        return self._to_dto(tipo_seguro)
    
    def _to_dto(self, tipo_seguro: TipoSeguro) -> TipoSeguroDto:
        # Convertir la entidad a DTO
        from src.features.aseguradoras.application.dtos import AseguradoraDto
        
        return TipoSeguroDto(
            id=tipo_seguro.id,
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            descripcion=tipo_seguro.descripcion,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            categoria=tipo_seguro.categoria,
            cobertura=tipo_seguro.cobertura,
            vigencia_default=tipo_seguro.vigencia_default,
            aseguradora=AseguradoraDto(
                id=tipo_seguro.aseguradora.id,
                codigo=tipo_seguro.aseguradora.codigo,
                nombre=tipo_seguro.aseguradora.nombre,
                direccion=tipo_seguro.aseguradora.direccion,
                telefono=tipo_seguro.aseguradora.telefono,
                email=tipo_seguro.aseguradora.email,
                sitio_web=tipo_seguro.aseguradora.sitio_web,
                esta_activo=tipo_seguro.aseguradora.esta_activo,
                fecha_creacion=tipo_seguro.aseguradora.fecha_creacion,
                fecha_actualizacion=tipo_seguro.aseguradora.fecha_actualizacion
            ),
            fecha_creacion=tipo_seguro.fecha_creacion,
            fecha_actualizacion=tipo_seguro.fecha_actualizacion
        )


class ObtenerTipoSeguroPorCodigoUseCase:
    """Caso de uso para obtener un tipo de seguro por su cu00f3digo."""
    
    def __init__(self, tipo_seguro_repository: AbstractTipoSeguroRepository):
        self.tipo_seguro_repository = tipo_seguro_repository
    
    def execute(self, codigo: str) -> Optional[TipoSeguroDto]:
        tipo_seguro = self.tipo_seguro_repository.get_by_codigo(codigo)
        if not tipo_seguro:
            return None
        
        return self._to_dto(tipo_seguro)
    
    def _to_dto(self, tipo_seguro: TipoSeguro) -> TipoSeguroDto:
        # Convertir la entidad a DTO
        from src.features.aseguradoras.application.dtos import AseguradoraDto
        
        return TipoSeguroDto(
            id=tipo_seguro.id,
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            descripcion=tipo_seguro.descripcion,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            categoria=tipo_seguro.categoria,
            cobertura=tipo_seguro.cobertura,
            vigencia_default=tipo_seguro.vigencia_default,
            aseguradora=AseguradoraDto(
                id=tipo_seguro.aseguradora.id,
                codigo=tipo_seguro.aseguradora.codigo,
                nombre=tipo_seguro.aseguradora.nombre,
                direccion=tipo_seguro.aseguradora.direccion,
                telefono=tipo_seguro.aseguradora.telefono,
                email=tipo_seguro.aseguradora.email,
                sitio_web=tipo_seguro.aseguradora.sitio_web,
                esta_activo=tipo_seguro.aseguradora.esta_activo,
                fecha_creacion=tipo_seguro.aseguradora.fecha_creacion,
                fecha_actualizacion=tipo_seguro.aseguradora.fecha_actualizacion
            ),
            fecha_creacion=tipo_seguro.fecha_creacion,
            fecha_actualizacion=tipo_seguro.fecha_actualizacion
        )


class ListarTiposSeguroUseCase:
    """Caso de uso para listar todos los tipos de seguro."""
    
    def __init__(self, tipo_seguro_repository: AbstractTipoSeguroRepository):
        self.tipo_seguro_repository = tipo_seguro_repository
    
    def execute(self) -> List[TipoSeguroSummaryDto]:
        tipos_seguro = self.tipo_seguro_repository.get_all()
        return [self._to_summary_dto(tipo_seguro) for tipo_seguro in tipos_seguro]
    
    def _to_summary_dto(self, tipo_seguro: TipoSeguro) -> TipoSeguroSummaryDto:
        # Convertir la entidad a DTO resumido
        return TipoSeguroSummaryDto(
            id=tipo_seguro.id,
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            categoria=tipo_seguro.categoria,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            aseguradora_id=tipo_seguro.aseguradora.id,
            aseguradora_nombre=tipo_seguro.aseguradora.nombre
        )


class ListarTiposSeguroPorAseguradoraUseCase:
    """Caso de uso para listar tipos de seguro por aseguradora."""
    
    def __init__(self, tipo_seguro_repository: AbstractTipoSeguroRepository):
        self.tipo_seguro_repository = tipo_seguro_repository
    
    def execute(self, aseguradora_id: int) -> List[TipoSeguroSummaryDto]:
        tipos_seguro = self.tipo_seguro_repository.get_by_aseguradora(aseguradora_id)
        return [self._to_summary_dto(tipo_seguro) for tipo_seguro in tipos_seguro]
    
    def _to_summary_dto(self, tipo_seguro: TipoSeguro) -> TipoSeguroSummaryDto:
        # Convertir la entidad a DTO resumido
        return TipoSeguroSummaryDto(
            id=tipo_seguro.id,
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            categoria=tipo_seguro.categoria,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            aseguradora_id=tipo_seguro.aseguradora.id,
            aseguradora_nombre=tipo_seguro.aseguradora.nombre
        )


class ActualizarTipoSeguroUseCase:
    """Caso de uso para actualizar un tipo de seguro existente."""
    
    def __init__(
        self,
        tipo_seguro_repository: AbstractTipoSeguroRepository,
        aseguradora_repository: AbstractAseguradoraRepository
    ):
        self.tipo_seguro_repository = tipo_seguro_repository
        self.aseguradora_repository = aseguradora_repository
    
    def execute(self, command: UpdateTipoSeguroCommand) -> TipoSeguroDto:
        # Verificar que el tipo de seguro existe
        tipo_seguro = self.tipo_seguro_repository.get_by_id(command.id)
        if not tipo_seguro:
            raise ValueError(f"Tipo de seguro con ID {command.id} no encontrado")
        
        # Verificar que la aseguradora existe
        aseguradora = self.aseguradora_repository.get_by_id(command.aseguradora_id)
        if not aseguradora:
            raise ValueError(f"Aseguradora con ID {command.aseguradora_id} no encontrada")
        
        # Verificar que el cu00f3digo no estu00e9 duplicado (si se cambia)
        if command.codigo != tipo_seguro.codigo:
            existing_tipo_seguro = self.tipo_seguro_repository.get_by_codigo(command.codigo)
            if existing_tipo_seguro and existing_tipo_seguro.id != command.id:
                raise ValueError(f"Ya existe un tipo de seguro con el cu00f3digo {command.codigo}")
        
        # Actualizar la entidad de dominio
        tipo_seguro.codigo = command.codigo
        tipo_seguro.nombre = command.nombre
        tipo_seguro.descripcion = command.descripcion
        tipo_seguro.es_default = command.es_default
        tipo_seguro.esta_activo = command.esta_activo
        tipo_seguro.categoria = command.categoria
        tipo_seguro.cobertura = command.cobertura
        tipo_seguro.vigencia_default = command.vigencia_default
        tipo_seguro.aseguradora = aseguradora
        tipo_seguro.fecha_actualizacion = get_utc_now()
        
        # Persistir la entidad actualizada
        self.tipo_seguro_repository.update(tipo_seguro)
        
        # Obtener la entidad actualizada y convertirla a DTO
        return self._to_dto(tipo_seguro)
    
    def _to_dto(self, tipo_seguro: TipoSeguro) -> TipoSeguroDto:
        # Convertir la entidad a DTO
        from src.features.aseguradoras.application.dtos import AseguradoraDto
        
        return TipoSeguroDto(
            id=tipo_seguro.id,
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            descripcion=tipo_seguro.descripcion,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            categoria=tipo_seguro.categoria,
            cobertura=tipo_seguro.cobertura,
            vigencia_default=tipo_seguro.vigencia_default,
            aseguradora=AseguradoraDto(
                id=tipo_seguro.aseguradora.id,
                codigo=tipo_seguro.aseguradora.codigo,
                nombre=tipo_seguro.aseguradora.nombre,
                direccion=tipo_seguro.aseguradora.direccion,
                telefono=tipo_seguro.aseguradora.telefono,
                email=tipo_seguro.aseguradora.email,
                sitio_web=tipo_seguro.aseguradora.sitio_web,
                esta_activo=tipo_seguro.aseguradora.esta_activo,
                fecha_creacion=tipo_seguro.aseguradora.fecha_creacion,
                fecha_actualizacion=tipo_seguro.aseguradora.fecha_actualizacion
            ),
            fecha_creacion=tipo_seguro.fecha_creacion,
            fecha_actualizacion=tipo_seguro.fecha_actualizacion
        )


class EliminarTipoSeguroUseCase:
    """Caso de uso para eliminar un tipo de seguro."""
    
    def __init__(self, tipo_seguro_repository: AbstractTipoSeguroRepository):
        self.tipo_seguro_repository = tipo_seguro_repository
    
    def execute(self, tipo_seguro_id: int) -> None:
        # Verificar que el tipo de seguro existe
        tipo_seguro = self.tipo_seguro_repository.get_by_id(tipo_seguro_id)
        if not tipo_seguro:
            raise ValueError(f"Tipo de seguro con ID {tipo_seguro_id} no encontrado")
        
        # Eliminar la entidad
        self.tipo_seguro_repository.delete(tipo_seguro_id)