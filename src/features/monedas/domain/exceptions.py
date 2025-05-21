class MonedaException(Exception):
    """Excepcion base para todas las excepciones relacionadas con Moneda."""
    pass


class MonedaNotFoundException(MonedaException):
    """Excepcion lanzada cuando no se encuentra una moneda."""
    
    def __init__(self, moneda_id=None, codigo=None):
        if moneda_id:
            self.message = f"No se encontro la moneda con ID: {moneda_id}"
        elif codigo:
            self.message = f"No se encontro la moneda con codigo: {codigo}"
        else:
            self.message = "No se encontro la moneda especificada"
        super().__init__(self.message)


class MonedaInvalidaException(MonedaException):
    """Excepcion lanzada cuando se proporciona una moneda invalida."""
    
    def __init__(self, codigo=None):
        if codigo:
            self.message = f"La moneda con codigo '{codigo}' no es valida o esta inactiva"
        else:
            self.message = "La moneda especificada no es valida o esta inactiva"
        super().__init__(self.message)


class MonedaCodigoExistsException(MonedaException):
    """Excepcion lanzada cuando se intenta crear una moneda con un codigo que ya existe."""
    
    def __init__(self, codigo):
        self.message = f"Ya existe una moneda con el codigo: {codigo}"
        super().__init__(self.message)
