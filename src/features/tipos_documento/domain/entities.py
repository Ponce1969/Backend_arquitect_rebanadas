from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TipoDocumento:
    """Entidad de dominio para tipos de documento."""
    nombre: str
    id: Optional[int] = None
    descripcion: Optional[str] = None
    activo: bool = True
    
    # Relaciones
    clientes: List = None  # Lista de clientes que usan este tipo de documento
    
    def __post_init__(self):
        if self.clientes is None:
            self.clientes = []
