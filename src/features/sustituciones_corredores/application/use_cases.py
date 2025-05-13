from datetime import date
from typing import List, Optional

from .dtos import (
    FinalizarSustitucionRequest,
    SustitucionCorredorCreate,
    SustitucionCorredorResponse,
    SustitucionCorredorUpdate
)
from .interfaces.repositories import AbstractSustitucionCorredorRepository
from ..domain.entities import SustitucionCorredor as SustitucionCorredorDomain
from ..domain.exceptions import (
    SustitucionCorredorNotFoundException,
    SustitucionCorredorSolapamientoException,
    CorredorAusenteNotFoundException,
    CorredorSustitutoNotFoundException
)


class CrearSustitucionCorredorUseCase:
    """Caso de uso para crear una nueva sustitución de corredor."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, sustitucion_data: SustitucionCorredorCreate) -> SustitucionCorredorResponse:
        # Verificar que el corredor ausente y el sustituto existan
        # En un caso real, aquí verificaríamos que los corredores existan en la base de datos
        # Si no existen, lanzaríamos las excepciones correspondientes:
        # if not corredor_ausente_exists:
        #    raise CorredorAusenteNotFoundException(sustitucion_data.corredor_ausente_numero)
        # if not corredor_sustituto_exists:
        #    raise CorredorSustitutoNotFoundException(sustitucion_data.corredor_sustituto_numero)
        
        # Verificar que no haya otra sustitución activa para el mismo corredor ausente
        sustituciones_activas = self.repository.get_activas_by_corredor_ausente(
            sustitucion_data.corredor_ausente_numero
        )
        
        if sustituciones_activas:
            raise SustitucionCorredorSolapamientoException(
                sustitucion_data.corredor_ausente_numero,
                sustitucion_data.fecha_inicio.isoformat(),
                sustitucion_data.fecha_fin.isoformat() if sustitucion_data.fecha_fin else "indefinida"
            )
        
        # Crear la entidad de dominio
        sustitucion = SustitucionCorredorDomain(
            corredor_ausente_numero=sustitucion_data.corredor_ausente_numero,
            corredor_sustituto_numero=sustitucion_data.corredor_sustituto_numero,
            fecha_inicio=sustitucion_data.fecha_inicio,
            fecha_fin=sustitucion_data.fecha_fin,
            estado=sustitucion_data.estado,
            motivo=sustitucion_data.motivo,
            observaciones=sustitucion_data.observaciones
        )
        
        # Guardar la sustitución en el repositorio
        new_sustitucion = self.repository.add(sustitucion)
        
        # Convertir la entidad de dominio a DTO de respuesta
        return SustitucionCorredorResponse(
            id=new_sustitucion.id,
            corredor_ausente_numero=new_sustitucion.corredor_ausente_numero,
            corredor_sustituto_numero=new_sustitucion.corredor_sustituto_numero,
            fecha_inicio=new_sustitucion.fecha_inicio,
            fecha_fin=new_sustitucion.fecha_fin,
            estado=new_sustitucion.estado,
            motivo=new_sustitucion.motivo,
            observaciones=new_sustitucion.observaciones,
            fecha_creacion=new_sustitucion.fecha_creacion,
            fecha_actualizacion=new_sustitucion.fecha_actualizacion
        )


class ObtenerSustitucionCorredorPorIdUseCase:
    """Caso de uso para obtener una sustitución de corredor por su ID."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, sustitucion_id: int) -> Optional[SustitucionCorredorResponse]:
        sustitucion = self.repository.get_by_id(sustitucion_id)
        if not sustitucion:
            return None
        
        return SustitucionCorredorResponse(
            id=sustitucion.id,
            corredor_ausente_numero=sustitucion.corredor_ausente_numero,
            corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
            fecha_inicio=sustitucion.fecha_inicio,
            fecha_fin=sustitucion.fecha_fin,
            estado=sustitucion.estado,
            motivo=sustitucion.motivo,
            observaciones=sustitucion.observaciones,
            fecha_creacion=sustitucion.fecha_creacion,
            fecha_actualizacion=sustitucion.fecha_actualizacion
        )


class ListarSustitucionesCorredorUseCase:
    """Caso de uso para listar todas las sustituciones de corredores."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self) -> List[SustitucionCorredorResponse]:
        sustituciones = self.repository.get_all()
        return [
            SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
            for sustitucion in sustituciones
        ]


class ListarSustitucionesActivasUseCase:
    """Caso de uso para listar todas las sustituciones activas."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, fecha: date = None) -> List[SustitucionCorredorResponse]:
        sustituciones = self.repository.get_activas(fecha)
        return [
            SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
            for sustitucion in sustituciones
        ]


class ObtenerSustitucionesPorCorredorAusenteUseCase:
    """Caso de uso para obtener las sustituciones donde un corredor está ausente."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, corredor_numero: int) -> List[SustitucionCorredorResponse]:
        sustituciones = self.repository.get_by_corredor_ausente(corredor_numero)
        return [
            SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
            for sustitucion in sustituciones
        ]


class ObtenerSustitucionesPorCorredorSustitutoUseCase:
    """Caso de uso para obtener las sustituciones donde un corredor es sustituto."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, corredor_numero: int) -> List[SustitucionCorredorResponse]:
        sustituciones = self.repository.get_by_corredor_sustituto(corredor_numero)
        return [
            SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
            for sustitucion in sustituciones
        ]


class ObtenerSustitucionesActivasPorCorredorAusenteUseCase:
    """Caso de uso para obtener las sustituciones activas donde un corredor está ausente."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, corredor_numero: int, fecha: date = None) -> List[SustitucionCorredorResponse]:
        sustituciones = self.repository.get_activas_by_corredor_ausente(corredor_numero, fecha)
        return [
            SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
            for sustitucion in sustituciones
        ]


class ObtenerSustitucionesActivasPorCorredorSustitutoUseCase:
    """Caso de uso para obtener las sustituciones activas donde un corredor es sustituto."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, corredor_numero: int, fecha: date = None) -> List[SustitucionCorredorResponse]:
        sustituciones = self.repository.get_activas_by_corredor_sustituto(corredor_numero, fecha)
        return [
            SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
            for sustitucion in sustituciones
        ]


class ActualizarSustitucionCorredorUseCase:
    """Caso de uso para actualizar una sustitución de corredor existente."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, sustitucion_id: int, sustitucion_data: SustitucionCorredorUpdate) -> SustitucionCorredorResponse:
        # Verificar si la sustitución existe
        sustitucion = self.repository.get_by_id(sustitucion_id)
        if not sustitucion:
            raise SustitucionCorredorNotFoundException(sustitucion_id)
        
        # Actualizar los campos de la sustitución
        if sustitucion_data.corredor_sustituto_numero is not None:
            sustitucion.corredor_sustituto_numero = sustitucion_data.corredor_sustituto_numero
        
        if sustitucion_data.fecha_inicio is not None:
            sustitucion.fecha_inicio = sustitucion_data.fecha_inicio
        
        if sustitucion_data.fecha_fin is not None:
            sustitucion.fecha_fin = sustitucion_data.fecha_fin
        
        if sustitucion_data.estado is not None:
            sustitucion.estado = sustitucion_data.estado
        
        if sustitucion_data.motivo is not None:
            sustitucion.motivo = sustitucion_data.motivo
        
        if sustitucion_data.observaciones is not None:
            sustitucion.observaciones = sustitucion_data.observaciones
        
        # Guardar los cambios en el repositorio
        updated_sustitucion = self.repository.update(sustitucion)
        
        # Convertir la entidad de dominio a DTO de respuesta
        return SustitucionCorredorResponse(
            id=updated_sustitucion.id,
            corredor_ausente_numero=updated_sustitucion.corredor_ausente_numero,
            corredor_sustituto_numero=updated_sustitucion.corredor_sustituto_numero,
            fecha_inicio=updated_sustitucion.fecha_inicio,
            fecha_fin=updated_sustitucion.fecha_fin,
            estado=updated_sustitucion.estado,
            motivo=updated_sustitucion.motivo,
            observaciones=updated_sustitucion.observaciones,
            fecha_creacion=updated_sustitucion.fecha_creacion,
            fecha_actualizacion=updated_sustitucion.fecha_actualizacion
        )


class EliminarSustitucionCorredorUseCase:
    """Caso de uso para eliminar una sustitución de corredor."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, sustitucion_id: int) -> None:
        sustitucion = self.repository.get_by_id(sustitucion_id)
        if not sustitucion:
            raise SustitucionCorredorNotFoundException(sustitucion_id)
        
        self.repository.delete(sustitucion_id)


class FinalizarSustitucionCorredorUseCase:
    """Caso de uso para finalizar una sustitución de corredor."""

    def __init__(self, repository: AbstractSustitucionCorredorRepository):
        self.repository = repository

    def execute(self, sustitucion_id: int, request: FinalizarSustitucionRequest) -> Optional[SustitucionCorredorResponse]:
        try:
            # Finalizar la sustitución en el repositorio
            sustitucion = self.repository.finalizar(sustitucion_id, request.fecha_fin)
            
            # Si hay observaciones adicionales, actualizar la sustitución
            if request.observaciones:
                sustitucion.observaciones = (sustitucion.observaciones or "") + "\n" + request.observaciones
                sustitucion = self.repository.update(sustitucion)
            
            # Convertir la entidad de dominio a DTO de respuesta
            return SustitucionCorredorResponse(
                id=sustitucion.id,
                corredor_ausente_numero=sustitucion.corredor_ausente_numero,
                corredor_sustituto_numero=sustitucion.corredor_sustituto_numero,
                fecha_inicio=sustitucion.fecha_inicio,
                fecha_fin=sustitucion.fecha_fin,
                estado=sustitucion.estado,
                motivo=sustitucion.motivo,
                observaciones=sustitucion.observaciones,
                fecha_creacion=sustitucion.fecha_creacion,
                fecha_actualizacion=sustitucion.fecha_actualizacion
            )
        except ValueError:
            return None
