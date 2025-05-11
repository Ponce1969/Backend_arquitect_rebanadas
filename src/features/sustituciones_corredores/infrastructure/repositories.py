from datetime import date
from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from ..application.interfaces.repositories import AbstractSustitucionCorredorRepository
from ..domain.entities import SustitucionCorredor as SustitucionCorredorDomain
from src.features.sustituciones_corredores.infrastructure.models import SustitucionCorredor as SustitucionCorredorModel


class SQLAlchemySustitucionCorredorRepository(AbstractSustitucionCorredorRepository):
    """Implementación SQLAlchemy del repositorio de Sustituciones de Corredores."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, sustitucion: SustitucionCorredorDomain) -> SustitucionCorredorDomain:
        """Agrega una nueva sustitución de corredor al repositorio."""
        db_sustitucion = SustitucionCorredorModel.from_entity(sustitucion)
        self.session.add(db_sustitucion)
        self.session.commit()
        self.session.refresh(db_sustitucion)
        return db_sustitucion.to_entity()

    def get_by_id(self, sustitucion_id: int) -> SustitucionCorredorDomain | None:
        """Obtiene una sustitución por su ID técnico."""
        db_sustitucion = self.session.query(SustitucionCorredorModel).filter(
            SustitucionCorredorModel.id == sustitucion_id
        ).first()
        return db_sustitucion.to_entity() if db_sustitucion else None

    def get_by_corredor_ausente(self, corredor_numero: int) -> list[SustitucionCorredorDomain]:
        """Obtiene todas las sustituciones donde el corredor especificado está ausente."""
        db_sustituciones = self.session.query(SustitucionCorredorModel).filter(
            SustitucionCorredorModel.corredor_ausente_numero == corredor_numero
        ).all()
        return [db_sustitucion.to_entity() for db_sustitucion in db_sustituciones]

    def get_by_corredor_sustituto(self, corredor_numero: int) -> list[SustitucionCorredorDomain]:
        """Obtiene todas las sustituciones donde el corredor especificado es sustituto."""
        db_sustituciones = self.session.query(SustitucionCorredorModel).filter(
            SustitucionCorredorModel.corredor_sustituto_numero == corredor_numero
        ).all()
        return [db_sustitucion.to_entity() for db_sustitucion in db_sustituciones]

    def get_activas_by_corredor_ausente(self, corredor_numero: int, fecha_actual: date | None = None) -> list[SustitucionCorredorDomain]:
        """Obtiene las sustituciones activas donde el corredor especificado está ausente."""
        if fecha_actual is None:
            fecha_actual = date.today()
            
        db_sustituciones = self.session.query(SustitucionCorredorModel).filter(
            and_(
                SustitucionCorredorModel.corredor_ausente_numero == corredor_numero,
                SustitucionCorredorModel.estado == "activa",
                SustitucionCorredorModel.fecha_inicio <= fecha_actual,
                or_(
                    SustitucionCorredorModel.fecha_fin is None,
                    SustitucionCorredorModel.fecha_fin >= fecha_actual
                )
            )
        ).all()
        return [db_sustitucion.to_entity() for db_sustitucion in db_sustituciones]

    def get_activas_by_corredor_sustituto(self, corredor_numero: int, fecha_actual: date | None = None) -> list[SustitucionCorredorDomain]:
        """Obtiene las sustituciones activas donde el corredor especificado es sustituto."""
        if fecha_actual is None:
            fecha_actual = date.today()
            
        db_sustituciones = self.session.query(SustitucionCorredorModel).filter(
            and_(
                SustitucionCorredorModel.corredor_sustituto_numero == corredor_numero,
                SustitucionCorredorModel.estado == "activa",
                SustitucionCorredorModel.fecha_inicio <= fecha_actual,
                or_(
                    SustitucionCorredorModel.fecha_fin is None,
                    SustitucionCorredorModel.fecha_fin >= fecha_actual
                )
            )
        ).all()
        return [db_sustitucion.to_entity() for db_sustitucion in db_sustituciones]

    def get_all(self) -> list[SustitucionCorredorDomain]:
        """Obtiene todas las sustituciones de corredores."""
        db_sustituciones = self.session.query(SustitucionCorredorModel).all()
        return [db_sustitucion.to_entity() for db_sustitucion in db_sustituciones]

    def get_activas(self, fecha_actual: date | None = None) -> list[SustitucionCorredorDomain]:
        """Obtiene todas las sustituciones activas en la fecha actual."""
        if fecha_actual is None:
            fecha_actual = date.today()
            
        db_sustituciones = self.session.query(SustitucionCorredorModel).filter(
            and_(
                SustitucionCorredorModel.estado == "activa",
                SustitucionCorredorModel.fecha_inicio <= fecha_actual,
                or_(
                    SustitucionCorredorModel.fecha_fin is None,
                    SustitucionCorredorModel.fecha_fin >= fecha_actual
                )
            )
        ).all()
        return [db_sustitucion.to_entity() for db_sustitucion in db_sustituciones]

    def update(self, sustitucion: SustitucionCorredorDomain) -> SustitucionCorredorDomain:
        """Actualiza una sustitución existente."""
        db_sustitucion = self.session.query(SustitucionCorredorModel).filter(
            SustitucionCorredorModel.id == sustitucion.id
        ).first()
        
        if db_sustitucion is None:
            raise ValueError(f"No se encontró una sustitución con el ID {sustitucion.id}")
        
        # Actualizar campos
        if sustitucion.corredor_sustituto_numero is not None:
            db_sustitucion.corredor_sustituto_numero = sustitucion.corredor_sustituto_numero
        if sustitucion.fecha_inicio is not None:
            db_sustitucion.fecha_inicio = sustitucion.fecha_inicio
        if sustitucion.fecha_fin is not None:
            db_sustitucion.fecha_fin = sustitucion.fecha_fin
        if sustitucion.estado is not None:
            db_sustitucion.estado = sustitucion.estado
        if sustitucion.motivo is not None:
            db_sustitucion.motivo = sustitucion.motivo
        if sustitucion.observaciones is not None:
            db_sustitucion.observaciones = sustitucion.observaciones
        
        self.session.commit()
        self.session.refresh(db_sustitucion)
        return db_sustitucion.to_entity()

    def delete(self, sustitucion_id: int) -> None:
        """Elimina una sustitución por su ID técnico."""
        db_sustitucion = self.session.query(SustitucionCorredorModel).filter(
            SustitucionCorredorModel.id == sustitucion_id
        ).first()
        
        if db_sustitucion is None:
            raise ValueError(f"No se encontró una sustitución con el ID {sustitucion_id}")
        
        self.session.delete(db_sustitucion)
        self.session.commit()

    def finalizar(self, sustitucion_id: int, fecha_fin: date | None = None) -> SustitucionCorredorDomain:
        """Finaliza una sustitución estableciendo su fecha de fin y cambiando su estado a inactiva."""
        if fecha_fin is None:
            fecha_fin = date.today()
            
        db_sustitucion = self.session.query(SustitucionCorredorModel).filter(
            SustitucionCorredorModel.id == sustitucion_id
        ).first()
        
        if db_sustitucion is None:
            raise ValueError(f"No se encontró una sustitución con el ID {sustitucion_id}")
        
        # Verificar que la fecha de fin sea posterior a la fecha de inicio
        if fecha_fin < db_sustitucion.fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        db_sustitucion.fecha_fin = fecha_fin
        db_sustitucion.estado = "inactiva"
        
        self.session.commit()
        self.session.refresh(db_sustitucion)
        return db_sustitucion.to_entity()
