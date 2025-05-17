
from ..domain.entities import Corredor as CorredorDomain
from .dtos import (
    CorredorCreate,
    CorredorDto,
    CorredorSearchParams,
    CorredorUpdate,
)
from .interfaces.repositories import ICorredorRepository


class CrearCorredorUseCase:
    """Caso de uso para crear un nuevo corredor."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, corredor_data: CorredorCreate) -> CorredorDto:
        # Verificar si ya existe un corredor con el mismo email o documento
        existing_email = self.repository.get_by_email(corredor_data.email)
        if existing_email:
            raise ValueError(f"Ya existe un corredor con el email {corredor_data.email}")

        # Crear la entidad de dominio
        corredor = CorredorDomain(
            numero=None,  # Se asignará en la base de datos
            nombres=corredor_data.nombre.split()[0] if len(corredor_data.nombre.split()) > 1 else corredor_data.nombre,
            apellidos=" ".join(corredor_data.nombre.split()[1:]) if len(corredor_data.nombre.split()) > 1 else "",
            documento="",  # Opcional en el DTO de creación
            direccion=corredor_data.direccion,
            localidad="",  # Opcional en el DTO de creación
            mail=corredor_data.email,
            tipo="corredor",
            telefonos=corredor_data.telefono,
            movil="",  # Opcional en el DTO de creación
            observaciones="",  # Opcional en el DTO de creación
            fecha_alta=None,  # Se asignará automáticamente
            fecha_baja=None,
            matricula="",  # Opcional en el DTO de creación
            especializacion="",  # Opcional en el DTO de creación
            usuarios=[],
            clientes_asociados=[]
        )

        # Guardar el corredor en el repositorio
        new_corredor = self.repository.add(corredor)

        # Convertir la entidad de dominio a DTO de respuesta
        return CorredorDto(
            id=new_corredor.id,
            numero=new_corredor.numero,
            nombre=f"{new_corredor.nombres} {new_corredor.apellidos}".strip(),
            direccion=new_corredor.direccion,
            telefono=new_corredor.telefonos,
            email=new_corredor.mail,
            contacto=None,
            comision_default=0.0,
            esta_activo=new_corredor.fecha_baja is None
        )


class ObtenerCorredorPorIdUseCase:
    """Caso de uso para obtener un corredor por su ID."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, corredor_id: int) -> CorredorDto | None:
        corredor = self.repository.get_by_id(corredor_id)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            direccion=corredor.direccion,
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None
        )


class ObtenerCorredorPorNumeroUseCase:
    """Caso de uso para obtener un corredor por su número."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, numero: int) -> CorredorDto | None:
        corredor = self.repository.get_by_numero(numero)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            direccion=corredor.direccion,
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None
        )


class ObtenerCorredorPorDocumentoUseCase:
    """Caso de uso para obtener un corredor por su documento."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, documento: str) -> CorredorDto | None:
        corredor = self.repository.get_by_documento(documento)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            direccion=corredor.direccion,
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None
        )


class ObtenerCorredorPorEmailUseCase:
    """Caso de uso para obtener un corredor por su email."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, email: str) -> CorredorDto | None:
        corredor = self.repository.get_by_email(email)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            direccion=corredor.direccion,
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None
        )


class ListarCorredoresUseCase:
    """Caso de uso para listar todos los corredores."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self) -> list[CorredorDto]:
        corredores = self.repository.get_all()
        return [
            CorredorDto(
                id=corredor.id,
                numero=corredor.numero,
                nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
                direccion=corredor.direccion,
                telefono=corredor.telefonos,
                email=corredor.mail,
                contacto=None,
                comision_default=0.0,
                esta_activo=corredor.fecha_baja is None
            )
            for corredor in corredores
        ]


class ActualizarCorredorUseCase:
    """Caso de uso para actualizar un corredor existente."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, numero: int, corredor_data: CorredorUpdate) -> CorredorDto | None:
        # Verificar si el corredor existe
        corredor = self.repository.get_by_numero(numero)
        if not corredor:
            return None

        # Verificar si el email ya está en uso por otro corredor
        if corredor_data.email and corredor_data.email != corredor.mail:
            existing_email = self.repository.get_by_email(corredor_data.email)
            if existing_email and existing_email.numero != numero:
                raise ValueError(f"Ya existe un corredor con el email {corredor_data.email}")

        # Actualizar los campos del corredor
        if corredor_data.nombre is not None:
            nombres_apellidos = corredor_data.nombre.split()
            if len(nombres_apellidos) > 1:
                corredor.nombres = nombres_apellidos[0]
                corredor.apellidos = " ".join(nombres_apellidos[1:])
            else:
                corredor.nombres = corredor_data.nombre

        if corredor_data.direccion is not None:
            corredor.direccion = corredor_data.direccion

        if corredor_data.telefono is not None:
            corredor.telefonos = corredor_data.telefono

        if corredor_data.email is not None:
            corredor.mail = corredor_data.email

        if corredor_data.contacto is not None:
            # Manejar el campo contacto según la lógica de negocio
            pass

        if corredor_data.comision_default is not None:
            # Manejar el campo comision_default según la lógica de negocio
            pass

        if corredor_data.esta_activo is not None:
            # Actualizar fecha_baja según el estado activo
            from datetime import date
            if not corredor_data.esta_activo and corredor.fecha_baja is None:
                corredor.fecha_baja = date.today()
            elif corredor_data.esta_activo and corredor.fecha_baja is not None:
                corredor.fecha_baja = None

        # Guardar los cambios en el repositorio
        updated_corredor = self.repository.update(corredor)

        # Convertir la entidad de dominio a DTO de respuesta
        return CorredorDto(
            id=updated_corredor.id,
            numero=updated_corredor.numero,
            nombre=f"{updated_corredor.nombres} {updated_corredor.apellidos}".strip(),
            direccion=updated_corredor.direccion,
            telefono=updated_corredor.telefonos,
            email=updated_corredor.mail,
            contacto=None,
            comision_default=0.0,
            esta_activo=updated_corredor.fecha_baja is None
        )


class EliminarCorredorUseCase:
    """Caso de uso para eliminar un corredor."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, corredor_id: int) -> bool:
        try:
            self.repository.delete(corredor_id)
            return True
        except ValueError:
            return False


class BuscarCorredoresUseCase:
    """Caso de uso para buscar corredores según criterios específicos."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, search_params: CorredorSearchParams) -> list[CorredorDto]:
        corredores = self.repository.search(
            query=search_params.query,
            esta_activo=search_params.esta_activo
        )

        return [
            CorredorDto(
                id=corredor.id,
                numero=corredor.numero,
                nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
                direccion=corredor.direccion,
                telefono=corredor.telefonos,
                email=corredor.mail,
                contacto=None,
                comision_default=0.0,
                esta_activo=corredor.fecha_baja is None
            )
            for corredor in corredores
        ]
