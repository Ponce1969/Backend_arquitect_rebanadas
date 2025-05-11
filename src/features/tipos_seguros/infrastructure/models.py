from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

# Importamos la Base desde la infraestructura compartida
from src.infrastructure.database.base import Base

# Importamos la Entidad de Dominio TipoSeguro para mapear
from src.features.tipos_seguros.domain.entities import TipoSeguro as TipoSeguroEntity
# Importamos la Entidad de Dominio Aseguradora para mapear
from src.features.aseguradoras.domain.entities import Aseguradora as AseguradoraEntity


# Definición de la función helper para el tiempo
def get_utc_now():
    """Función helper para obtener el tiempo UTC actual en UTC."""
    return datetime.now(timezone.utc)


class TipoSeguro(Base):  # Modelo SQLAlchemy
    """Modelo SQLAlchemy para la tabla tipos_de_seguros."""

    __tablename__ = "tipos_de_seguros"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    es_default = Column(Boolean, default=False)
    esta_activo = Column(Boolean, default=True)
    categoria = Column(String(30), nullable=False)
    cobertura = Column(Text, nullable=False)
    vigencia_default = Column(Integer, default=1)
    aseguradora_id = Column(Integer, ForeignKey("aseguradoras.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_actualizacion = Column(
        DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now
    )

    # Relaciones a Modelos SQLAlchemy
    aseguradora_rel = relationship(
        "Aseguradora",  # Nombre del modelo SQLAlchemy
        back_populates="tipos_seguros",  # Nombre de la relación en el modelo Aseguradora
        lazy="selectin"  # Carga eager
    )
    # Relación con movimientos (modelo MovimientoVigencia)
    movimientos = relationship("MovimientoVigencia", back_populates="tipo_seguro_rel", lazy="selectin")

    # Métodos para mapear entre Modelo SQLAlchemy y Entidad de Dominio
    def to_entity(self) -> TipoSeguroEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        # Mapear la relación Aseguradora cargada si existe
        aseguradora_entity = self.aseguradora_rel.to_entity() if self.aseguradora_rel else None

        return TipoSeguroEntity(  # Crea una instancia de la Entidad de Dominio
            id=self.id,
            codigo=self.codigo,
            nombre=self.nombre,
            descripcion=self.descripcion,
            es_default=self.es_default,
            esta_activo=self.esta_activo,
            categoria=self.categoria,
            cobertura=self.cobertura,
            vigencia_default=self.vigencia_default,
            aseguradora=aseguradora_entity,  # Asigna la Entidad Aseguradora relacionada
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion
            # No mapeamos lista de movimientos aquí a menos que la entidad de dominio la necesite
        )

    @staticmethod
    def from_entity(tipo_seguro: TipoSeguroEntity) -> 'TipoSeguro':  # Retorna una instancia de este modelo SQLAlchemy
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy."""
        # Mapea la referencia a la Entidad Aseguradora a su ID
        return TipoSeguro(  # Crea una instancia del modelo SQLAlchemy
            id=tipo_seguro.id,  # ID para update/delete, None para add (si es autoincremental)
            codigo=tipo_seguro.codigo,
            nombre=tipo_seguro.nombre,
            descripcion=tipo_seguro.descripcion,
            es_default=tipo_seguro.es_default,
            esta_activo=tipo_seguro.esta_activo,
            categoria=tipo_seguro.categoria,
            cobertura=tipo_seguro.cobertura,
            vigencia_default=tipo_seguro.vigencia_default,
            aseguradora_id=tipo_seguro.aseguradora.id if tipo_seguro.aseguradora else None,  # Usa el ID de la Entidad Aseguradora
            fecha_creacion=tipo_seguro.fecha_creacion,
            fecha_actualizacion=tipo_seguro.fecha_actualizacion,
        )