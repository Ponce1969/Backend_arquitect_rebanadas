from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Moneda:
    """Entidad de Dominio para una Moneda."""
    codigo: str  # Ej: USD, EUR, CLP
    nombre: str  # Ej: Dolar Estadounidense, Euro, Peso Chileno
    simbolo: str  # Ej: $, u20ac, $
    id: Optional[int] = None
    esta_activo: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    def get_formatted_code(self) -> str:
        """Retorna el codigo formateado para mostrar."""
        return f"{self.codigo} ({self.simbolo})"
