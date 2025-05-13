class SustitucionCorredorException(Exception):
    """Excepción base para el slice de Sustituciones de Corredores."""
    pass


class SustitucionCorredorNotFoundException(SustitucionCorredorException):
    """Excepción lanzada cuando no se encuentra una sustitución de corredor."""
    def __init__(self, sustitucion_id: int):
        self.sustitucion_id = sustitucion_id
        self.message = f"No se encontró la sustitución de corredor con ID {sustitucion_id}"
        super().__init__(self.message)


class CorredorAusenteNotFoundException(SustitucionCorredorException):
    """Excepción lanzada cuando no se encuentra el corredor ausente."""
    def __init__(self, corredor_id: int):
        self.corredor_id = corredor_id
        self.message = f"No se encontró el corredor ausente con ID {corredor_id}"
        super().__init__(self.message)


class CorredorSustitutoNotFoundException(SustitucionCorredorException):
    """Excepción lanzada cuando no se encuentra el corredor sustituto."""
    def __init__(self, corredor_id: int):
        self.corredor_id = corredor_id
        self.message = f"No se encontró el corredor sustituto con ID {corredor_id}"
        super().__init__(self.message)


class SustitucionCorredorFechasInvalidasException(SustitucionCorredorException):
    """Excepción lanzada cuando las fechas de la sustitución son inválidas."""
    def __init__(self, mensaje: str = "Las fechas de la sustitución son inválidas"):
        self.message = mensaje
        super().__init__(self.message)


class SustitucionCorredorSolapamientoException(SustitucionCorredorException):
    """Excepción lanzada cuando hay solapamiento con otra sustitución existente."""
    def __init__(self, corredor_ausente_id: int, fecha_inicio: str, fecha_fin: str):
        self.corredor_ausente_id = corredor_ausente_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.message = f"Ya existe una sustitución para el corredor {corredor_ausente_id} que se solapa con el periodo {fecha_inicio} - {fecha_fin}"
        super().__init__(self.message)
