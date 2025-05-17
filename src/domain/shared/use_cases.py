from src.domain.shared.entities import Moneda
from src.domain.shared.dtos import CrearMonedaCommand, ActualizarMonedaCommand, MonedaDto
from src.domain.shared.exceptions import MonedaNotFoundException, MonedaInvalidaException, MonedaCodigoExistsException


class ObtenerMonedaUseCase:
    """Caso de uso para obtener una moneda por su ID."""
    
    def __init__(self, moneda_repository):
        self.moneda_repository = moneda_repository
    
    def execute(self, moneda_id: int) -> MonedaDto:
        """Obtiene una moneda por su ID."""
        try:
            moneda = self.moneda_repository.get_by_id(moneda_id)
            return MonedaDto.model_validate(moneda)
        except MonedaNotFoundException as e:
            raise e


class ObtenerMonedaPorCodigoUseCase:
    """Caso de uso para obtener una moneda por su cu00f3digo."""
    
    def __init__(self, moneda_repository):
        self.moneda_repository = moneda_repository
    
    def execute(self, codigo: str) -> MonedaDto:
        """Obtiene una moneda por su cu00f3digo."""
        try:
            moneda = self.moneda_repository.get_by_codigo(codigo)
            return MonedaDto.model_validate(moneda)
        except (MonedaNotFoundException, MonedaInvalidaException) as e:
            raise e


class ListarMonedasUseCase:
    """Caso de uso para listar todas las monedas."""
    
    def __init__(self, moneda_repository):
        self.moneda_repository = moneda_repository
    
    def execute(self) -> list[MonedaDto]:
        """Lista todas las monedas activas."""
        monedas = self.moneda_repository.get_all()
        return [MonedaDto.model_validate(moneda) for moneda in monedas]


class CrearMonedaUseCase:
    """Caso de uso para crear una nueva moneda."""
    
    def __init__(self, moneda_repository):
        self.moneda_repository = moneda_repository
    
    def execute(self, command: CrearMonedaCommand) -> MonedaDto:
        """Crea una nueva moneda."""
        # Creamos la entidad de dominio
        moneda = Moneda(
            codigo=command.codigo,
            nombre=command.nombre,
            simbolo=command.simbolo
        )
        
        try:
            # Guardamos en el repositorio
            created_moneda = self.moneda_repository.add(moneda)
            return MonedaDto.model_validate(created_moneda)
        except MonedaCodigoExistsException as e:
            raise e


class ActualizarMonedaUseCase:
    """Caso de uso para actualizar una moneda existente."""
    
    def __init__(self, moneda_repository):
        self.moneda_repository = moneda_repository
    
    def execute(self, command: ActualizarMonedaCommand) -> MonedaDto:
        """Actualiza una moneda existente."""
        try:
            # Obtenemos la moneda actual
            current_moneda = self.moneda_repository.get_by_id(command.id)
            
            # Actualizamos solo los campos que vienen en el comando
            if command.codigo is not None:
                current_moneda.codigo = command.codigo
            if command.nombre is not None:
                current_moneda.nombre = command.nombre
            if command.simbolo is not None:
                current_moneda.simbolo = command.simbolo
            if command.esta_activo is not None:
                current_moneda.esta_activo = command.esta_activo
            
            # Guardamos los cambios
            updated_moneda = self.moneda_repository.update(current_moneda)
            return MonedaDto.model_validate(updated_moneda)
        except (MonedaNotFoundException, MonedaCodigoExistsException) as e:
            raise e


class EliminarMonedaUseCase:
    """Caso de uso para eliminar una moneda (marcarla como inactiva)."""
    
    def __init__(self, moneda_repository):
        self.moneda_repository = moneda_repository
    
    def execute(self, moneda_id: int) -> bool:
        """Elimina una moneda (marcu00e1ndola como inactiva)."""
        try:
            return self.moneda_repository.delete(moneda_id)
        except MonedaNotFoundException as e:
            raise e
