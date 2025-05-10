from dataclasses import dataclass


@dataclass
class TipoDocumento:
    """Entidad de dominio para tipos de documento."""
    nombre: str
    id: int | None = None
    descripcion: str | None = None
    activo: bool = True
    
    # Relaciones
    clientes: list = None  # Lista de clientes que usan este tipo de documento
    
    def __post_init__(self):
        if self.clientes is None:
            self.clientes = []
