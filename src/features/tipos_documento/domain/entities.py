from dataclasses import dataclass
from typing import Optional


@dataclass
class TipoDocumento:
    """Entidad de Dominio para un Tipo de Documento."""
    codigo: str  # Ej: DNI, RUT, PASAPORTE
    nombre: str  # Ej: Documento Nacional de Identidad, Rol Único Tributario, Pasaporte
    id: Optional[int] = None
    descripcion: Optional[str] = None
    es_default: bool = False
    esta_activo: bool = True
    
    def is_valid_format(self, documento: str) -> bool:
        """Valida si el formato del documento es correcto según el tipo."""
        # Implementar lógica de validación según el tipo de documento
        # Por ejemplo, para RUT chileno, DNI argentino, etc.
        if self.codigo == "RUT":
            # Validar formato RUT chileno (ejemplo simplificado)
            return len(documento) >= 8 and "-" in documento
        elif self.codigo == "DNI":
            # Validar formato DNI (ejemplo simplificado)
            return len(documento) == 8 and documento.isdigit()
        elif self.codigo == "PASAPORTE":
            # Validar formato pasaporte (ejemplo simplificado)
            return len(documento) >= 6
        # Por defecto, aceptar cualquier formato
        return True
