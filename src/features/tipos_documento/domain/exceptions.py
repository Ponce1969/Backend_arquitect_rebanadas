class TipoDocumentoException(Exception):
    """Excepciu00f3n base para todas las excepciones relacionadas con TipoDocumento."""
    pass


class TipoDocumentoNotFoundException(TipoDocumentoException):
    """Excepciu00f3n lanzada cuando no se encuentra un tipo de documento."""
    
    def __init__(self, tipo_id=None, codigo=None):
        if tipo_id:
            self.message = f"No se encontru00f3 el tipo de documento con ID: {tipo_id}"
        elif codigo:
            self.message = f"No se encontru00f3 el tipo de documento con cu00f3digo: {codigo}"
        else:
            self.message = "No se encontru00f3 el tipo de documento especificado"
        super().__init__(self.message)


class TipoDocumentoInvalidoException(TipoDocumentoException):
    """Excepciu00f3n lanzada cuando se proporciona un tipo de documento invu00e1lido."""
    
    def __init__(self, codigo=None):
        if codigo:
            self.message = f"El tipo de documento con cu00f3digo '{codigo}' no es vu00e1lido o estu00e1 inactivo"
        else:
            self.message = "El tipo de documento especificado no es vu00e1lido o estu00e1 inactivo"
        super().__init__(self.message)


class TipoDocumentoCodigoExistsException(TipoDocumentoException):
    """Excepciu00f3n lanzada cuando se intenta crear un tipo de documento con un cu00f3digo que ya existe."""
    
    def __init__(self, codigo):
        self.message = f"Ya existe un tipo de documento con el cu00f3digo: {codigo}"
        super().__init__(self.message)


class TipoDocumentoDefaultException(TipoDocumentoException):
    """Excepciu00f3n lanzada cuando hay operaciones no permitidas con el tipo de documento por defecto."""
    
    def __init__(self):
        self.message = "No se puede realizar esta operaciu00f3n con el tipo de documento por defecto"
        super().__init__(self.message)
