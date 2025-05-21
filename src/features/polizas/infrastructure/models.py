import enum
from datetime import date

from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# Importamos la Base desde la infraestructura compartida
from src.infrastructure.database import Base

# Importamos Modelos SQLAlchemy relacionados
from src.features.clientes.infrastructure.models import Cliente as ClienteModel
from src.features.corredores.infrastructure.models import Corredor as CorredorModel
from src.features.tipos_seguros.infrastructure.models import TipoSeguro as TipoSeguroModel
# Asumimos que existe un modelo Moneda en la infraestructura compartida
# from src.features.monedas.infrastructure.models import Moneda as MonedaModel

# Importamos la Entidad de Dominio Poliza para mapear
from src.features.polizas.domain.entities import Poliza as PolizaEntity
# Importamos el Enum TipoDuracion del dominio de Polizas
from src.features.polizas.domain.types import TipoDuracion as TipoDuracionEnum


class MovimientoVigencia(Base):
    """Modelo SQLAlchemy para la tabla movimientos_vigencias."""

    __tablename__ = "movimientos_vigencias"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    corredor_id = Column(Integer, ForeignKey("corredores.numero"))
    tipo_seguro_id = Column(Integer, ForeignKey("tipos_de_seguros.id"), nullable=False)
    carpeta = Column(String(100))
    numero_poliza = Column(String(100), nullable=False, unique=True)
    endoso = Column(String(100))
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    fecha_emision = Column(Date)
    estado_poliza = Column(String(20), default="activa")
    forma_pago = Column(String(20))
    tipo_endoso = Column(String(50))
    moneda_id = Column(Integer, ForeignKey("monedas.id"))
    suma_asegurada = Column(Float, nullable=False)
    prima = Column(Float, nullable=False)
    comision = Column(Float)
    cuotas = Column(Integer)
    observaciones = Column(String(500))
    tipo_duracion = Column(
        Enum(TipoDuracionEnum, name="tipo_duracion"),
        nullable=False,
        default=TipoDuracionEnum.anual,
        server_default=TipoDuracionEnum.anual.value,
    )

    # Relaciones
    cliente_rel = relationship("Cliente", back_populates="movimientos_vigencias", lazy="selectin")
    corredor_rel = relationship("Corredor", back_populates="movimientos", lazy="selectin")
    tipo_seguro_rel = relationship("TipoSeguro", back_populates="movimientos", lazy="selectin")
    # moneda_rel = relationship("MonedaModel", back_populates="movimientos", lazy="selectin")

    # Mu00e9todos para mapear entre Modelo SQLAlchemy y Entidad de Dominio (Poliza)
    def to_entity(self) -> PolizaEntity:
        """Convierte el modelo SQLAlchemy MovimientoVigencia a Entidad de Dominio Poliza."""
        # Mapear relaciones cargadas a Entidades de Dominio
        cliente_entity = self.cliente_rel.to_entity() if self.cliente_rel else None
        corredor_entity = self.corredor_rel.to_entity() if self.corredor_rel else None
        tipo_seguro_entity = self.tipo_seguro_rel.to_entity() if self.tipo_seguro_rel else None
        # moneda_entity = self.moneda_rel.to_entity() if self.moneda_rel else None

        # Mapear el valor del Enum de SQLAlchemy a la Entidad de Dominio
        try:
            tipo_duracion_domain = TipoDuracionEnum(self.tipo_duracion)
        except ValueError:
            # Manejar caso si el valor en DB no coincide con el Enum
            tipo_duracion_domain = TipoDuracionEnum.anual  # O un valor por defecto

        return PolizaEntity(
            id=self.id,
            cliente=cliente_entity,
            corredor=corredor_entity,
            tipo_seguro=tipo_seguro_entity,
            carpeta=self.carpeta,
            numero_poliza=self.numero_poliza,
            endoso=self.endoso,
            fecha_inicio=self.fecha_inicio,
            fecha_vencimiento=self.fecha_vencimiento,
            fecha_emision=self.fecha_emision,
            estado_poliza=self.estado_poliza,
            forma_pago=self.forma_pago,
            tipo_endoso=self.tipo_endoso,
            # moneda=moneda_entity,
            suma_asegurada=self.suma_asegurada,
            prima=self.prima,
            comision=self.comision,
            cuotas=self.cuotas,
            observaciones=self.observaciones,
            tipo_duracion=tipo_duracion_domain,
        )

    @staticmethod
    def from_entity(poliza: PolizaEntity) -> 'MovimientoVigencia':
        """Convierte una Entidad de Dominio Poliza a Modelo SQLAlchemy MovimientoVigencia."""
        # Mapea las referencias a Entidades de Dominio a IDs o Modelos relacionados
        return MovimientoVigencia(
            id=poliza.id,  # ID para update/delete, None para add (si es autoincremental)
            cliente_id=poliza.cliente.id if poliza.cliente else None,
            corredor_id=poliza.corredor.numero if poliza.corredor else None,
            tipo_seguro_id=poliza.tipo_seguro.id if poliza.tipo_seguro else None,
            carpeta=poliza.carpeta,
            numero_poliza=poliza.numero_poliza,
            endoso=poliza.endoso,
            fecha_inicio=poliza.fecha_inicio,
            fecha_vencimiento=poliza.fecha_vencimiento,
            fecha_emision=poliza.fecha_emision,
            estado_poliza=poliza.estado_poliza,
            forma_pago=poliza.forma_pago,
            tipo_endoso=poliza.tipo_endoso,
            # moneda_id=poliza.moneda.id if poliza.moneda else None,
            suma_asegurada=poliza.suma_asegurada,
            prima=poliza.prima,
            comision=poliza.comision,
            cuotas=poliza.cuotas,
            observaciones=poliza.observaciones,
            tipo_duracion=poliza.tipo_duracion.value,
        )