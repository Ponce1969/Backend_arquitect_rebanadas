from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.features.clientes.infrastructure.models import Cliente
from src.features.corredores.infrastructure.models import Corredor, ClienteCorredor


class SQLAlchemyClienteCorredorRepository:
    """Repositorio SQLAlchemy para la relación entre clientes y corredores."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_cliente_corredor(self, cliente_id: UUID, corredor_numero: int) -> Optional[ClienteCorredor]:
        """Obtiene una asignación específica entre un cliente y un corredor."""
        return self.session.query(ClienteCorredor).filter(
            ClienteCorredor.cliente_id == cliente_id,
            ClienteCorredor.corredor_numero == corredor_numero
        ).first()
    
    def get_by_cliente(self, cliente_id: UUID) -> List[ClienteCorredor]:
        """Obtiene todas las asignaciones para un cliente específico."""
        return self.session.query(ClienteCorredor).filter(
            ClienteCorredor.cliente_id == cliente_id
        ).all()
    
    def get_by_corredor(self, corredor_numero: int) -> List[ClienteCorredor]:
        """Obtiene todas las asignaciones para un corredor específico."""
        return self.session.query(ClienteCorredor).filter(
            ClienteCorredor.corredor_numero == corredor_numero
        ).all()
    
    def add(self, cliente_id: UUID, corredor_numero: int, fecha_asignacion: date) -> ClienteCorredor:
        """Agrega una nueva asignación entre un cliente y un corredor."""
        # Verificar que el cliente y el corredor existen
        cliente = self.session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID {cliente_id}")
        
        corredor = self.session.query(Corredor).filter(Corredor.numero == corredor_numero).first()
        if not corredor:
            raise ValueError(f"No se encontró un corredor con número {corredor_numero}")
        
        # Crear la nueva asignación
        asignacion = ClienteCorredor(
            cliente_id=cliente_id,
            corredor_numero=corredor_numero,
            fecha_asignacion=fecha_asignacion
        )
        
        self.session.add(asignacion)
        self.session.commit()
        self.session.refresh(asignacion)
        
        return asignacion
    
    def delete(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """Elimina una asignación entre un cliente y un corredor."""
        asignacion = self.get_by_cliente_corredor(cliente_id, corredor_numero)
        if not asignacion:
            return False
        
        self.session.delete(asignacion)
        self.session.commit()
        
        return True
