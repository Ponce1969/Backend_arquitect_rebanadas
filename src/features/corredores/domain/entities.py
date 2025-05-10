from dataclasses import dataclass, field
from datetime import date

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