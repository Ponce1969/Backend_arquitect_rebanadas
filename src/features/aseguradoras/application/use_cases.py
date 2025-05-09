from typing import List, Optional

from .dtos import AseguradoraCreate, AseguradoraUpdate, AseguradoraResponse
from .interfaces import AbstractAseguradoraRepository
from ..domain.entities import Aseguradora


class CrearAseguradoraUseCase:
    """Caso de uso para crear una nueva aseguradora."""

    def __init__(self, repository: AbstractAseguradoraRepository):
        self.repository = repository

    def execute(self, aseguradora_data: AseguradoraCreate) -> AseguradoraResponse:
        # Verificar si ya existe una aseguradora con el mismo nombre
        if aseguradora_data.nombre:
            existing = self.repository.get_by_nombre(aseguradora_data.nombre)
            if existing:
                raise ValueError(f"Ya existe una aseguradora con el nombre {aseguradora_data.nombre}")

        # Verificar si ya existe una aseguradora con el mismo identificador fiscal
        if aseguradora_data.identificador_fiscal:
            existing = self.repository.get_by_identificador_fiscal(aseguradora_data.identificador_fiscal)
            if existing:
                raise ValueError(f"Ya existe una aseguradora con el identificador fiscal {aseguradora_data.identificador_fiscal}")

        # Crear entidad de dominio
        aseguradora = Aseguradora(
            nombre=aseguradora_data.nombre,
            identificador_fiscal=aseguradora_data.identificador_fiscal,
            telefono=aseguradora_data.telefono,
            direccion=aseguradora_data.direccion,
            email=aseguradora_data.email,
            pagina_web=aseguradora_data.pagina_web,
            esta_activa=aseguradora_data.esta_activa,
            observaciones=aseguradora_data.observaciones,
        )

        # Guardar en el repositorio
        created_aseguradora = self.repository.add(aseguradora)

        # Convertir a DTO de respuesta
        return AseguradoraResponse(
            id=created_aseguradora.id,
            nombre=created_aseguradora.nombre,
            identificador_fiscal=created_aseguradora.identificador_fiscal,
            telefono=created_aseguradora.telefono,
            direccion=created_aseguradora.direccion,
            email=created_aseguradora.email,
            pagina_web=created_aseguradora.pagina_web,
            esta_activa=created_aseguradora.esta_activa,
            observaciones=created_aseguradora.observaciones,
            fecha_creacion=created_aseguradora.fecha_creacion,
            fecha_actualizacion=created_aseguradora.fecha_actualizacion,
        )


class ObtenerAseguradoraUseCase:
    """Caso de uso para obtener una aseguradora por su ID."""

    def __init__(self, repository: AbstractAseguradoraRepository):
        self.repository = repository

    def execute(self, aseguradora_id: int) -> Optional[AseguradoraResponse]:
        aseguradora = self.repository.get_by_id(aseguradora_id)
        if not aseguradora:
            return None

        return AseguradoraResponse(
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


class ListarAseguradorasUseCase:
    """Caso de uso para listar todas las aseguradoras."""

    def __init__(self, repository: AbstractAseguradoraRepository):
        self.repository = repository

    def execute(self) -> List[AseguradoraResponse]:
        aseguradoras = self.repository.get_all()
        return [
            AseguradoraResponse(
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
            for aseguradora in aseguradoras
        ]


class ActualizarAseguradoraUseCase:
    """Caso de uso para actualizar una aseguradora existente."""

    def __init__(self, repository: AbstractAseguradoraRepository):
        self.repository = repository

    def execute(self, aseguradora_id: int, aseguradora_data: AseguradoraUpdate) -> Optional[AseguradoraResponse]:
        # Verificar si la aseguradora existe
        existing_aseguradora = self.repository.get_by_id(aseguradora_id)
        if not existing_aseguradora:
            return None

        # Verificar si el nombre ya está en uso por otra aseguradora
        if aseguradora_data.nombre and aseguradora_data.nombre != existing_aseguradora.nombre:
            existing = self.repository.get_by_nombre(aseguradora_data.nombre)
            if existing and existing.id != aseguradora_id:
                raise ValueError(f"Ya existe otra aseguradora con el nombre {aseguradora_data.nombre}")

        # Verificar si el identificador fiscal ya está en uso por otra aseguradora
        if aseguradora_data.identificador_fiscal and aseguradora_data.identificador_fiscal != existing_aseguradora.identificador_fiscal:
            existing = self.repository.get_by_identificador_fiscal(aseguradora_data.identificador_fiscal)
            if existing and existing.id != aseguradora_id:
                raise ValueError(f"Ya existe otra aseguradora con el identificador fiscal {aseguradora_data.identificador_fiscal}")

        # Actualizar los campos de la entidad existente
        updated_aseguradora = Aseguradora(
            id=existing_aseguradora.id,
            nombre=aseguradora_data.nombre if aseguradora_data.nombre is not None else existing_aseguradora.nombre,
            identificador_fiscal=aseguradora_data.identificador_fiscal if aseguradora_data.identificador_fiscal is not None else existing_aseguradora.identificador_fiscal,
            telefono=aseguradora_data.telefono if aseguradora_data.telefono is not None else existing_aseguradora.telefono,
            direccion=aseguradora_data.direccion if aseguradora_data.direccion is not None else existing_aseguradora.direccion,
            email=aseguradora_data.email if aseguradora_data.email is not None else existing_aseguradora.email,
            pagina_web=aseguradora_data.pagina_web if aseguradora_data.pagina_web is not None else existing_aseguradora.pagina_web,
            esta_activa=aseguradora_data.esta_activa if aseguradora_data.esta_activa is not None else existing_aseguradora.esta_activa,
            observaciones=aseguradora_data.observaciones if aseguradora_data.observaciones is not None else existing_aseguradora.observaciones,
            fecha_creacion=existing_aseguradora.fecha_creacion,
            fecha_actualizacion=existing_aseguradora.fecha_actualizacion,
        )

        # Actualizar en el repositorio
        updated = self.repository.update(updated_aseguradora)

        # Convertir a DTO de respuesta
        return AseguradoraResponse(
            id=updated.id,
            nombre=updated.nombre,
            identificador_fiscal=updated.identificador_fiscal,
            telefono=updated.telefono,
            direccion=updated.direccion,
            email=updated.email,
            pagina_web=updated.pagina_web,
            esta_activa=updated.esta_activa,
            observaciones=updated.observaciones,
            fecha_creacion=updated.fecha_creacion,
            fecha_actualizacion=updated.fecha_actualizacion,
        )


class EliminarAseguradoraUseCase:
    """Caso de uso para eliminar una aseguradora."""

    def __init__(self, repository: AbstractAseguradoraRepository):
        self.repository = repository

    def execute(self, aseguradora_id: int) -> bool:
        return self.repository.delete(aseguradora_id)
