from uuid import UUID


class ClienteException(Exception):
    """Excepción base para el slice de Clientes."""
    pass


class ClienteNotFoundException(ClienteException):
    """Excepción lanzada cuando no se encuentra un cliente."""
    def __init__(self, cliente_id: UUID):
        self.cliente_id = cliente_id
        self.message = f"No se encontró el cliente con ID {cliente_id}"
        super().__init__(self.message)


class ClienteNumeroNotFoundException(ClienteException):
    """Excepción lanzada cuando no se encuentra un cliente por su número."""
    def __init__(self, numero_cliente: int):
        self.numero_cliente = numero_cliente
        self.message = f"No se encontró el cliente con número {numero_cliente}"
        super().__init__(self.message)


class ClienteDocumentoNotFoundException(ClienteException):
    """Excepción lanzada cuando no se encuentra un cliente por su documento."""
    def __init__(self, numero_documento: str):
        self.numero_documento = numero_documento
        self.message = f"No se encontró el cliente con documento {numero_documento}"
        super().__init__(self.message)


class ClienteDocumentoExistsException(ClienteException):
    """Excepción lanzada cuando ya existe un cliente con el mismo número de documento."""
    def __init__(self, numero_documento: str):
        self.numero_documento = numero_documento
        self.message = f"Ya existe un cliente con el número de documento {numero_documento}"
        super().__init__(self.message)


class ClienteEmailExistsException(ClienteException):
    """Excepción lanzada cuando ya existe un cliente con el mismo email."""
    def __init__(self, email: str):
        self.email = email
        self.message = f"Ya existe un cliente con el email {email}"
        super().__init__(self.message)
