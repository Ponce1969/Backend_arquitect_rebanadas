from src.features.monedas.application.dtos import CrearMonedaCommand, ActualizarMonedaCommand, MonedaDto
from src.features.monedas.application.interfaces.repositories import AbstractMonedaRepository
from src.features.monedas.infrastructure.mappers import MonedaDTOMapper, CrearMonedaCommandMapper


class ObtenerMonedaUseCase:
    """Caso de uso para obtener una moneda por su ID."""
    
    def __init__(self, moneda_repository: AbstractMonedaRepository):
        self.moneda_repository = moneda_repository
    
    def execute(self, moneda_id: int) -> MonedaDto:
        """Obtiene una moneda por su ID."""
        moneda = self.moneda_repository.get_by_id(moneda_id)
        return MonedaDTOMapper.to_dto(moneda)


class ObtenerMonedaPorCodigoUseCase:
    """Caso de uso para obtener una moneda por su codigo."""
    
    def __init__(self, moneda_repository: AbstractMonedaRepository):
        self.moneda_repository = moneda_repository
    
    def execute(self, codigo: str) -> MonedaDto:
        """Obtiene una moneda por su codigo."""
        moneda = self.moneda_repository.get_by_codigo(codigo)
        return MonedaDTOMapper.to_dto(moneda)


class ListarMonedasUseCase:
    """Caso de uso para listar todas las monedas."""
    
    def __init__(self, moneda_repository: AbstractMonedaRepository):
        self.moneda_repository = moneda_repository
    
    def execute(self) -> list[MonedaDto]:
        """Lista todas las monedas activas."""
        monedas = self.moneda_repository.get_all()
        return MonedaDTOMapper.to_dto_list(monedas)


class CrearMonedaUseCase:
    """Caso de uso para crear una nueva moneda."""
    
    def __init__(self, moneda_repository: AbstractMonedaRepository):
        self.moneda_repository = moneda_repository
    
    def execute(self, command: CrearMonedaCommand) -> MonedaDto:
        """Crea una nueva moneda."""
        # Convertimos el comando a entidad de dominio
        moneda = CrearMonedaCommandMapper.to_entity(command)
        
        # Guardamos en el repositorio
        created_moneda = self.moneda_repository.add(moneda)
        
        # Convertimos la entidad a DTO
        return MonedaDTOMapper.to_dto(created_moneda)


class ActualizarMonedaUseCase:
    """Caso de uso para actualizar una moneda existente."""
    
    def __init__(self, moneda_repository: AbstractMonedaRepository):
        self.moneda_repository = moneda_repository
    
    def execute(self, command: ActualizarMonedaCommand) -> MonedaDto:
        """Actualiza una moneda existente."""
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
        
        # Convertimos la entidad a DTO
        return MonedaDTOMapper.to_dto(updated_moneda)


class EliminarMonedaUseCase:
    """Caso de uso para eliminar una moneda (marcarla como inactiva)."""
    
    def __init__(self, moneda_repository: AbstractMonedaRepository):
        self.moneda_repository = moneda_repository
    
    def execute(self, moneda_id: int) -> bool:
        """Elimina una moneda (marcandola como inactiva)."""
        return self.moneda_repository.delete(moneda_id)
