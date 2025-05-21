from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.features.clientes.infrastructure.models import Cliente
from src.features.corredores.infrastructure.models import Corredor, ClienteCorredor as ClienteCorredorModel
from src.features.corredores.domain.entities import ClienteCorredor as ClienteCorredorEntity
from src.features.corredores.domain.exceptions import (
    ClienteCorredorAsignacionDuplicadaException,
    ClienteNoEncontradoException,
    CorredorNoEncontradoException,
    FechaAsignacionInvalidaException
)
from src.features.corredores.application.interfaces.repositories import IClienteCorredorRepository


class SQLAlchemyClienteCorredorRepository(IClienteCorredorRepository):
    """
    Implementación del repositorio de ClienteCorredor usando SQLAlchemy.
    
    Esta clase implementa la interfaz IClienteCorredorRepository y proporciona
    una implementación concreta usando SQLAlchemy como ORM.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de SQLAlchemy.
        
        Args:
            session: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.session = session
    
    def _to_entity(self, model: ClienteCorredorModel) -> Optional[ClienteCorredorEntity]:
        """
        Convierte un modelo de SQLAlchemy a una entidad de dominio.
        
        Args:
            model: Instancia del modelo SQLAlchemy
            
        Returns:
            Entidad de dominio ClienteCorredor
        """
        if not model:
            return None
            
        return ClienteCorredorEntity(
            cliente_id=model.cliente_id,
            corredor_numero=model.corredor_numero,
            fecha_asignacion=model.fecha_asignacion
        )
    
    def _to_model(self, entity: ClienteCorredorEntity) -> Optional[ClienteCorredorModel]:
        """
        Convierte una entidad de dominio a un modelo de SQLAlchemy.
        
        Args:
            entity: Entidad de dominio ClienteCorredor
            
        Returns:
            Instancia del modelo SQLAlchemy
        """
        if not entity:
            return None
            
        return ClienteCorredorModel(
            cliente_id=entity.cliente_id,
            corredor_numero=entity.corredor_numero,
            fecha_asignacion=entity.fecha_asignacion
        )
    
    def exists(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """Verifica si existe una asignación entre un cliente y un corredor."""
        return self.session.query(
            self.session.query(ClienteCorredorModel)
            .filter_by(cliente_id=cliente_id, corredor_numero=corredor_numero)
            .exists()
        ).scalar()
    
    def get_by_cliente_corredor(self, cliente_id: UUID, corredor_numero: int) -> Optional[ClienteCorredorEntity]:
        """
        Obtiene una asignación específica entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente
            corredor_numero: Número del corredor
            
        Returns:
            ClienteCorredorEntity si se encuentra, None en caso contrario
        """
        model = self.session.query(ClienteCorredorModel).filter(
            ClienteCorredorModel.cliente_id == cliente_id,
            ClienteCorredorModel.corredor_numero == corredor_numero
        ).first()
        
        return self._to_entity(model)
    
    def get_by_cliente(self, cliente_id: UUID) -> list[ClienteCorredorEntity]:
        """
        Obtiene todas las asignaciones para un cliente específico.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Lista de entidades ClienteCorredor
        """
        models = self.session.query(ClienteCorredorModel).filter(
            ClienteCorredorModel.cliente_id == cliente_id
        ).all()
        
        return [self._to_entity(model) for model in models]
    
    def get_by_corredor(self, corredor_numero: int) -> list[ClienteCorredorEntity]:
        """
        Obtiene todas las asignaciones para un corredor específico.
        
        Args:
            corredor_numero: Número del corredor
            
        Returns:
            Lista de entidades ClienteCorredor
        """
        models = self.session.query(ClienteCorredorModel).filter(
            ClienteCorredorModel.corredor_numero == corredor_numero
        ).all()
        
        return [self._to_entity(model) for model in models]
    
    def add(self, cliente_id: UUID, corredor_numero: int, fecha_asignacion: date) -> ClienteCorredorEntity:
        """
        Agrega una nueva asignación entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente a asignar
            corredor_numero: Número del corredor al que se asignará el cliente
            fecha_asignacion: Fecha en que se realiza la asignación
            
        Returns:
            La entidad ClienteCorredor creada
            
        Raises:
            ClienteNoEncontradoException: Si no existe el cliente
            CorredorNoEncontradoException: Si no existe el corredor
            ClienteCorredorAsignacionDuplicadaException: Si ya existe la asignación
            FechaAsignacionInvalidaException: Si la fecha de asignación es futura
        """
        # Validar que la fecha de asignación no sea futura
        if fecha_asignacion > date.today():
            raise FechaAsignacionInvalidaException(str(fecha_asignacion))
        
        # Verificar que el cliente existe
        cliente = self.session.query(Cliente).get(cliente_id)
        if not cliente:
            raise ClienteNoEncontradoException(cliente_id)
        
        # Verificar que el corredor existe
        corredor = self.session.query(Corredor).filter_by(numero=corredor_numero).first()
        if not corredor:
            raise CorredorNoEncontradoException(corredor_numero)
        
        # Verificar que no exista ya la asignación
        if self.exists(cliente_id, corredor_numero):
            raise ClienteCorredorAsignacionDuplicadaException(cliente_id, corredor_numero)
        
        # Crear la nueva asignación
        model = ClienteCorredorModel(
            cliente_id=cliente_id,
            corredor_numero=corredor_numero,
            fecha_asignacion=fecha_asignacion
        )
        
        self.session.add(model)
        self.session.commit()
        
        # Convertir el modelo a entidad y devolverlo
        return self._to_entity(model)
    
    def remove(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """
        Elimina una asignación entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente
            corredor_numero: Número del corredor
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        asignacion = self.get_by_cliente_corredor(cliente_id, corredor_numero)
        if not asignacion:
            return False
        
        # Buscar el modelo correspondiente a la entidad
        model = self.session.query(ClienteCorredorModel).filter_by(
            cliente_id=cliente_id,
            corredor_numero=corredor_numero
        ).first()
        
        if not model:
            return False
            
        self.session.delete(model)
        self.session.commit()
        
        return True

    def update(self, cliente_id: UUID, corredor_numero_antiguo: int, 
              corredor_numero_nuevo: int, fecha_asignacion: date) -> ClienteCorredorEntity:
        """
        Actualiza una asignación de cliente entre corredores.
        
        Args:
            cliente_id: ID del cliente a reasignar
            corredor_numero_antiguo: Número del corredor actual
            corredor_numero_nuevo: Número del nuevo corredor
            fecha_asignacion: Nueva fecha de asignación
            
        Returns:
            La entidad ClienteCorredor actualizada
            
        Raises:
            ClienteCorredorNoEncontradoException: Si no existe la asignación original
            ClienteCorredorAsignacionDuplicadaException: Si ya existe una asignación para el nuevo par cliente-corredor
        """
        # Verificar que la asignación original existe
        asignacion_original = self.get_by_cliente_corredor(cliente_id, corredor_numero_antiguo)
        if not asignacion_original:
            raise ClienteNoEncontradoException(f"No existe asignación para el cliente {cliente_id} con el corredor {corredor_numero_antiguo}")
        
        # Si el corredor nuevo es diferente al antiguo, verificar que no exista ya una asignación
        if corredor_numero_antiguo != corredor_numero_nuevo and self.exists(cliente_id, corredor_numero_nuevo):
            raise ClienteCorredorAsignacionDuplicadaException(
                f"El cliente {cliente_id} ya está asignado al corredor {corredor_numero_nuevo}"
            )
        
        # Eliminar la asignación original
        self.remove(cliente_id, corredor_numero_antiguo)
        
        # Crear la nueva asignación
        return self.add(cliente_id, corredor_numero_nuevo, fecha_asignacion)
