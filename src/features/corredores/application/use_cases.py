from datetime import date, datetime
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

    def _generar_numero_corredor(self) -> int:
        """Genera un nuevo número de corredor secuencial."""
        # Obtener el último número de corredor a través del repositorio
        ultimo_numero = self.repository.obtener_ultimo_numero()
        return (ultimo_numero or 0) + 1

    def _separar_nombre_apellido(self, nombre_completo: str) -> tuple[str, str]:
        """Separa nombres y apellidos de manera más robusta."""
        partes = nombre_completo.strip().split()
        if not partes:
            return "", ""
        if len(partes) == 1:
            return partes[0], ""
        return " ".join(partes[:1]), " ".join(partes[1:])

    def execute(self, corredor_data: CorredorCreate) -> CorredorDto:
        """Ejecuta el caso de uso para crear un nuevo corredor."""
        # Validar que el nombre no esté vacío
        if not corredor_data.nombre or len(corredor_data.nombre.strip()) < 2:
            raise ValueError("El nombre del corredor es requerido y debe tener al menos 2 caracteres")

        # Verificar si ya existe un corredor con el mismo documento
        if corredor_data.documento:
            existing_doc, _ = self.repository.get_by_documento(corredor_data.documento)
            if existing_doc:
                raise ValueError(f"Ya existe un corredor con el documento {corredor_data.documento}")

        # Verificar si ya existe un corredor con el mismo email
        if corredor_data.email:
            existing_email, _ = self.repository.get_by_email(corredor_data.email)
            if existing_email:
                raise ValueError(f"Ya existe un corredor con el email {corredor_data.email}")

        # Generar número de corredor
        numero = self._generar_numero_corredor()

        # Separar nombres y apellidos
        nombres, apellidos = self._separar_nombre_apellido(corredor_data.nombre)

        # Crear entidad de dominio
        new_corredor = CorredorDomain(
            numero=numero,
            nombres=nombres,
            apellidos=apellidos,
            documento=corredor_data.documento or "",
            direccion=corredor_data.direccion or "",
            localidad=corredor_data.localidad or "",
            telefonos=corredor_data.telefono or "",
            mail=corredor_data.email or "",
            observaciones=corredor_data.observaciones or "",
            matricula=corredor_data.matricula or "",
            especializacion=corredor_data.especializacion or "",
            fecha_alta=date.today(),
            fecha_baja=None,
        )

        # Guardar en el repositorio
        saved_id = self.repository.save(new_corredor)
        now = datetime.now()

        # Retornar DTO con el corredor creado
        return CorredorDto(
            id=saved_id,
            numero=new_corredor.numero,
            nombre=f"{new_corredor.nombres} {new_corredor.apellidos}".strip(),
            documento=new_corredor.documento or "",
            direccion=new_corredor.direccion,
            localidad=new_corredor.localidad or "",
            telefono=new_corredor.telefonos,
            email=new_corredor.mail,
            contacto=None,
            observaciones=new_corredor.observaciones or "",
            matricula=new_corredor.matricula or "",
            especializacion=new_corredor.especializacion or "",
            comision_default=0.0,
            esta_activo=new_corredor.fecha_baja is None,
            fecha_creacion=now,
            fecha_actualizacion=now
        )


class ObtenerCorredorPorIdUseCase:
    """Caso de uso para obtener un corredor por su ID."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, corredor_id: int) -> CorredorDto | None:
        corredor, id = self.repository.get_by_id(corredor_id)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            documento=corredor.documento or "",
            direccion=corredor.direccion,
            localidad=corredor.localidad or "",
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            observaciones=corredor.observaciones or "",
            matricula=corredor.matricula or "",
            especializacion=corredor.especializacion or "",
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None,
            fecha_creacion=corredor.fecha_alta if hasattr(corredor, 'fecha_alta') else datetime.now(),
            fecha_actualizacion=datetime.now()
        )


class ObtenerCorredorPorNumeroUseCase:
    """Caso de uso para obtener un corredor por su número."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, numero: int) -> CorredorDto | None:
        corredor, id = self.repository.get_by_numero(numero)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            documento=corredor.documento or "",
            direccion=corredor.direccion,
            localidad=corredor.localidad or "",
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            observaciones=corredor.observaciones or "",
            matricula=corredor.matricula or "",
            especializacion=corredor.especializacion or "",
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None,
            fecha_creacion=corredor.fecha_alta if hasattr(corredor, 'fecha_alta') else datetime.now(),
            fecha_actualizacion=datetime.now()
        )


class ObtenerCorredorPorDocumentoUseCase:
    """Caso de uso para obtener un corredor por su documento."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, documento: str) -> CorredorDto | None:
        corredor, id = self.repository.get_by_documento(documento)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            documento=corredor.documento or "",
            direccion=corredor.direccion,
            localidad=corredor.localidad or "",
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            observaciones=corredor.observaciones or "",
            matricula=corredor.matricula or "",
            especializacion=corredor.especializacion or "",
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None,
            fecha_creacion=corredor.fecha_alta if hasattr(corredor, 'fecha_alta') else datetime.now(),
            fecha_actualizacion=datetime.now()
        )


class ObtenerCorredorPorEmailUseCase:
    """Caso de uso para obtener un corredor por su email."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, email: str) -> CorredorDto | None:
        corredor, id = self.repository.get_by_email(email)
        if not corredor:
            return None

        return CorredorDto(
            id=corredor.id,
            numero=corredor.numero,
            nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
            documento=corredor.documento or "",
            direccion=corredor.direccion,
            localidad=corredor.localidad or "",
            telefono=corredor.telefonos,
            email=corredor.mail,
            contacto=None,
            observaciones=corredor.observaciones or "",
            matricula=corredor.matricula or "",
            especializacion=corredor.especializacion or "",
            comision_default=0.0,
            esta_activo=corredor.fecha_baja is None,
            fecha_creacion=corredor.fecha_alta if hasattr(corredor, 'fecha_alta') else datetime.now(),
            fecha_actualizacion=datetime.now()
        )


class ListarCorredoresUseCase:
    """Caso de uso para listar todos los corredores."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self) -> list[CorredorDto]:
        corredores_with_ids = self.repository.get_all()
        return [
            CorredorDto(
                id=corredor_id,
                numero=corredor.numero,
                nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
                documento=corredor.documento or "",
                direccion=corredor.direccion,
                localidad=corredor.localidad or "",
                telefono=corredor.telefonos,
                email=corredor.mail,
                contacto=None,
                observaciones=corredor.observaciones or "",
                matricula=corredor.matricula or "",
                especializacion=corredor.especializacion or "",
                comision_default=0.0,
                esta_activo=corredor.fecha_baja is None,
                fecha_creacion=corredor.fecha_alta if hasattr(corredor, 'fecha_alta') else datetime.now(),
                fecha_actualizacion=datetime.now()
            )
            for corredor, corredor_id in corredores_with_ids
        ]


class ActualizarCorredorUseCase:
    """Caso de uso para actualizar un corredor existente."""

    def __init__(self, repository: ICorredorRepository):
        self.repository = repository

    def execute(self, numero: int, corredor_data: CorredorUpdate) -> CorredorDto | None:
        # Verificar si el corredor existe
        existing_corredor, existing_id = self.repository.get_by_numero(numero)
        if not existing_corredor:
            return None

        # Si se está actualizando el email, verificar que no exista otro corredor con ese email
        if corredor_data.email and corredor_data.email != existing_corredor.mail:
            existing_email, _ = self.repository.get_by_email(corredor_data.email)
            if existing_email and existing_email.numero != numero:
                raise ValueError(f"Ya existe un corredor con el email {corredor_data.email}")

        # Actualizar los campos del corredor
        if corredor_data.nombre is not None:
            nombres_apellidos = corredor_data.nombre.split()
            if len(nombres_apellidos) > 1:
                existing_corredor.nombres = nombres_apellidos[0]
                existing_corredor.apellidos = " ".join(nombres_apellidos[1:])
            else:
                existing_corredor.nombres = corredor_data.nombre

        if corredor_data.direccion is not None:
            existing_corredor.direccion = corredor_data.direccion

        if corredor_data.telefono is not None:
            existing_corredor.telefonos = corredor_data.telefono

        if corredor_data.email is not None:
            existing_corredor.mail = corredor_data.email

        if corredor_data.contacto is not None:
            # Manejar el campo contacto según la lógica de negocio
            pass

        if corredor_data.comision_default is not None:
            # Manejar el campo comision_default según la lógica de negocio
            pass

        if corredor_data.esta_activo is not None:
            # Actualizar fecha_baja según el estado activo
            from datetime import date
            if not corredor_data.esta_activo and existing_corredor.fecha_baja is None:
                existing_corredor.fecha_baja = date.today()
            elif corredor_data.esta_activo and existing_corredor.fecha_baja is not None:
                existing_corredor.fecha_baja = None

        # Actualizar el corredor en el repositorio
        updated_corredor, updated_id = self.repository.update(existing_corredor)

        # Convertir la entidad de dominio actualizada a DTO de respuesta
        return CorredorDto(
            id=updated_id,
            numero=updated_corredor.numero,
            nombre=f"{updated_corredor.nombres} {updated_corredor.apellidos}".strip(),
            documento=updated_corredor.documento or "",
            direccion=updated_corredor.direccion,
            localidad=updated_corredor.localidad or "",
            telefono=updated_corredor.telefonos,
            email=updated_corredor.mail,
            contacto=None,
            observaciones=updated_corredor.observaciones or "",
            matricula=updated_corredor.matricula or "",
            especializacion=updated_corredor.especializacion or "",
            comision_default=0.0,
            esta_activo=updated_corredor.fecha_baja is None,
            fecha_creacion=updated_corredor.fecha_alta if hasattr(updated_corredor, 'fecha_alta') else datetime.now(),
            fecha_actualizacion=datetime.now()
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
        corredores_with_ids = self.repository.search(
            query=search_params.query,
            esta_activo=search_params.esta_activo
        )
        
        return [
            CorredorDto(
                id=corredor_id,
                numero=corredor.numero,
                nombre=f"{corredor.nombres} {corredor.apellidos}".strip(),
                documento=corredor.documento or "",
                direccion=corredor.direccion,
                localidad=corredor.localidad or "",
                telefono=corredor.telefonos,
                email=corredor.mail,
                contacto=None,
                observaciones=corredor.observaciones or "",
                matricula=corredor.matricula or "",
                especializacion=corredor.especializacion or "",
                comision_default=0.0,
                esta_activo=corredor.fecha_baja is None,
                fecha_creacion=corredor.fecha_alta if hasattr(corredor, 'fecha_alta') else datetime.now(),
                fecha_actualizacion=datetime.now()
            )
            for corredor, corredor_id in corredores_with_ids
        ]
