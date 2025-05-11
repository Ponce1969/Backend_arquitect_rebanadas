from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..application.interfaces.repositories import AbstractClienteRepository
from ..domain.entities import Cliente as ClienteDomain
from .models import Cliente as ClienteModel


class SQLAlchemyClienteRepository(AbstractClienteRepository):
    """Implementación SQLAlchemy del repositorio de Clientes."""

    def __init__(self, session: Session):
        self.session = session

    def _map_to_domain(self, db_cliente: ClienteModel) -> ClienteDomain:
        """Mapea un modelo SQLAlchemy a una entidad de dominio."""
        return ClienteDomain(
            id=db_cliente.id,
            numero_cliente=db_cliente.numero_cliente,
            nombres=db_cliente.nombres,
            apellidos=db_cliente.apellidos,
            tipo_documento_id=db_cliente.tipo_documento_id,
            numero_documento=db_cliente.numero_documento,
            fecha_nacimiento=db_cliente.fecha_nacimiento,
            direccion=db_cliente.direccion,
            localidad=db_cliente.localidad,
            telefonos=db_cliente.telefonos,
            movil=db_cliente.movil,
            mail=db_cliente.mail,
            observaciones=db_cliente.observaciones,
            creado_por_id=db_cliente.creado_por_id,
            modificado_por_id=db_cliente.modificado_por_id,
            fecha_creacion=db_cliente.fecha_creacion,
            fecha_modificacion=db_cliente.fecha_modificacion,
        )

    def _map_to_model(self, cliente: ClienteDomain) -> ClienteModel:
        """Mapea una entidad de dominio a un modelo SQLAlchemy."""
        return ClienteModel(
            id=cliente.id,
            numero_cliente=cliente.numero_cliente,
            nombres=cliente.nombres,
            apellidos=cliente.apellidos,
            tipo_documento_id=cliente.tipo_documento_id,
            numero_documento=cliente.numero_documento,
            fecha_nacimiento=cliente.fecha_nacimiento,
            direccion=cliente.direccion,
            localidad=cliente.localidad,
            telefonos=cliente.telefonos,
            movil=cliente.movil,
            mail=cliente.mail,
            observaciones=cliente.observaciones,
            creado_por_id=cliente.creado_por_id,
            modificado_por_id=cliente.modificado_por_id,
            fecha_creacion=cliente.fecha_creacion,
            fecha_modificacion=cliente.fecha_modificacion,
        )

    def add(self, cliente: ClienteDomain) -> ClienteDomain:
        db_cliente = self._map_to_model(cliente)
        self.session.add(db_cliente)
        self.session.flush()  # Para obtener el ID generado
        return self._map_to_domain(db_cliente)

    def get_by_id(self, cliente_id: UUID) -> ClienteDomain | None:
        db_cliente = self.session.query(ClienteModel).filter(
            ClienteModel.id == cliente_id
        ).first()
        return self._map_to_domain(db_cliente) if db_cliente else None

    def get_by_numero_cliente(self, numero_cliente: int) -> ClienteDomain | None:
        db_cliente = self.session.query(ClienteModel).filter(
            ClienteModel.numero_cliente == numero_cliente
        ).first()
        return self._map_to_domain(db_cliente) if db_cliente else None

    def get_by_numero_documento(self, numero_documento: str) -> ClienteDomain | None:
        db_cliente = self.session.query(ClienteModel).filter(
            ClienteModel.numero_documento == numero_documento
        ).first()
        return self._map_to_domain(db_cliente) if db_cliente else None

    def get_by_email(self, email: str) -> ClienteDomain | None:
        db_cliente = self.session.query(ClienteModel).filter(
            ClienteModel.mail == email
        ).first()
        return self._map_to_domain(db_cliente) if db_cliente else None

    def get_all(self) -> list[ClienteDomain]:
        db_clientes = self.session.query(ClienteModel).all()
        return [self._map_to_domain(db_cliente) for db_cliente in db_clientes]

    def update(self, cliente: ClienteDomain) -> ClienteDomain:
        db_cliente = self.session.query(ClienteModel).filter(
            ClienteModel.id == cliente.id
        ).first()
        if db_cliente:
            # Actualizar todos los campos
            db_cliente.nombres = cliente.nombres
            db_cliente.apellidos = cliente.apellidos
            db_cliente.tipo_documento_id = cliente.tipo_documento_id
            db_cliente.numero_documento = cliente.numero_documento
            db_cliente.fecha_nacimiento = cliente.fecha_nacimiento
            db_cliente.direccion = cliente.direccion
            db_cliente.localidad = cliente.localidad
            db_cliente.telefonos = cliente.telefonos
            db_cliente.movil = cliente.movil
            db_cliente.mail = cliente.mail
            db_cliente.observaciones = cliente.observaciones
            db_cliente.modificado_por_id = cliente.modificado_por_id
            # No actualizamos fecha_creacion ni creado_por_id
            # fecha_modificacion se actualiza automáticamente por onupdate
            self.session.flush()
            return self._map_to_domain(db_cliente)
        return cliente  # Devuelve la entidad original si no se encuentra

    def delete(self, cliente_id: UUID) -> bool:
        db_cliente = self.session.query(ClienteModel).filter(
            ClienteModel.id == cliente_id
        ).first()
        if db_cliente:
            self.session.delete(db_cliente)
            return True
        return False

    def search(self, query: str) -> list[ClienteDomain]:
        # Búsqueda por nombres, apellidos o número de documento
        search_pattern = f"%{query}%"
        db_clientes = self.session.query(ClienteModel).filter(
            or_(
                ClienteModel.nombres.ilike(search_pattern),
                ClienteModel.apellidos.ilike(search_pattern),
                ClienteModel.numero_documento.ilike(search_pattern)
            )
        ).all()
        return [self._map_to_domain(db_cliente) for db_cliente in db_clientes]
