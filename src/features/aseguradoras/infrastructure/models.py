from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from src.infrastructure.database import Base
from src.infrastructure.utils.datetime import get_utc_now


class Aseguradora(Base):
    """Modelo para la tabla aseguradoras."""

    __tablename__ = "aseguradoras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    identificador_fiscal = Column(
        String(12),
        unique=True,
        comment="Identificador fiscal de la aseguradora (RUT, CUIT, NIF, etc.)",
    )
    telefono = Column(String(20))
    direccion = Column(String(200))
    email = Column(String(100))
    pagina_web = Column(String(100))
    esta_activa = Column(Boolean, default=True)
    observaciones = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_actualizacion = Column(
        DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now
    )

    # Relación con tipos de seguros
    tipos_seguros = relationship("TipoSeguro", back_populates="aseguradora_rel")
