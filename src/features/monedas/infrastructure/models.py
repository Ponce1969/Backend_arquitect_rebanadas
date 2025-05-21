from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.infrastructure.database.base import Base
from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.infrastructure.utils.datetime import get_utc_now


class Moneda(Base):
    """Modelo SQLAlchemy para la tabla monedas."""
    __tablename__ = "monedas"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    simbolo = Column(String(5), nullable=False)
    esta_activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_actualizacion = Column(
        DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now
    )
    
    # Relaciones
    # movimientos = relationship("MovimientoVigencia", back_populates="moneda_rel")
    
    # Métodos para mapear entre Modelo SQLAlchemy y Entidad de Dominio
    def to_entity(self) -> MonedaEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        return MonedaEntity(
            id=self.id,
            codigo=self.codigo,
            nombre=self.nombre,
            simbolo=self.simbolo,
            esta_activo=self.esta_activo,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion
        )
    
    @staticmethod
    def from_entity(moneda: MonedaEntity) -> 'Moneda':
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy."""
        return Moneda(
            id=moneda.id,
            codigo=moneda.codigo,
            nombre=moneda.nombre,
            simbolo=moneda.simbolo,
            esta_activo=moneda.esta_activo,
            fecha_creacion=moneda.fecha_creacion,
            fecha_actualizacion=moneda.fecha_actualizacion
        )
