import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

# Importamos la interfaz abstracta (de la capa de Aplicaciu00f3n)
from src.features.polizas.application.interfaces.repositories import AbstractPolizaRepository
# Importamos la Entidad de Dominio Poliza
from src.features.polizas.domain.entities import Poliza as PolizaEntity
# Importamos el Modelo SQLAlchemy MovimientoVigencia
from .models import MovimientoVigencia as MovimientoVigenciaModel


class SQLAlchemyPolizaRepository(AbstractPolizaRepository):
    """Implementaciu00f3n del Repositorio de Pu00f3lizas usando SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    # Helper para query base con eager loading de TODAS las relaciones
    def _get_base_query(self):
        return self.session.query(MovimientoVigenciaModel).options(
            joinedload(MovimientoVigenciaModel.cliente_rel),
            joinedload(MovimientoVigenciaModel.corredor_rel),
            joinedload(MovimientoVigenciaModel.tipo_seguro_rel),
            # joinedload(MovimientoVigenciaModel.moneda_rel)  # Comentado hasta que se implemente el modelo Moneda
        )

    def add(self, poliza: PolizaEntity):
        """Au00f1ade una nueva pu00f3liza a la DB."""
        # from_entity mapea la Entidad (con referencias a otras Entidades) a Modelo (con IDs de FK)
        db_poliza = MovimientoVigenciaModel.from_entity(poliza)
        try:
            self.session.add(db_poliza)
            self.session.flush()  # Para obtener el ID generado
            poliza.id = db_poliza.id  # Asigna el ID de vuelta a la Entidad
        except Exception as e:  # Considerar IntegrityError para errores especu00edficos
            self.session.rollback()
            raise Exception(f"Error al crear pu00f3liza: {e}")

    def get_by_id(self, poliza_id: int) -> Optional[PolizaEntity]:
        """Obtiene una pu00f3liza de la DB por su ID, con relaciones cargadas."""
        db_poliza = self._get_base_query().filter(MovimientoVigenciaModel.id == poliza_id).first()
        if db_poliza:
            return db_poliza.to_entity()  # Mapeo de Modelo (con relaciones) a Entidad
        return None

    def get_by_numero_poliza(self, numero_poliza: str, carpeta: Optional[str] = None) -> Optional[PolizaEntity]:
        """Obtiene una pu00f3liza por su nu00famero y carpeta, con relaciones cargadas."""
        query = self._get_base_query().filter(MovimientoVigenciaModel.numero_poliza == numero_poliza)
        if carpeta is not None:
            query = query.filter(MovimientoVigenciaModel.carpeta == carpeta)
        db_poliza = query.first()
        if db_poliza:
            return db_poliza.to_entity()
        return None

    def get_all(self) -> List[PolizaEntity]:
        """Obtiene todas las pu00f3lizas de la DB, con relaciones cargadas."""
        db_polizas = self._get_base_query().all()
        return [db_poliza.to_entity() for db_poliza in db_polizas]

    def update(self, poliza: PolizaEntity):
        """Actualiza una pu00f3liza existente."""
        db_poliza = self._get_base_query().filter(MovimientoVigenciaModel.id == poliza.id).first()
        if not db_poliza:
            raise ValueError(f"Pu00f3liza con ID {poliza.id} no encontrada")
        
        # Actualizamos los campos del modelo con los valores de la entidad
        updated_db_poliza = MovimientoVigenciaModel.from_entity(poliza)
        
        # Actualizamos los atributos del modelo existente
        for key, value in updated_db_poliza.__dict__.items():
            if key != "_sa_instance_state" and hasattr(db_poliza, key):
                setattr(db_poliza, key, value)
        
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al actualizar pu00f3liza: {e}")

    def delete(self, poliza_id: int):
        """Elimina una pu00f3liza por su ID tu00e9cnico."""
        db_poliza = self.session.query(MovimientoVigenciaModel).filter(MovimientoVigenciaModel.id == poliza_id).first()
        if not db_poliza:
            raise ValueError(f"Pu00f3liza con ID {poliza_id} no encontrada")
        
        try:
            self.session.delete(db_poliza)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al eliminar pu00f3liza: {e}")

    def get_by_cliente(self, cliente_id: uuid.UUID) -> List[PolizaEntity]:
        """Obtiene todas las pu00f3lizas de un cliente especu00edfico, con relaciones cargadas."""
        db_polizas = self._get_base_query().filter(MovimientoVigenciaModel.cliente_id == cliente_id).all()
        return [db_poliza.to_entity() for db_poliza in db_polizas]

    def get_vigentes_by_cliente(self, cliente_id: uuid.UUID, today: date) -> List[PolizaEntity]:
        """Obtiene las pu00f3lizas vigentes de un cliente a una fecha dada, con relaciones cargadas."""
        db_polizas = self._get_base_query().filter(
            and_(
                MovimientoVigenciaModel.cliente_id == cliente_id,
                MovimientoVigenciaModel.fecha_inicio <= today,
                MovimientoVigenciaModel.fecha_vencimiento >= today,
                MovimientoVigenciaModel.estado_poliza == "activa"
            )
        ).all()
        return [db_poliza.to_entity() for db_poliza in db_polizas]

    def get_by_corredor(self, corredor_id: int) -> List[PolizaEntity]:
        """Obtiene todas las pu00f3lizas de un corredor especu00edfico."""
        # Asumimos que corredor_id es el nu00famero del corredor, que es lo que se usa como FK en la tabla
        db_polizas = self._get_base_query().filter(MovimientoVigenciaModel.corredor_id == corredor_id).all()
        return [db_poliza.to_entity() for db_poliza in db_polizas]