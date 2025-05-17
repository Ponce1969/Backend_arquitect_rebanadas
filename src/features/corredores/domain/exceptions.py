from uuid import UUID


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


# Excepciones específicas para ClienteCorredor
class ClienteCorredorException(CorredorException):
    """Excepción base para el módulo ClienteCorredor."""
    pass


class ClienteCorredorAsignacionDuplicadaException(ClienteCorredorException):
    """Excepción lanzada cuando se intenta crear una asignación duplicada."""
    def __init__(self, cliente_id: UUID, corredor_numero: int):
        self.cliente_id = cliente_id
        self.corredor_numero = corredor_numero
        self.message = f"El cliente {cliente_id} ya está asignado al corredor {corredor_numero}"
        super().__init__(self.message)


class ClienteCorredorNoEncontradoException(ClienteCorredorException):
    """Excepción lanzada cuando no se encuentra una asignación."""
    def __init__(self, cliente_id: UUID, corredor_numero: int):
        self.cliente_id = cliente_id
        self.corredor_numero = corredor_numero
        self.message = f"No se encontró la asignación del cliente {cliente_id} al corredor {corredor_numero}"
        super().__init__(self.message)


class ClienteNoEncontradoException(ClienteCorredorException):
    """Excepción lanzada cuando no se encuentra un cliente."""
    def __init__(self, cliente_id: UUID):
        self.cliente_id = cliente_id
        self.message = f"No se encontró el cliente con ID {cliente_id}"
        super().__init__(self.message)


class CorredorNoEncontradoException(ClienteCorredorException):
    """Excepción lanzada cuando no se encuentra un corredor."""
    def __init__(self, corredor_numero: int):
        self.corredor_numero = corredor_numero
        self.message = f"No se encontró el corredor con número {corredor_numero}"
        super().__init__(self.message)


class FechaAsignacionInvalidaException(ClienteCorredorException):
    """Excepción lanzada cuando la fecha de asignación no es válida."""
    def __init__(self, fecha_asignacion: str):
        self.fecha_asignacion = fecha_asignacion
        self.message = f"La fecha de asignación {fecha_asignacion} no es válida (no puede ser futura)"
        super().__init__(self.message)
