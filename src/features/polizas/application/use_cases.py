import uuid
from datetime import date
from typing import List, Optional

# Importamos las interfaces de los repositorios
from src.features.polizas.application.interfaces.repositories import AbstractPolizaRepository
from src.features.clientes.application.interfaces.repositories import IClienteRepository
from src.features.corredores.application.interfaces.repositories import ICorredorRepository
from src.features.tipos_seguros.application.interfaces.repositories import AbstractTipoSeguroRepository
# from src.domain.shared.interfaces.repositories import AbstractMonedaRepository  # Asumimos que existe

# Importamos los DTOs
from src.features.polizas.application.dtos import EmitirPolizaCommand, ActualizarPolizaCommand, PolizaDto, PolizaSummaryDto

# Importamos la entidad de dominio
from src.features.polizas.domain.entities import Poliza

# Importamos las excepciones personalizadas
from src.features.polizas.domain.exceptions import (
    PolizaNotFoundException,
    PolizaNumeroExistsException,
    ClienteNotFoundException,
    CorredorNotFoundException,
    TipoSeguroNotFoundException,
    MonedaNotFoundException
)


class EmitirPolizaUseCase:
    """Caso de uso para emitir una nueva poliza."""
    
    def __init__(
        self,
        poliza_repository: AbstractPolizaRepository,
        cliente_repository: IClienteRepository,
        corredor_repository: ICorredorRepository,
        tipo_seguro_repository: AbstractTipoSeguroRepository,
        # moneda_repository: AbstractMonedaRepository  # Asumimos que existe
    ):
        self.poliza_repository = poliza_repository
        self.cliente_repository = cliente_repository
        self.corredor_repository = corredor_repository
        self.tipo_seguro_repository = tipo_seguro_repository
        # self.moneda_repository = moneda_repository
    
    def execute(self, command: EmitirPolizaCommand) -> PolizaDto:
        """Ejecuta el caso de uso para emitir una nueva poliza."""
        # Verificar si ya existe una poliza con el mismo numero
        existing_poliza = self.poliza_repository.get_by_numero_poliza(command.numero_poliza, command.carpeta)
        if existing_poliza:
            raise PolizaNumeroExistsException(command.numero_poliza, command.carpeta)
        
        # Obtener las entidades relacionadas
        cliente = self.cliente_repository.get_by_id(command.cliente_id)
        if not cliente:
            raise ClienteNotFoundException(command.cliente_id)
        
        corredor = None
        if command.corredor_id:
            corredor = self.corredor_repository.get_by_numero(command.corredor_id)
            if not corredor:
                raise CorredorNotFoundException(command.corredor_id)
        
        tipo_seguro = self.tipo_seguro_repository.get_by_id(command.tipo_seguro_id)
        if not tipo_seguro:
            raise TipoSeguroNotFoundException(command.tipo_seguro_id)
        
        moneda = None
        # if command.moneda_id:
        #     moneda = self.moneda_repository.get_by_id(command.moneda_id)
        #     if not moneda:
        #         raise MonedaNotFoundException(command.moneda_id)
        
        # Crear la entidad de dominio
        poliza = Poliza(
            cliente=cliente,
            corredor=corredor,
            tipo_seguro=tipo_seguro,
            carpeta=command.carpeta,
            numero_poliza=command.numero_poliza,
            endoso=command.endoso,
            fecha_inicio=command.fecha_inicio,
            fecha_vencimiento=command.fecha_vencimiento,
            fecha_emision=command.fecha_emision,
            estado_poliza=command.estado_poliza,
            forma_pago=command.forma_pago,
            tipo_endoso=command.tipo_endoso,
            moneda=moneda,
            suma_asegurada=command.suma_asegurada,
            prima=command.prima,
            comision=command.comision,
            cuotas=command.cuotas,
            observaciones=command.observaciones,
            tipo_duracion=command.tipo_duracion,
        )
        
        # Persistir la entidad
        self.poliza_repository.add(poliza)
        
        # Obtener la entidad completa con su ID asignado
        created_poliza = self.poliza_repository.get_by_id(poliza.id)
        
        # Mapear a DTO y retornar
        return PolizaDto.model_validate(created_poliza)


class ObtenerPolizaUseCase:
    """Caso de uso para obtener una poliza por su ID."""
    
    def __init__(self, poliza_repository: AbstractPolizaRepository):
        self.poliza_repository = poliza_repository
    
    def execute(self, poliza_id: int) -> PolizaDto:
        """Ejecuta el caso de uso para obtener una poliza por su ID."""
        poliza = self.poliza_repository.get_by_id(poliza_id)
        if not poliza:
            raise PolizaNotFoundException(poliza_id)
        
        return PolizaDto.model_validate(poliza)


class ObtenerPolizaPorNumeroUseCase:
    """Caso de uso para obtener una poliza por su numero."""
    
    def __init__(self, poliza_repository: AbstractPolizaRepository):
        self.poliza_repository = poliza_repository
    
    def execute(self, numero_poliza: str, carpeta: Optional[str] = None) -> PolizaDto:
        """Ejecuta el caso de uso para obtener una poliza por su numero."""
        poliza = self.poliza_repository.get_by_numero_poliza(numero_poliza, carpeta)
        if not poliza:
            raise PolizaNotFoundException(0)  # Usamos 0 como ID genuérico ya que no tenemos el ID real
        
        return PolizaDto.model_validate(poliza)


class ListarPolizasUseCase:
    """Caso de uso para listar todas las polizas."""
    
    def __init__(self, poliza_repository: AbstractPolizaRepository):
        self.poliza_repository = poliza_repository
    
    def execute(self) -> List[PolizaSummaryDto]:
        """Ejecuta el caso de uso para listar todas las polizas."""
        polizas = self.poliza_repository.get_all()
        
        # Mapear a DTOs de resumen
        return [self._to_summary_dto(poliza) for poliza in polizas]
    
    def _to_summary_dto(self, poliza: Poliza) -> PolizaSummaryDto:
        """Convierte una entidad Poliza a un DTO de resumen."""
        return PolizaSummaryDto.model_validate(poliza)


class ListarPolizasPorClienteUseCase:
    """Caso de uso para listar las polizas de un cliente."""
    
    def __init__(self, poliza_repository: AbstractPolizaRepository):
        self.poliza_repository = poliza_repository
    
    def execute(self, cliente_id: uuid.UUID) -> List[PolizaSummaryDto]:
        """Ejecuta el caso de uso para listar las polizas de un cliente."""
        polizas = self.poliza_repository.get_by_cliente(cliente_id)
        
        # Mapear a DTOs de resumen
        return [self._to_summary_dto(poliza) for poliza in polizas]
    
    def _to_summary_dto(self, poliza: Poliza) -> PolizaSummaryDto:
        """Convierte una entidad Poliza a un DTO de resumen."""
        return PolizaSummaryDto.model_validate(poliza)


class ActualizarPolizaUseCase:
    """Caso de uso para actualizar una poliza existente."""
    
    def __init__(
        self,
        poliza_repository: AbstractPolizaRepository,
        corredor_repository: ICorredorRepository,
        # moneda_repository: AbstractMonedaRepository  # Asumimos que existe
    ):
        self.poliza_repository = poliza_repository
        self.corredor_repository = corredor_repository
        # self.moneda_repository = moneda_repository
    
    def execute(self, command: ActualizarPolizaCommand) -> PolizaDto:
        """Ejecuta el caso de uso para actualizar una poliza existente."""
        # Obtener la poliza existente
        poliza = self.poliza_repository.get_by_id(command.id)
        if not poliza:
            raise PolizaNotFoundException(command.id)
        
        # Actualizar los campos que vienen en el comando
        if command.corredor_id is not None:
            if command.corredor_id != (poliza.corredor.numero if poliza.corredor else None):
                corredor = self.corredor_repository.get_by_numero(command.corredor_id)
                if not corredor:
                    raise CorredorNotFoundException(command.corredor_id)
                poliza.corredor = corredor
        
        # if command.moneda_id is not None:
        #     if command.moneda_id != (poliza.moneda.id if poliza.moneda else None):
        #         moneda = self.moneda_repository.get_by_id(command.moneda_id)
        #         if not moneda:
        #             raise MonedaNotFoundException(command.moneda_id)
        #         poliza.moneda = moneda
        
        # Actualizar campos simples
        if command.carpeta is not None:
            poliza.carpeta = command.carpeta
        if command.endoso is not None:
            poliza.endoso = command.endoso
        if command.fecha_vencimiento is not None:
            poliza.fecha_vencimiento = command.fecha_vencimiento
        if command.fecha_emision is not None:
            poliza.fecha_emision = command.fecha_emision
        if command.estado_poliza is not None:
            poliza.estado_poliza = command.estado_poliza
        if command.forma_pago is not None:
            poliza.forma_pago = command.forma_pago
        if command.tipo_endoso is not None:
            poliza.tipo_endoso = command.tipo_endoso
        if command.suma_asegurada is not None:
            poliza.suma_asegurada = command.suma_asegurada
        if command.prima is not None:
            poliza.prima = command.prima
        if command.comision is not None:
            poliza.comision = command.comision
        if command.cuotas is not None:
            poliza.cuotas = command.cuotas
        if command.observaciones is not None:
            poliza.observaciones = command.observaciones
        if command.tipo_duracion is not None:
            poliza.tipo_duracion = command.tipo_duracion
        
        # Persistir los cambios
        self.poliza_repository.update(poliza)
        
        # Obtener la entidad actualizada
        updated_poliza = self.poliza_repository.get_by_id(poliza.id)
        
        # Mapear a DTO y retornar
        return PolizaDto.model_validate(updated_poliza)


class EliminarPolizaUseCase:
    """Caso de uso para eliminar una poliza."""
    
    def __init__(self, poliza_repository: AbstractPolizaRepository):
        self.poliza_repository = poliza_repository
    
    def execute(self, poliza_id: int) -> bool:
        """Ejecuta el caso de uso para eliminar una poliza."""
        # Verificar si la poliza existe
        poliza = self.poliza_repository.get_by_id(poliza_id)
        if not poliza:
            raise PolizaNotFoundException(poliza_id)
        
        # Eliminar la poliza
        self.poliza_repository.delete(poliza_id)
        
        return True
