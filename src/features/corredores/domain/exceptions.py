class CorredorException(Exception):
    """Excepción base para el slice de Corredores."""
    pass


class CorredorNotFoundException(CorredorException):
    """Excepción lanzada cuando no se encuentra un corredor."""
    def __init__(self, corredor_id: int):
        self.corredor_id = corredor_id
        self.message = f"No se encontró el corredor con ID {corredor_id}"
        super().__init__(self.message)


class CorredorNumeroExistsException(CorredorException):
    """Excepción lanzada cuando ya existe un corredor con el mismo número."""
    def __init__(self, numero: int):
        self.numero = numero
        self.message = f"Ya existe un corredor con el número {numero}"
        super().__init__(self.message)


class CorredorIdentificadorFiscalExistsException(CorredorException):
    """Excepción lanzada cuando ya existe un corredor con el mismo identificador fiscal."""
    def __init__(self, identificador_fiscal: str):
        self.identificador_fiscal = identificador_fiscal
        self.message = f"Ya existe un corredor con el identificador fiscal {identificador_fiscal}"
        super().__init__(self.message)


class CorredorEmailExistsException(CorredorException):
    """Excepción lanzada cuando ya existe un corredor con el mismo email."""
    def __init__(self, email: str):
        self.email = email
        self.message = f"Ya existe un corredor con el email {email}"
        super().__init__(self.message)
