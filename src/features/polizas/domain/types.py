import enum


class TipoDuracion(str, enum.Enum):
    """Enumeraciu00f3n de Dominio para los tipos de duraciu00f3n de pu00f3lizas."""
    diaria = "diaria"
    semanal = "semanal"
    mensual = "mensual"
    trimestral = "trimestral"
    semestral = "semestral"
    anual = "anual"
