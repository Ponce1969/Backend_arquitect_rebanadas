class AseguradoraException(Exception):
    """Excepción base para el slice de Aseguradoras."""
    pass


class AseguradoraNotFoundException(AseguradoraException):
    """Excepción lanzada cuando no se encuentra una aseguradora."""
    def __init__(self, aseguradora_id: int):
        self.aseguradora_id = aseguradora_id
        self.message = f"No se encontró la aseguradora con ID {aseguradora_id}"
        super().__init__(self.message)


class AseguradoraNombreExistsException(AseguradoraException):
    """Excepción lanzada cuando ya existe una aseguradora con el mismo nombre."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.message = f"Ya existe una aseguradora con el nombre {nombre}"
        super().__init__(self.message)


class AseguradoraIdentificadorFiscalExistsException(AseguradoraException):
    """Excepción lanzada cuando ya existe una aseguradora con el mismo identificador fiscal."""
    def __init__(self, identificador_fiscal: str):
        self.identificador_fiscal = identificador_fiscal
        self.message = f"Ya existe una aseguradora con el identificador fiscal {identificador_fiscal}"
        super().__init__(self.message)
