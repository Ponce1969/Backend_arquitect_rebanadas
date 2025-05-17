from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..application.interfaces.repositories import ICorredorRepository
from ..domain.entities import Corredor as CorredorDomain
from .models import Corredor as CorredorModel


class SQLAlchemyCorredorRepository(ICorredorRepository):
    """Implementaciu00f3n SQLAlchemy del repositorio de Corredores."""

    def __init__(self, session: Session):
        self.session = session

    def _map_to_domain(self, db_corredor: CorredorModel) -> CorredorDomain:
        """Mapea un modelo SQLAlchemy a una entidad de dominio."""
        return CorredorDomain(
            numero=db_corredor.numero,
            nombres=db_corredor.nombres,
            apellidos=db_corredor.apellidos,
            documento=db_corredor.documento,
            direccion=db_corredor.direccion,
            localidad=db_corredor.localidad,
            mail=db_corredor.mail,
            tipo=db_corredor.tipo,
            telefonos=db_corredor.telefonos,
            movil=db_corredor.movil,
            observaciones=db_corredor.observaciones,
            fecha_alta=db_corredor.fecha_alta,
            fecha_baja=db_corredor.fecha_baja,
            matricula=db_corredor.matricula,
            especializacion=db_corredor.especializacion,
            # Relaciones
            usuarios=[],  # Aquí se podrían mapear los usuarios relacionados si es necesario
            clientes_asociados=[]  # Aquí se podrían mapear los clientes relacionados si es necesario
        )

    def _map_to_db(self, corredor: CorredorDomain, db_corredor: Optional[CorredorModel] = None) -> CorredorModel:
        """Mapea una entidad de dominio a un modelo SQLAlchemy."""
        if db_corredor is None:
            db_corredor = CorredorModel()

        db_corredor.numero = corredor.numero
        db_corredor.nombres = corredor.nombres
        db_corredor.apellidos = corredor.apellidos
        db_corredor.documento = corredor.documento
        db_corredor.direccion = corredor.direccion
        db_corredor.localidad = corredor.localidad
        db_corredor.mail = corredor.mail
        db_corredor.tipo = corredor.tipo
        db_corredor.telefonos = corredor.telefonos
        db_corredor.movil = corredor.movil
        db_corredor.observaciones = corredor.observaciones
        db_corredor.fecha_alta = corredor.fecha_alta
        db_corredor.fecha_baja = corredor.fecha_baja
        db_corredor.matricula = corredor.matricula
        db_corredor.especializacion = corredor.especializacion

        return db_corredor

    def add(self, corredor: CorredorDomain):
        """Añade un nuevo corredor al repositorio."""
        db_corredor = self._map_to_db(corredor)
        self.session.add(db_corredor)
        self.session.commit()
        self.session.refresh(db_corredor)
        return self._map_to_domain(db_corredor)

    def get_by_id(self, corredor_id: int) -> Optional[CorredorDomain]:
        """Obtiene un corredor por su ID técnico."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.id == corredor_id).first()
        return self._map_to_domain(db_corredor) if db_corredor else None

    def get_by_numero(self, numero: int) -> Optional[CorredorDomain]:
        """Obtiene un corredor por su número (identificador de negocio)."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.numero == numero).first()
        return self._map_to_domain(db_corredor) if db_corredor else None

    def get_by_documento(self, documento: str) -> Optional[CorredorDomain]:
        """Obtiene un corredor por su número de documento."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.documento == documento).first()
        return self._map_to_domain(db_corredor) if db_corredor else None

    def get_by_email(self, email: str) -> Optional[CorredorDomain]:
        """Obtiene un corredor por su dirección de correo electrónico."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.mail == email).first()
        return self._map_to_domain(db_corredor) if db_corredor else None

    def get_all(self) -> List[CorredorDomain]:
        """Obtiene todos los corredores."""
        db_corredores = self.session.query(CorredorModel).all()
        return [self._map_to_domain(db_corredor) for db_corredor in db_corredores]

    def update(self, corredor: CorredorDomain):
        """Actualiza un corredor existente."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.numero == corredor.numero).first()
        if db_corredor is None:
            raise ValueError(f"No se encontró un corredor con el número {corredor.numero}")

        db_corredor = self._map_to_db(corredor, db_corredor)
        self.session.commit()
        self.session.refresh(db_corredor)
        return self._map_to_domain(db_corredor)

    def delete(self, corredor_id: int):
        """Elimina un corredor por su ID técnico."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.id == corredor_id).first()
        if db_corredor is None:
            raise ValueError(f"No se encontró un corredor con el ID {corredor_id}")

        self.session.delete(db_corredor)
        self.session.commit()

    def search(self, query: str = None, esta_activo: bool = None) -> List[CorredorDomain]:
        """Busca corredores según criterios específicos."""
        db_query = self.session.query(CorredorModel)

        # Filtrar por estado activo/inactivo si se especifica
        if esta_activo is not None:
            if esta_activo:
                db_query = db_query.filter(CorredorModel.fecha_baja == None)
            else:
                db_query = db_query.filter(CorredorModel.fecha_baja != None)

        # Filtrar por término de búsqueda si se especifica
        if query:
            search_term = f"%{query}%"
            db_query = db_query.filter(
                or_(
                    CorredorModel.nombres.ilike(search_term),
                    CorredorModel.apellidos.ilike(search_term),
                    CorredorModel.documento.ilike(search_term),
                    CorredorModel.mail.ilike(search_term),
                    CorredorModel.localidad.ilike(search_term)
                )
            )

        db_corredores = db_query.all()
        return [self._map_to_domain(db_corredor) for db_corredor in db_corredores]