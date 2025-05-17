from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID

# Importamos Entidades de Dominio relacionadas si es necesario
# from src.features.usuarios.domain.entities import Usuario
# from src.features.clientes.domain.entities import Cliente

@dataclass
class Corredor:
    """Entidad de Dominio para un Corredor."""
    # id: Optional[int] = None # ID técnico (Integer, autoincremental) - Opcional en dominio si solo se usa en infra
    numero: int # Identificador de negocio (Integer, único)
    nombres: str
    apellidos: str
    documento: str
    direccion: str
    localidad: str
    mail: str
    tipo: str | None = "corredor"
    telefonos: str | None = None
    movil: str | None = None
    observaciones: str | None = None
    fecha_alta: date | None = None
    fecha_baja: date | None = None
    matricula: str | None = None
    especializacion: str | None = None

    # Relaciones a Entidades de Dominio
    # Un Corredor puede tener varios Usuarios asociados (ej: administrador, asistente, él mismo)
    usuarios: list = field(default_factory=list)
    # Un Corredor tiene muchos Clientes (a través de la tabla intermedia)
    # La lista aquí representa los Clientes asociados, no la entidad intermedia ClienteCorredor
    clientes_asociados: list = field(default_factory=list)
    # Podrías añadir movimientos_vigencias si es relevante en este nivel de dominio

    # Métodos de negocio (ej: activar/desactivar corredor, añadir cliente)
    def activate(self):
        if self.fecha_baja is not None and self.fecha_baja <= date.today():
             self.fecha_baja = None # Re-activar si estaba dado de baja
        # Lógica adicional de activación


@dataclass
class ClienteCorredor:
    """Entidad de Dominio para la relación entre un Cliente y un Corredor."""
    cliente_id: UUID
    corredor_numero: int
    fecha_asignacion: date
    
    # Métodos de negocio
    def es_valida(self) -> bool:
        """
        Verifica si la asignación es válida según las reglas de negocio.
        
        Returns:
            bool: True si la asignación es válida, False en caso contrario.
        """
        # La fecha de asignación no puede ser futura
        return self.fecha_asignacion <= date.today()
    
    def es_activa(self, fecha_referencia: Optional[date] = None) -> bool:
        """
        Verifica si la asignación está activa en una fecha de referencia.
        
        Args:
            fecha_referencia: Fecha para verificar la vigencia. Si es None, se usa la fecha actual.
            
        Returns:
            bool: True si la asignación está activa en la fecha de referencia.
        """
        if fecha_referencia is None:
            fecha_referencia = date.today()
            
        return self.fecha_asignacion <= fecha_referencia