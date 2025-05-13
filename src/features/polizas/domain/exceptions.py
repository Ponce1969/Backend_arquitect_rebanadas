from uuid import UUID


class PolizaException(Exception):
    """Excepción base para el slice de Pólizas."""
    pass


class PolizaNotFoundException(PolizaException):
    """Excepción lanzada cuando no se encuentra una póliza."""
    def __init__(self, poliza_id: int):
        self.poliza_id = poliza_id
        self.message = f"Póliza con ID {poliza_id} no encontrada"
        super().__init__(self.message)


class PolizaNumeroExistsException(PolizaException):
    """Excepción lanzada cuando ya existe una póliza con el mismo número."""
    def __init__(self, numero_poliza: str, carpeta: str = None):
        self.numero_poliza = numero_poliza
        self.carpeta = carpeta
        carpeta_str = f" en la carpeta {carpeta}" if carpeta else ""
        self.message = f"Ya existe una póliza con el número {numero_poliza}{carpeta_str}"
        super().__init__(self.message)


class ClienteNotFoundException(PolizaException):
    """Excepción lanzada cuando no se encuentra un cliente al emitir o actualizar una póliza."""
    def __init__(self, cliente_id: UUID):
        self.cliente_id = cliente_id
        self.message = f"Cliente con ID {cliente_id} no encontrado"
        super().__init__(self.message)


class CorredorNotFoundException(PolizaException):
    """Excepción lanzada cuando no se encuentra un corredor al emitir o actualizar una póliza."""
    def __init__(self, corredor_id: int):
        self.corredor_id = corredor_id
        self.message = f"Corredor con número {corredor_id} no encontrado"
        super().__init__(self.message)


class TipoSeguroNotFoundException(PolizaException):
    """Excepción lanzada cuando no se encuentra un tipo de seguro al emitir o actualizar una póliza."""
    def __init__(self, tipo_seguro_id: int):
        self.tipo_seguro_id = tipo_seguro_id
        self.message = f"Tipo de seguro con ID {tipo_seguro_id} no encontrado"
        super().__init__(self.message)


class MonedaNotFoundException(PolizaException):
    """Excepción lanzada cuando no se encuentra una moneda al emitir o actualizar una póliza."""
    def __init__(self, moneda_id: int):
        self.moneda_id = moneda_id
        self.message = f"Moneda con ID {moneda_id} no encontrada"
        super().__init__(self.message)
