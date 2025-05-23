from uuid import UUID

from ..domain.entities import Cliente
from ..domain.exceptions import (
    ClienteDocumentoExistsException,
    ClienteDocumentoNotFoundException,
    ClienteEmailExistsException,
    ClienteNotFoundException,
    ClienteNumeroNotFoundException,
)
from .dtos import ClienteCreate, ClienteResponse, ClienteSearchParams, ClienteUpdate
from .interfaces.repositories import IClienteRepository


class CrearClienteUseCase:
    """Caso de uso para crear un nuevo cliente."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, cliente_data: ClienteCreate) -> ClienteResponse:
        # Verificar si ya existe un cliente con el mismo número de documento
        existing = self.repository.get_by_numero_documento(cliente_data.numero_documento)
        if existing:
            raise ClienteDocumentoExistsException(cliente_data.numero_documento)

        # Verificar si ya existe un cliente con el mismo email
        existing = self.repository.get_by_email(cliente_data.mail)
        if existing:
            raise ClienteEmailExistsException(cliente_data.mail)

        # Crear entidad de dominio
        cliente = Cliente(
            nombres=cliente_data.nombres,
            apellidos=cliente_data.apellidos,
            tipo_documento_id=cliente_data.tipo_documento_id,
            numero_documento=cliente_data.numero_documento,
            fecha_nacimiento=cliente_data.fecha_nacimiento,
            direccion=cliente_data.direccion,
            localidad=cliente_data.localidad,
            telefonos=cliente_data.telefonos,
            movil=cliente_data.movil,
            mail=cliente_data.mail,
            observaciones=cliente_data.observaciones,
            creado_por_id=cliente_data.creado_por_id,
            modificado_por_id=cliente_data.modificado_por_id,
        )

        # Guardar en el repositorio
        created_cliente = self.repository.add(cliente)

        # Convertir a DTO de respuesta
        return ClienteResponse(
            id=created_cliente.id,
            numero_cliente=created_cliente.numero_cliente,
            nombres=created_cliente.nombres,
            apellidos=created_cliente.apellidos,
            tipo_documento_id=created_cliente.tipo_documento_id,
            numero_documento=created_cliente.numero_documento,
            fecha_nacimiento=created_cliente.fecha_nacimiento,
            direccion=created_cliente.direccion,
            localidad=created_cliente.localidad,
            telefonos=created_cliente.telefonos,
            movil=created_cliente.movil,
            mail=created_cliente.mail,
            observaciones=created_cliente.observaciones,
            creado_por_id=created_cliente.creado_por_id,
            modificado_por_id=created_cliente.modificado_por_id,
            fecha_creacion=created_cliente.fecha_creacion,
            fecha_modificacion=created_cliente.fecha_modificacion,
        )


class ObtenerClienteUseCase:
    """Caso de uso para obtener un cliente por su ID."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, cliente_id: UUID) -> ClienteResponse:
        cliente = self.repository.get_by_id(cliente_id)
        if not cliente:
            raise ClienteNotFoundException(cliente_id)

        return ClienteResponse(
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


class ObtenerClientePorNumeroUseCase:
    """Caso de uso para obtener un cliente por su número de cliente."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, numero_cliente: int) -> ClienteResponse:
        cliente = self.repository.get_by_numero_cliente(numero_cliente)
        if not cliente:
            raise ClienteNumeroNotFoundException(numero_cliente)

        return ClienteResponse(
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


class ObtenerClientePorDocumentoUseCase:
    """Caso de uso para obtener un cliente por su número de documento."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, numero_documento: str) -> ClienteResponse:
        cliente = self.repository.get_by_numero_documento(numero_documento)
        if not cliente:
            raise ClienteDocumentoNotFoundException(numero_documento)

        return ClienteResponse(
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


class ListarClientesUseCase:
    """Caso de uso para listar todos los clientes."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self) -> list[ClienteResponse]:
        clientes = self.repository.get_all()
        return [
            ClienteResponse(
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
            for cliente in clientes
        ]


class BuscarClientesUseCase:
    """Caso de uso para buscar clientes."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, search_params: ClienteSearchParams) -> list[ClienteResponse]:
        """Ejecuta la búsqueda de clientes según los parámetros especificados.
        
        Args:
            search_params: Parámetros de búsqueda (query, tipo_documento_id, localidad)
            
        Returns:
            Lista de clientes que coinciden con los criterios de búsqueda
        """
        # Realizar la búsqueda con todos los parámetros disponibles
        clientes = self.repository.search(
            query=search_params.query,
            tipo_documento_id=search_params.tipo_documento_id,
            localidad=search_params.localidad
        )
        
        # Si no hay resultados, devolver lista vacía
        if not clientes:
            return []
            
        # Convertir entidades de dominio a DTOs de respuesta
        return [
            ClienteResponse(
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
            for cliente in clientes
        ]


class ActualizarClienteUseCase:
    """Caso de uso para actualizar un cliente existente."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, cliente_id: UUID, cliente_data: ClienteUpdate) -> ClienteResponse:
        # Verificar si el cliente existe
        existing_cliente = self.repository.get_by_id(cliente_id)
        if not existing_cliente:
            raise ClienteNotFoundException(cliente_id)

        # Verificar si el número de documento ya está en uso por otro cliente
        if cliente_data.numero_documento and cliente_data.numero_documento != existing_cliente.numero_documento:
            existing = self.repository.get_by_numero_documento(cliente_data.numero_documento)
            if existing and existing.id != cliente_id:
                raise ClienteDocumentoExistsException(cliente_data.numero_documento)

        # Verificar si el email ya está en uso por otro cliente
        if cliente_data.mail and cliente_data.mail != existing_cliente.mail:
            existing = self.repository.get_by_email(cliente_data.mail)
            if existing and existing.id != cliente_id:
                raise ClienteEmailExistsException(cliente_data.mail)

        # Actualizar los campos de la entidad existente
        updated_cliente = Cliente(
            id=existing_cliente.id,
            numero_cliente=existing_cliente.numero_cliente,
            nombres=cliente_data.nombres if cliente_data.nombres is not None else existing_cliente.nombres,
            apellidos=cliente_data.apellidos if cliente_data.apellidos is not None else existing_cliente.apellidos,
            tipo_documento_id=cliente_data.tipo_documento_id if cliente_data.tipo_documento_id is not None else existing_cliente.tipo_documento_id,
            numero_documento=cliente_data.numero_documento if cliente_data.numero_documento is not None else existing_cliente.numero_documento,
            fecha_nacimiento=cliente_data.fecha_nacimiento if cliente_data.fecha_nacimiento is not None else existing_cliente.fecha_nacimiento,
            direccion=cliente_data.direccion if cliente_data.direccion is not None else existing_cliente.direccion,
            localidad=cliente_data.localidad if cliente_data.localidad is not None else existing_cliente.localidad,
            telefonos=cliente_data.telefonos if cliente_data.telefonos is not None else existing_cliente.telefonos,
            movil=cliente_data.movil if cliente_data.movil is not None else existing_cliente.movil,
            mail=cliente_data.mail if cliente_data.mail is not None else existing_cliente.mail,
            observaciones=cliente_data.observaciones if cliente_data.observaciones is not None else existing_cliente.observaciones,
            creado_por_id=existing_cliente.creado_por_id,  # No se actualiza
            modificado_por_id=cliente_data.modificado_por_id,
            fecha_creacion=existing_cliente.fecha_creacion,  # No se actualiza
            fecha_modificacion=existing_cliente.fecha_modificacion,  # Se actualiza automáticamente
        )

        # Actualizar en el repositorio
        updated = self.repository.update(updated_cliente)

        # Convertir a DTO de respuesta
        return ClienteResponse(
            id=updated.id,
            numero_cliente=updated.numero_cliente,
            nombres=updated.nombres,
            apellidos=updated.apellidos,
            tipo_documento_id=updated.tipo_documento_id,
            numero_documento=updated.numero_documento,
            fecha_nacimiento=updated.fecha_nacimiento,
            direccion=updated.direccion,
            localidad=updated.localidad,
            telefonos=updated.telefonos,
            movil=updated.movil,
            mail=updated.mail,
            observaciones=updated.observaciones,
            creado_por_id=updated.creado_por_id,
            modificado_por_id=updated.modificado_por_id,
            fecha_creacion=updated.fecha_creacion,
            fecha_modificacion=updated.fecha_modificacion,
        )


class EliminarClienteUseCase:
    """Caso de uso para eliminar un cliente."""

    def __init__(self, repository: IClienteRepository):
        self.repository = repository

    def execute(self, cliente_id: UUID) -> bool:
        # Verificar si el cliente existe antes de intentar eliminarlo
        if not self.repository.get_by_id(cliente_id):
            raise ClienteNotFoundException(cliente_id)
        return self.repository.delete(cliente_id)
