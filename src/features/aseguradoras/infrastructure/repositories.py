
from sqlalchemy.orm import Session

from ..application.interfaces import AbstractAseguradoraRepository
from ..domain.entities import Aseguradora as AseguradoraDomain
from .models import Aseguradora as AseguradoraModel


class SQLAlchemyAseguradoraRepository(AbstractAseguradoraRepository):
    """Implementación SQLAlchemy del repositorio de Aseguradoras."""

    def __init__(self, session: Session):
        self.session = session

    def _map_to_domain(self, db_aseguradora: AseguradoraModel) -> AseguradoraDomain:
        """Mapea un modelo SQLAlchemy a una entidad de dominio."""
        return AseguradoraDomain(
            id=db_aseguradora.id,
            nombre=db_aseguradora.nombre,
            identificador_fiscal=db_aseguradora.identificador_fiscal,
            telefono=db_aseguradora.telefono,
            direccion=db_aseguradora.direccion,
            email=db_aseguradora.email,
            pagina_web=db_aseguradora.pagina_web,
            esta_activa=db_aseguradora.esta_activa,
            observaciones=db_aseguradora.observaciones,
            fecha_creacion=db_aseguradora.fecha_creacion,
            fecha_actualizacion=db_aseguradora.fecha_actualizacion,
        )

    def _map_to_model(self, aseguradora: AseguradoraDomain) -> AseguradoraModel:
        """Mapea una entidad de dominio a un modelo SQLAlchemy."""
        return AseguradoraModel(
            id=aseguradora.id,
            nombre=aseguradora.nombre,
            identificador_fiscal=aseguradora.identificador_fiscal,
            telefono=aseguradora.telefono,
            direccion=aseguradora.direccion,
            email=aseguradora.email,
            pagina_web=aseguradora.pagina_web,
            esta_activa=aseguradora.esta_activa,
            observaciones=aseguradora.observaciones,
            fecha_creacion=aseguradora.fecha_creacion,
            fecha_actualizacion=aseguradora.fecha_actualizacion,
        )

    def add(self, aseguradora: AseguradoraDomain) -> AseguradoraDomain:
        db_aseguradora = self._map_to_model(aseguradora)
        self.session.add(db_aseguradora)
        self.session.flush()  # Para obtener el ID generado
        return self._map_to_domain(db_aseguradora)

    def get_by_id(self, aseguradora_id: int) -> AseguradoraDomain | None:
        db_aseguradora = self.session.query(AseguradoraModel).filter(
            AseguradoraModel.id == aseguradora_id
        ).first()
        return self._map_to_domain(db_aseguradora) if db_aseguradora else None

    def get_all(self) -> list[AseguradoraDomain]:
        db_aseguradoras = self.session.query(AseguradoraModel).all()
        return [self._map_to_domain(db_aseguradora) for db_aseguradora in db_aseguradoras]

    def update(self, aseguradora: AseguradoraDomain) -> AseguradoraDomain:
        db_aseguradora = self.session.query(AseguradoraModel).filter(
            AseguradoraModel.id == aseguradora.id
        ).first()
        if db_aseguradora:
            db_aseguradora.nombre = aseguradora.nombre
            db_aseguradora.identificador_fiscal = aseguradora.identificador_fiscal
            db_aseguradora.telefono = aseguradora.telefono
            db_aseguradora.direccion = aseguradora.direccion
            db_aseguradora.email = aseguradora.email
            db_aseguradora.pagina_web = aseguradora.pagina_web
            db_aseguradora.esta_activa = aseguradora.esta_activa
            db_aseguradora.observaciones = aseguradora.observaciones
            self.session.flush()
            return self._map_to_domain(db_aseguradora)
        return aseguradora  # Devuelve la entidad original si no se encuentra

    def delete(self, aseguradora_id: int) -> bool:
        db_aseguradora = self.session.query(AseguradoraModel).filter(
            AseguradoraModel.id == aseguradora_id
        ).first()
        if db_aseguradora:
            self.session.delete(db_aseguradora)
            return True
        return False

    def get_by_nombre(self, nombre: str) -> AseguradoraDomain | None:
        db_aseguradora = self.session.query(AseguradoraModel).filter(
            AseguradoraModel.nombre == nombre
        ).first()
        return self._map_to_domain(db_aseguradora) if db_aseguradora else None

    def get_by_identificador_fiscal(self, identificador_fiscal: str) -> AseguradoraDomain | None:
        db_aseguradora = self.session.query(AseguradoraModel).filter(
            AseguradoraModel.identificador_fiscal == identificador_fiscal
        ).first()
        return self._map_to_domain(db_aseguradora) if db_aseguradora else None
