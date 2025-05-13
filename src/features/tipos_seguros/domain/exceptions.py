class TipoSeguroException(Exception):
    """Excepción base para el slice de Tipos de Seguros."""
    pass


class TipoSeguroNotFoundException(TipoSeguroException):
    """Excepción lanzada cuando no se encuentra un tipo de seguro."""
    def __init__(self, tipo_seguro_id: int):
        self.tipo_seguro_id = tipo_seguro_id
        self.message = f"No se encontró el tipo de seguro con ID {tipo_seguro_id}"
        super().__init__(self.message)


class TipoSeguroCodigoExistsException(TipoSeguroException):
    """Excepción lanzada cuando ya existe un tipo de seguro con el mismo código."""
    def __init__(self, codigo: str):
        self.codigo = codigo
        self.message = f"Ya existe un tipo de seguro con el código {codigo}"
        super().__init__(self.message)


class TipoSeguroNombreExistsException(TipoSeguroException):
    """Excepción lanzada cuando ya existe un tipo de seguro con el mismo nombre."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.message = f"Ya existe un tipo de seguro con el nombre {nombre}"
        super().__init__(self.message)


class TipoSeguroAseguradoraNotFoundException(TipoSeguroException):
    """Excepción lanzada cuando no se encuentra la aseguradora asociada al tipo de seguro."""
    def __init__(self, aseguradora_id: int):
        self.aseguradora_id = aseguradora_id
        self.message = f"No se encontró la aseguradora con ID {aseguradora_id} para asociar al tipo de seguro"
        super().__init__(self.message)
