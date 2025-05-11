from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Importamos la Entidad de Dominio Aseguradora desde su slice
from src.features.aseguradoras.domain.entities import Aseguradora

@dataclass
class TipoSeguro:
    """Entidad de Dominio para un Tipo de Seguro."""
    codigo: str
    nombre: str
    categoria: str
    cobertura: str
    # Referencia a la Entidad de Dominio Aseguradora
    aseguradora: Aseguradora  # Un TipoSeguro pertenece a una Aseguradora
    id: Optional[int] = None  # ID técnico (Integer)
    descripcion: Optional[str] = None
    es_default: bool = False
    esta_activo: bool = True
    vigencia_default: int = 1
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    # Mu00e9todos de negocio relevantes
    def is_valid_for_vigencia(self, duration_in_months: int) -> bool:
        """Verifica si el tipo de seguro es vu00e1lido para una vigencia especu00edfica."""
        # Ejemplo: Un tipo de seguro con vigencia_default 12 es vu00e1lido para vigencias de 12 meses
        return self.vigencia_default * 30 >= duration_in_months
    
    def get_full_description(self) -> str:
        """Obtiene la descripciu00f3n completa del tipo de seguro."""
        return f"{self.nombre} ({self.codigo}) - {self.categoria}: {self.descripcion}"
    
    def is_active(self) -> bool:
        """Verifica si el tipo de seguro estu00e1 activo."""
        return self.esta_activo