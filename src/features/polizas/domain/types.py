import enum


class TipoDuracion(str, enum.Enum):
    """Enumeración de Dominio para los tipos de duración de polizas."""
    diaria = "diaria"
    semanal = "semanal"
    mensual = "mensual"
    trimestral = "trimestral"
    semestral = "semestral"
    anual = "anual"
