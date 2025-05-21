from datetime import date, datetime
from typing import Optional


class SustitucionCorredor:
    """Entidad de dominio para la sustitución temporal de corredores."""

    def __init__(
        self,
        id: Optional[int] = None,
        corredor_ausente_numero: int = None,
        corredor_sustituto_numero: int = None,
        fecha_inicio: date = None,
        fecha_fin: Optional[date] = None,
        estado: str = "activa",  # activa, inactiva
        motivo: str = "",
        observaciones: str = "",
        fecha_creacion: Optional[datetime] = None,
        fecha_actualizacion: Optional[datetime] = None,
    ):
        self.id = id
        self.corredor_ausente_numero = corredor_ausente_numero
        self.corredor_sustituto_numero = corredor_sustituto_numero
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.motivo = motivo
        self.observaciones = observaciones
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
