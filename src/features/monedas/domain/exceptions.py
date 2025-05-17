class MonedaException(Exception):
    """Excepciu00f3n base para todas las excepciones relacionadas con Moneda."""
    pass


class MonedaNotFoundException(MonedaException):
    """Excepciu00f3n lanzada cuando no se encuentra una moneda."""
    
    def __init__(self, moneda_id=None, codigo=None):
        if moneda_id:
            self.message = f"No se encontru00f3 la moneda con ID: {moneda_id}"
        elif codigo:
            self.message = f"No se encontru00f3 la moneda con cu00f3digo: {codigo}"
        else:
            self.message = "No se encontru00f3 la moneda especificada"
        super().__init__(self.message)


class MonedaInvalidaException(MonedaException):
    """Excepciu00f3n lanzada cuando se proporciona una moneda invu00e1lida."""
    
    def __init__(self, codigo=None):
        if codigo:
            self.message = f"La moneda con cu00f3digo '{codigo}' no es vu00e1lida o estu00e1 inactiva"
        else:
            self.message = "La moneda especificada no es vu00e1lida o estu00e1 inactiva"
        super().__init__(self.message)


class MonedaCodigoExistsException(MonedaException):
    """Excepciu00f3n lanzada cuando se intenta crear una moneda con un cu00f3digo que ya existe."""
    
    def __init__(self, codigo):
        self.message = f"Ya existe una moneda con el cu00f3digo: {codigo}"
        super().__init__(self.message)
