from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,  # Importar para constraint unico compuesto
)
from sqlalchemy.dialects.postgresql import (
    UUID as SQLAlchemyUUID,  # Usar alias para evitar conflicto con uuid.UUID
)
from sqlalchemy.orm import relationship

# Importamos la Entidad de Dominio para mapeo
from src.features.corredores.domain.entities import Corredor as CorredorEntity

# Importamos la Base desde la infraestructura compartida
from src.infrastructure.database import Base
# Importamos la función de tiempo desde la utilidad centralizada
from src.infrastructure.utils.datetime import get_utc_now


# --- Modelo SQLAlchemy para la tabla intermedia ClienteCorredor ---
class ClienteCorredor(Base):
    """Modelo SQLAlchemy para la tabla intermedia clientes_corredores."""

    __tablename__ = "clientes_corredores"

    # Definimos la clave primaria compuesta usando los FKs
    cliente_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("clientes.id"), primary_key=True)
    corredor_numero = Column(Integer, ForeignKey("corredores.numero"), primary_key=True) # FK al NUMERO del Corredor
    fecha_asignacion = Column(Date, default=date.today) # Usar date.today() o get_utc_now().date()

    # Definimos relaciones con los modelos principales
    # Usamos viewonly=True en una direccion si no queremos que SQLAlchemy maneje la coleccion en este modelo intermedio
    # O definimos back_populates si queremos la coleccion de asociaciones
    # Para simplificar, definimos las relaciones a Cliente y CorredorModel
    cliente_rel = relationship("Cliente", back_populates="corredores_asociados")
    corredor_rel = relationship("Corredor", back_populates="clientes_asociados")


# --- Modelo SQLAlchemy para la tabla Corredores ---
class Corredor(Base):
    """Modelo SQLAlchemy para la tabla corredores."""

    __tablename__ = "corredores"

    # Identificacion (usando Integer ID y Integer Numero segu00fan tu modelo original)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Clave primaria tecnica
    numero = Column(Integer, unique=True, index=True, nullable=False)  # Identificador de negocio
    tipo = Column(String(20), default="corredor")
    nombres = Column(String(30))
    apellidos = Column(String(30), nullable=False)
    documento = Column(String(20), nullable=False, unique=True)

    # Datos de contacto
    direccion = Column(String(70), nullable=False)
    localidad = Column(String(15), nullable=False)
    telefonos = Column(String(20))
    movil = Column(String(20))
    mail = Column(String(40), nullable=False, unique=True)

    # Datos adicionales
    observaciones = Column(Text)
    fecha_alta = Column(Date)
    fecha_baja = Column(Date)
    matricula = Column(String(50))
    especializacion = Column(String(100))

    # Relaciones a Modelos SQLAlchemy
    # Un corredor tiene multiples usuarios asociados
    usuarios = relationship(
        "Usuario", # Usamos el nombre del Modelo SQLAlchemy importado
        back_populates="corredor_rel", # Nombre de la relacion en el modelo UsuarioModel
        lazy="selectin" # Carga eager
    )
    # Un corredor tiene multiples clientes asociados (a travou00e9s del modelo intermedio)
    clientes_asociados = relationship(
        "ClienteCorredor", # Usamos el nombre del Modelo SQLAlchemy intermedio
        back_populates="corredor_rel", # Nombre de la relacion en el modelo ClienteCorredor
        lazy="selectin" # Carga eager
    )
    # Relacion con movimientos (modelo MovimientoVigencia)
    movimientos = relationship("MovimientoVigencia", back_populates="corredor_rel", lazy="selectin")

    # Metodos para mapear a Entidad de Dominio
    def to_entity(self) -> CorredorEntity:
        """Convierte el modelo SQLAlchemy a Entidad de Dominio."""
        # Mapear relaciones cargadas a Entidades de Dominio si existen
        usuarios_entities = [u.to_entity() for u in self.usuarios] if self.usuarios else []

        # Para la relacion muchos-a-muchos a clientes a travou00e9s de ClienteCorredor:
        # Mapeamos la relacion ClienteCorredorModel a la lista de ClienteEntity
        clientes_entities = [
             cc_rel.cliente_rel.to_entity() # Accedemos al modelo Cliente a travou00e9s de la relacion en ClienteCorredor
             for cc_rel in self.clientes_asociados # Iteramos sobre las instancias de ClienteCorredorModel
             if cc_rel.cliente_rel is not None # Asegurarse de que la relacion al ClienteModel esta cargada y no sea None
        ] if self.clientes_asociados else []


        return CorredorEntity(
            # id=self.id, # Omitimos el ID tecnico si el numero es el identificador principal en dominio
            numero=self.numero, # Usamos el numero como identificador en dominio
            tipo=self.tipo,
            nombres=self.nombres,
            apellidos=self.apellidos,
            documento=self.documento,
            direccion=self.direccion,
            localidad=self.localidad,
            telefonos=self.telefonos,
            movil=self.movil,
            mail=self.mail,
            observaciones=self.observaciones,
            fecha_alta=self.fecha_alta,
            fecha_baja=self.fecha_baja,
            matricula=self.matricula,
            especializacion=self.especializacion,
            usuarios=usuarios_entities, # Asigna lista de Entidades Usuario
            clientes_asociados=clientes_entities # Asigna lista de Entidades Cliente
            # Mapear movimientos si es relevante
        )

    @staticmethod
    def from_entity(corredor: CorredorEntity) -> 'Corredor': # Retorna una instancia de este modelo SQLAlchemy
        """Convierte una Entidad de Dominio a Modelo SQLAlchemy."""
        return Corredor( # Crea una instancia del modelo SQLAlchemy
            # id=corredor.id, # ID tecnico para update/delete, None para add
            numero=corredor.numero, # Numero para add (si no es autogenerado) o update/delete
            tipo=corredor.tipo,
            nombres=corredor.nombres,
            apellidos=corredor.apellidos,
            documento=corredor.documento,
            direccion=corredor.direccion,
            localidad=corredor.localidad,
            telefonos=corredor.telefonos,
            movil=corredor.movil,
            mail=corredor.mail,
            observaciones=corredor.observaciones,
            fecha_alta=corredor.fecha_alta,
            fecha_baja=corredor.fecha_baja,
            matricula=corredor.matricula,
            especializacion=corredor.especializacion,
            # No mapeamos listas de entidades aqui en from_entity del Corredor principal
        )