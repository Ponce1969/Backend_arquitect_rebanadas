from sqlalchemy.orm import Session

from src.features.monedas.domain.entities import Moneda as MonedaEntity
from src.features.monedas.domain.exceptions import MonedaNotFoundException, MonedaInvalidaException, MonedaCodigoExistsException
from src.features.tipos_documento.domain.entities import TipoDocumento as TipoDocumentoEntity
from src.infrastructure.cache import cached, clear_cache
from src.features.monedas.infrastructure.models import Moneda
from src.features.tipos_documento.infrastructure.models import TipoDocumento


class SQLAlchemyMonedaRepository:
    """Repositorio SQLAlchemy para el modelo Moneda."""
    
    def __init__(self, session: Session):
        self.session = session
    
    @cached(expiry_seconds=3600, key_prefix="moneda_id_")
    def get_by_id(self, moneda_id: int) -> MonedaEntity:
        """Obtiene una moneda por su ID."""
        moneda = self.session.query(Moneda).filter(Moneda.id == moneda_id).first()
        if not moneda:
            raise MonedaNotFoundException(moneda_id=moneda_id)
        return moneda.to_entity()
    
    @cached(expiry_seconds=3600, key_prefix="moneda_codigo_")
    def get_by_codigo(self, codigo: str) -> MonedaEntity:
        """Obtiene una moneda por su código."""
        moneda = self.session.query(Moneda).filter(Moneda.codigo == codigo).first()
        if not moneda:
            raise MonedaNotFoundException(codigo=codigo)
        if not moneda.esta_activo:
            raise MonedaInvalidaException(codigo=codigo)
        return moneda.to_entity()
    
    @cached(expiry_seconds=3600, key_prefix="monedas_all")
    def get_all(self) -> list[MonedaEntity]:
        """Obtiene todas las monedas."""
        monedas = self.session.query(Moneda).filter(Moneda.esta_activo == True).all()
        return [moneda.to_entity() for moneda in monedas]
    
    def add(self, moneda: MonedaEntity) -> MonedaEntity:
        """Agrega una nueva moneda."""
        # Verificar si ya existe una moneda con el mismo código
        existing = self.session.query(Moneda).filter(Moneda.codigo == moneda.codigo).first()
        if existing:
            raise MonedaCodigoExistsException(moneda.codigo)
            
        db_moneda = Moneda.from_entity(moneda)
        self.session.add(db_moneda)
        self.session.commit()
        self.session.refresh(db_moneda)
        
        # Limpiar caché después de agregar
        clear_cache("moneda_")
        clear_cache("monedas_")
        
        return db_moneda.to_entity()
    
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
        
        return db_moneda.to_entity()
    
    def delete(self, moneda_id: int) -> bool:
        """Elimina una moneda (marcándola como inactiva)."""
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


class SQLAlchemyTipoDocumentoRepository:
    """Repositorio SQLAlchemy para el modelo TipoDocumento."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, tipo_id: int) -> TipoDocumentoEntity:
        """Obtiene un tipo de documento por su ID."""
        tipo = self.session.query(TipoDocumento).filter(TipoDocumento.id == tipo_id).first()
        if tipo:
            return tipo.to_entity()
        return None
    
    def get_by_codigo(self, codigo: str) -> TipoDocumentoEntity:
        """Obtiene un tipo de documento por su código."""
        tipo = self.session.query(TipoDocumento).filter(TipoDocumento.codigo == codigo).first()
        if tipo:
            return tipo.to_entity()
        return None
    
    def get_default(self) -> TipoDocumentoEntity:
        """Obtiene el tipo de documento marcado como default."""
        tipo = self.session.query(TipoDocumento).filter(
            TipoDocumento.es_default == True,
            TipoDocumento.esta_activo == True
        ).first()
        if tipo:
            return tipo.to_entity()
        return None
    
    def get_all(self) -> list[TipoDocumentoEntity]:
        """Obtiene todos los tipos de documento activos."""
        tipos = self.session.query(TipoDocumento).filter(TipoDocumento.esta_activo == True).all()
        return [tipo.to_entity() for tipo in tipos]
    
    def add(self, tipo: TipoDocumentoEntity) -> TipoDocumentoEntity:
        """Agrega un nuevo tipo de documento."""
        db_tipo = TipoDocumento.from_entity(tipo)
        self.session.add(db_tipo)
        self.session.commit()
        self.session.refresh(db_tipo)
        return db_tipo.to_entity()
    
    def update(self, tipo: TipoDocumentoEntity) -> TipoDocumentoEntity:
        """Actualiza un tipo de documento existente."""
        db_tipo = self.session.query(TipoDocumento).filter(TipoDocumento.id == tipo.id).first()
        if not db_tipo:
            return None
        
        # Actualizar campos
        db_tipo.codigo = tipo.codigo
        db_tipo.nombre = tipo.nombre
        db_tipo.descripcion = tipo.descripcion
        db_tipo.es_default = tipo.es_default
        db_tipo.esta_activo = tipo.esta_activo
        
        self.session.commit()
        self.session.refresh(db_tipo)
        return db_tipo.to_entity()
    
    def delete(self, tipo_id: int) -> bool:
        """Elimina un tipo de documento (marcándolo como inactivo)."""
        db_tipo = self.session.query(TipoDocumento).filter(TipoDocumento.id == tipo_id).first()
        if not db_tipo:
            return False
        
        db_tipo.esta_activo = False
        self.session.commit()
        return True
