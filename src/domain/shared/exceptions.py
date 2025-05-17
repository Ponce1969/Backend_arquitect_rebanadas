class MonedaException(Exception):
    """Excepción base para todas las excepciones relacionadas con Moneda."""
    pass


class MonedaNotFoundException(MonedaException):
    """Excepción lanzada cuando no se encuentra una moneda."""
    
    def __init__(self, moneda_id=None, codigo=None):
        if moneda_id:
            self.message = f"No se encontró la moneda con ID: {moneda_id}"
        elif codigo:
            self.message = f"No se encontró la moneda con código: {codigo}"
        else:
            self.message = "No se encontró la moneda especificada"
        super().__init__(self.message)


class MonedaInvalidaException(MonedaException):
    """Excepción lanzada cuando se proporciona una moneda inválida."""
    
    def __init__(self, codigo=None):
        if codigo:
            self.message = f"La moneda con código '{codigo}' no es válida o está inactiva"
        else:
            self.message = "La moneda especificada no es válida o está inactiva"
        super().__init__(self.message)


class MonedaCodigoExistsException(MonedaException):
    """Excepción lanzada cuando se intenta crear una moneda con un código que ya existe."""
    
    def __init__(self, codigo):
        self.message = f"Ya existe una moneda con el código: {codigo}"
        super().__init__(self.message)
