class SustitucionCorredorException(Exception):
    """Excepcion base para el slice de Sustituciones de Corredores."""
    pass


class SustitucionCorredorNotFoundException(SustitucionCorredorException):
    """Excepcion lanzada cuando no se encuentra una sustitucion de corredor."""
    def __init__(self, sustitucion_id: int):
        self.sustitucion_id = sustitucion_id
        self.message = f"No se encontro la sustitucion de corredor con ID {sustitucion_id}"
        super().__init__(self.message)


class CorredorAusenteNotFoundException(SustitucionCorredorException):
    """Excepcion lanzada cuando no se encuentra el corredor ausente."""
    def __init__(self, corredor_id: int):
        self.corredor_id = corredor_id
        self.message = f"No se encontro el corredor ausente con ID {corredor_id}"
        super().__init__(self.message)


class CorredorSustitutoNotFoundException(SustitucionCorredorException):
    """Excepcion lanzada cuando no se encuentra el corredor sustituto."""
    def __init__(self, corredor_id: int):
        self.corredor_id = corredor_id
        self.message = f"No se encontro el corredor sustituto con ID {corredor_id}"
        super().__init__(self.message)


class SustitucionCorredorFechasInvalidasException(SustitucionCorredorException):
    """Excepcion lanzada cuando las fechas de la sustitucion son invalidas."""
    def __init__(self, mensaje: str = "Las fechas de la sustitucion son invalidas"):
        self.message = mensaje
        super().__init__(self.message)


class SustitucionCorredorSolapamientoException(SustitucionCorredorException):
    """Excepcion lanzada cuando hay solapamiento con otra sustitucion existente."""
    def __init__(self, corredor_ausente_id: int, fecha_inicio: str, fecha_fin: str):
        self.corredor_ausente_id = corredor_ausente_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.message = f"Ya existe una sustitucion para el corredor {corredor_ausente_id} que se solapa con el periodo {fecha_inicio} - {fecha_fin}"
        super().__init__(self.message)
