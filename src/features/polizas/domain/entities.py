from dataclasses import dataclass
from datetime import date
from typing import Optional

# Importamos Entidades de Dominio relacionadas
from src.features.clientes.domain.entities import Cliente
from src.features.corredores.domain.entities import Corredor
from src.features.tipos_seguros.domain.entities import TipoSeguro
from src.domain.shared.entities import Moneda

# Importamos los tipos del dominio (TipoDuracion)
from .types import TipoDuracion


@dataclass
class Poliza:
    """Entidad de Dominio para una Poliza (Movimiento de Vigencia)."""
    # Referencias a Entidades de Dominio relacionadas
    cliente: Cliente
    tipo_seguro: TipoSeguro
    numero_poliza: str
    fecha_inicio: date
    fecha_vencimiento: date
    estado_poliza: str  # Podría ser un Enum de Dominio si los estados son fijos
    suma_asegurada: float
    prima: float
    tipo_duracion: TipoDuracion  # Usamos el Enum de Dominio
    # Campos opcionales
    id: Optional[int] = None  # ID técnico de la tabla movimientos_vigencias
    corredor: Optional[Corredor] = None  # Puede ser opcional si no todas las polizas tienen corredor asignado
    # La carpeta y número de poliza pueden ser identificadores de negocio
    carpeta: Optional[str] = None
    endoso: Optional[str] = None
    fecha_emision: Optional[date] = None
    forma_pago: Optional[str] = None  # Podría ser un Enum de Dominio / Entidad de Catálogo
    tipo_endoso: Optional[str] = None  # Podría ser un Enum de Dominio / Entidad de Catálogo
    moneda: Optional[Moneda] = None  # Referencia a la Entidad de Dominio Moneda
    comision: Optional[float] = None
    cuotas: Optional[int] = None
    observaciones: Optional[str] = None

    # Polizas puede añadir lógica de negocio relevante aquí
    def is_active(self) -> bool:
        """Verifica si la poliza está actualmente activa basándose en las fechas."""
        today = date.today()
        return self.fecha_inicio <= today <= self.fecha_vencimiento and self.estado_poliza == "activa"

    def calculate_commission_amount(self) -> Optional[float]:
        """Calcula el monto de la comisión si el porcentaje está definido."""
        if self.comision is not None and self.comision >= 0:
            return (self.prima * self.comision) / 100.0
        return None  # O 0.0