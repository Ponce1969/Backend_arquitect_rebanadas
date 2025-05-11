from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

# Importamos la interfaz abstracta (de la capa de Aplicación)
from src.features.tipos_seguros.application.interfaces.repositories import AbstractTipoSeguroRepository
# Importamos la Entidad de Dominio TipoSeguro
from src.features.tipos_seguros.domain.entities import TipoSeguro as TipoSeguroEntity
# Importamos el Modelo SQLAlchemy TipoSeguro
from .models import TipoSeguro as TipoSeguroModel


class SQLAlchemyTipoSeguroRepository(AbstractTipoSeguroRepository):
    """Implementación del Repositorio de Tipos de Seguro usando SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    # Helper para query base con eager loading de la relación Aseguradora
    def _get_base_query(self):
        return self.session.query(TipoSeguroModel).options(
            joinedload(TipoSeguroModel.aseguradora_rel)  # Cargar Aseguradora asociada
        )

    def add(self, tipo_seguro: TipoSeguroEntity):
        """Añade un nuevo tipo de seguro a la DB."""
        # from_entity mapea la Entidad (con referencia a Aseguradora Entity) a Modelo (con ID de Aseguradora)
        db_tipo_seguro = TipoSeguroModel.from_entity(tipo_seguro)
        try:
            self.session.add(db_tipo_seguro)
            self.session.flush()  # Para obtener el ID generado
            tipo_seguro.id = db_tipo_seguro.id  # Asigna el ID de vuelta a la Entidad
        except IntegrityError as e:
            self.session.rollback()
            # Manejar errores especu00edficos (ej. codigo duplicado)
            raise ValueError(f"Error de integridad al crear tipo de seguro: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al crear tipo de seguro: {e}")

    def get_by_id(self, tipo_seguro_id: int) -> Optional[TipoSeguroEntity]:
        """Obtiene un tipo de seguro por su ID técnico, con relación cargada."""
        db_tipo_seguro = self._get_base_query().filter(TipoSeguroModel.id == tipo_seguro_id).first()
        if db_tipo_seguro:
            return db_tipo_seguro.to_entity()  # Mapeo de Modelo (con relación) a Entidad
        return None

    def get_by_codigo(self, codigo: str) -> Optional[TipoSeguroEntity]:
        """Obtiene un tipo de seguro por su código, con relación cargada."""
        db_tipo_seguro = self._get_base_query().filter(TipoSeguroModel.codigo == codigo).first()
        if db_tipo_seguro:
            return db_tipo_seguro.to_entity()
        return None

    def get_all(self) -> List[TipoSeguroEntity]:
        """Obtiene todos los tipos de seguro, con relaciones cargadas."""
        db_tipos_seguro = self._get_base_query().all()
        return [db_tipo_seguro.to_entity() for db_tipo_seguro in db_tipos_seguro]

    def get_by_aseguradora(self, aseguradora_id: int) -> List[TipoSeguroEntity]:
        """Obtiene tipos de seguro asociados a una aseguradora específica, con relaciones cargadas."""
        db_tipos_seguro = self._get_base_query().filter(TipoSeguroModel.aseguradora_id == aseguradora_id).all()
        return [db_tipo_seguro.to_entity() for db_tipo_seguro in db_tipos_seguro]

    def update(self, tipo_seguro: TipoSeguroEntity):
        """Actualiza un tipo de seguro existente."""
        if not tipo_seguro.id:
            raise ValueError("No se puede actualizar un tipo de seguro sin ID")
            
        # Verificar que el tipo de seguro existe
        db_tipo_seguro = self.session.query(TipoSeguroModel).filter(TipoSeguroModel.id == tipo_seguro.id).first()
        if not db_tipo_seguro:
            raise ValueError(f"Tipo de seguro con ID {tipo_seguro.id} no encontrado")
        
        # Actualizar los campos del modelo con los valores de la entidad
        updated_tipo_seguro = TipoSeguroModel.from_entity(tipo_seguro)
        
        # Actualizar cada campo individualmente para evitar problemas con la sesiu00f3n
        db_tipo_seguro.codigo = updated_tipo_seguro.codigo
        db_tipo_seguro.nombre = updated_tipo_seguro.nombre
        db_tipo_seguro.descripcion = updated_tipo_seguro.descripcion
        db_tipo_seguro.es_default = updated_tipo_seguro.es_default
        db_tipo_seguro.esta_activo = updated_tipo_seguro.esta_activo
        db_tipo_seguro.categoria = updated_tipo_seguro.categoria
        db_tipo_seguro.cobertura = updated_tipo_seguro.cobertura
        db_tipo_seguro.vigencia_default = updated_tipo_seguro.vigencia_default
        db_tipo_seguro.aseguradora_id = updated_tipo_seguro.aseguradora_id
        
        try:
            self.session.flush()
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Error de integridad al actualizar tipo de seguro: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al actualizar tipo de seguro: {e}")

    def delete(self, tipo_seguro_id: int):
        """Elimina un tipo de seguro por su ID técnico."""
        db_tipo_seguro = self.session.query(TipoSeguroModel).filter(TipoSeguroModel.id == tipo_seguro_id).first()
        if not db_tipo_seguro:
            raise ValueError(f"Tipo de seguro con ID {tipo_seguro_id} no encontrado")
        
        try:
            self.session.delete(db_tipo_seguro)
            self.session.flush()
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Error de integridad al eliminar tipo de seguro: {e}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al eliminar tipo de seguro: {e}")