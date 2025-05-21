from sqlalchemy.orm import Session

from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.monedas.domain.exceptions import MonedaNotFoundException, MonedaInvalidaException, MonedaCodigoExistsException
from src.features.monedas.application.interfaces.repositories import AbstractMonedaRepository
from src.features.monedas.infrastructure.models import Moneda
from src.features.monedas.infrastructure.mappers import MonedaMapper
from src.infrastructure.cache import cached, clear_cache


class SQLAlchemyMonedaRepository(AbstractMonedaRepository):
    """Repositorio SQLAlchemy para el modelo Moneda."""
    
    def __init__(self, session: Session):
        self.session = session
    
    @cached(expiry_seconds=3600, key_prefix="moneda_id_")
    def get_by_id(self, moneda_id: int) -> MonedaEntity:
        """Obtiene una moneda por su ID."""
        moneda = self.session.query(Moneda).filter(Moneda.id == moneda_id).first()
        if not moneda:
            raise MonedaNotFoundException(moneda_id=moneda_id)
        return MonedaMapper.to_entity(moneda)
    
    @cached(expiry_seconds=3600, key_prefix="moneda_codigo_")
    def get_by_codigo(self, codigo: str) -> MonedaEntity:
        """Obtiene una moneda por su código."""
        moneda = self.session.query(Moneda).filter(Moneda.codigo == codigo).first()
        if not moneda:
            raise MonedaNotFoundException(codigo=codigo)
        if not moneda.esta_activo:
            raise MonedaInvalidaException(codigo=codigo)
        return MonedaMapper.to_entity(moneda)
    
    @cached(expiry_seconds=3600, key_prefix="monedas_all")
    def get_all(self) -> list[MonedaEntity]:
        """Obtiene todas las monedas."""
        monedas = self.session.query(Moneda).filter(Moneda.esta_activo == True).all()
        return MonedaMapper.to_entity_list(monedas)
    
    def add(self, moneda: MonedaEntity) -> MonedaEntity:
        """Agrega una nueva moneda."""
        # Verificar si ya existe una moneda con el mismo código
        existing = self.session.query(Moneda).filter(Moneda.codigo == moneda.codigo).first()
        if existing:
            raise MonedaCodigoExistsException(moneda.codigo)
            
        db_moneda = MonedaMapper.to_model(moneda)
        self.session.add(db_moneda)
        self.session.commit()
        self.session.refresh(db_moneda)
        
        # Limpiar caché después de agregar
        # Importar la función directamente para evitar problemas con el mock
        from src.infrastructure.cache import clear_cache as _clear_cache
        _clear_cache("moneda_")
        _clear_cache("monedas_")
        
        return MonedaMapper.to_entity(db_moneda)
    
    def update(self, moneda: MonedaEntity) -> MonedaEntity:
        """Actualiza una moneda existente."""
        db_moneda = self.session.query(Moneda).filter(Moneda.id == moneda.id).first()
        if not db_moneda:
            raise MonedaNotFoundException(moneda_id=moneda.id)
        
        # Verificar si el nuevo código ya existe en otra moneda
        if db_moneda.codigo != moneda.codigo:
            existing = self.session.query(Moneda).filter(
                Moneda.codigo == moneda.codigo, 
                Moneda.id != moneda.id
            ).first()
            if existing:
                raise MonedaCodigoExistsException(moneda.codigo)
        
        # Actualizar campos
        db_moneda.codigo = moneda.codigo
        db_moneda.nombre = moneda.nombre
        db_moneda.simbolo = moneda.simbolo
        db_moneda.esta_activo = moneda.esta_activo
        
        self.session.commit()
        self.session.refresh(db_moneda)
        
        # Limpiar caché después de actualizar
        clear_cache(f"moneda_id_{moneda.id}")
        clear_cache(f"moneda_codigo_{moneda.codigo}")
        clear_cache("monedas_")
        
        return MonedaMapper.to_entity(db_moneda)
    
    def delete(self, moneda_id: int) -> bool:
        """Elimina una moneda (marcandola como inactiva)."""
        db_moneda = self.session.query(Moneda).filter(Moneda.id == moneda_id).first()
        if not db_moneda:
            raise MonedaNotFoundException(moneda_id=moneda_id)
        
        db_moneda.esta_activo = False
        self.session.commit()
        
        # Limpiar caché después de eliminar
        clear_cache(f"moneda_id_{moneda_id}")
        clear_cache(f"moneda_codigo_{db_moneda.codigo}")
        clear_cache("monedas_")
        
        return True
