from sqlalchemy.orm import Session

from src.features.tipos_documento.domain.entities import TipoDocumento as TipoDocumentoEntity
from src.features.tipos_documento.domain.exceptions import TipoDocumentoNotFoundException, TipoDocumentoCodigoExistsException
from src.features.tipos_documento.application.interfaces.repositories import AbstractTipoDocumentoRepository
from src.features.tipos_documento.infrastructure.models import TipoDocumento
from src.infrastructure.cache import cached, clear_cache


class SQLAlchemyTipoDocumentoRepository(AbstractTipoDocumentoRepository):
    """Repositorio SQLAlchemy para el modelo TipoDocumento."""
    
    def __init__(self, session: Session):
        self.session = session
    
    @cached(expiry_seconds=3600, key_prefix="tipo_documento_id_")
    def get_by_id(self, tipo_id: int) -> TipoDocumentoEntity:
        """Obtiene un tipo de documento por su ID."""
        tipo = self.session.query(TipoDocumento).filter(TipoDocumento.id == tipo_id).first()
        if not tipo:
            raise TipoDocumentoNotFoundException(tipo_id=tipo_id)
        return tipo.to_entity()
    
    @cached(expiry_seconds=3600, key_prefix="tipo_documento_codigo_")
    def get_by_codigo(self, codigo: str) -> TipoDocumentoEntity:
        """Obtiene un tipo de documento por su cu00f3digo."""
        tipo = self.session.query(TipoDocumento).filter(TipoDocumento.codigo == codigo).first()
        if not tipo:
            return None
        return tipo.to_entity()
    
    @cached(expiry_seconds=3600, key_prefix="tipo_documento_default")
    def get_default(self) -> TipoDocumentoEntity:
        """Obtiene el tipo de documento marcado como default."""
        tipo = self.session.query(TipoDocumento).filter(
            TipoDocumento.es_default == True,
            TipoDocumento.esta_activo == True
        ).first()
        if not tipo:
            return None
        return tipo.to_entity()
    
    @cached(expiry_seconds=3600, key_prefix="tipos_documento_all")
    def get_all(self) -> list[TipoDocumentoEntity]:
        """Obtiene todos los tipos de documento activos."""
        tipos = self.session.query(TipoDocumento).filter(TipoDocumento.esta_activo == True).all()
        return [tipo.to_entity() for tipo in tipos]
    
    def add(self, tipo: TipoDocumentoEntity) -> TipoDocumentoEntity:
        """Agrega un nuevo tipo de documento."""
        # Verificar si ya existe un tipo con el mismo cu00f3digo
        existing = self.session.query(TipoDocumento).filter(TipoDocumento.codigo == tipo.codigo).first()
        if existing:
            raise TipoDocumentoCodigoExistsException(tipo.codigo)
            
        db_tipo = TipoDocumento.from_entity(tipo)
        self.session.add(db_tipo)
        self.session.commit()
        self.session.refresh(db_tipo)
        
        # Limpiar cachu00e9 despuu00e9s de agregar
        clear_cache("tipo_documento_")
        clear_cache("tipos_documento_")
        
        return db_tipo.to_entity()
    
    def update(self, tipo: TipoDocumentoEntity) -> TipoDocumentoEntity:
        """Actualiza un tipo de documento existente."""
        db_tipo = self.session.query(TipoDocumento).filter(TipoDocumento.id == tipo.id).first()
        if not db_tipo:
            raise TipoDocumentoNotFoundException(tipo_id=tipo.id)
        
        # Verificar si el nuevo cu00f3digo ya existe en otro tipo
        if db_tipo.codigo != tipo.codigo:
            existing = self.session.query(TipoDocumento).filter(
                TipoDocumento.codigo == tipo.codigo, 
                TipoDocumento.id != tipo.id
            ).first()
            if existing:
                raise TipoDocumentoCodigoExistsException(tipo.codigo)
        
        # Actualizar campos
        db_tipo.codigo = tipo.codigo
        db_tipo.nombre = tipo.nombre
        db_tipo.descripcion = tipo.descripcion
        db_tipo.es_default = tipo.es_default
        db_tipo.esta_activo = tipo.esta_activo
        
        self.session.commit()
        self.session.refresh(db_tipo)
        
        # Limpiar cachu00e9 despuu00e9s de actualizar
        clear_cache(f"tipo_documento_id_{tipo.id}")
        clear_cache(f"tipo_documento_codigo_{tipo.codigo}")
        clear_cache("tipo_documento_default")
        clear_cache("tipos_documento_all")
        
        return db_tipo.to_entity()
    
    def delete(self, tipo_id: int) -> bool:
        """Elimina un tipo de documento (marcu00e1ndolo como inactivo)."""
        db_tipo = self.session.query(TipoDocumento).filter(TipoDocumento.id == tipo_id).first()
        if not db_tipo:
            raise TipoDocumentoNotFoundException(tipo_id=tipo_id)
        
        # No permitir eliminar el tipo por defecto
        if db_tipo.es_default:
            raise ValueError("No se puede eliminar el tipo de documento por defecto")
        
        db_tipo.esta_activo = False
        self.session.commit()
        
        # Limpiar cachu00e9 despuu00e9s de eliminar
        clear_cache(f"tipo_documento_id_{tipo_id}")
        clear_cache(f"tipo_documento_codigo_{db_tipo.codigo}")
        clear_cache("tipos_documento_all")
        
        return True
