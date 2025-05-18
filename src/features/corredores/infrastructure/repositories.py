
from sqlalchemy import or_, desc, func
from sqlalchemy.orm import Session

from ..application.interfaces.repositories import ICorredorRepository
from ..domain.entities import Corredor as CorredorDomain, Corredor
from .models import Corredor as CorredorModel


class SQLAlchemyCorredorRepository(ICorredorRepository):
    """Implementación SQLAlchemy del repositorio de Corredores."""

    def __init__(self, session: Session):
        self.session = session

    def _map_to_domain(self, db_corredor: CorredorModel) -> CorredorDomain:
        """Mapea un modelo SQLAlchemy a una entidad de dominio."""
        if not db_corredor:
            return None
            
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
        
    def _get_domain_with_id(self, db_corredor: CorredorModel) -> tuple[CorredorDomain, int]:
        """Mapea un modelo SQLAlchemy a una entidad de dominio y devuelve también su ID técnico.
        
        Este método es útil cuando necesitamos tanto la entidad de dominio como el ID técnico
        para construir DTOs en la capa de aplicación.
        
        Args:
            db_corredor: Modelo SQLAlchemy del corredor
            
        Returns:
            Tupla con la entidad de dominio y el ID técnico
        """
        if not db_corredor:
            return None, None
            
        return self._map_to_domain(db_corredor), db_corredor.id

    def _map_to_db(self, corredor: CorredorDomain, db_corredor: CorredorModel | None = None) -> CorredorModel:
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
        """Añade un nuevo corredor al repositorio.
        
        Args:
            corredor: Entidad de dominio del corredor a guardar
            
        Returns:
            CorredorDomain: Entidad de dominio del corredor guardado
            
        Raises:
            ValueError: Si ocurre un error al guardar el corredor
        """
        try:
            db_corredor = self._map_to_db(corredor)
            self.session.add(db_corredor)
            self.session.flush()  # Flush para obtener el ID generado
            
            # Confirmar la transacción
            self.session.commit()
            
            # Refrescar para obtener los datos completos
            self.session.refresh(db_corredor)
            return self._map_to_domain(db_corredor)
            
        except Exception as e:
            # Hacer rollback en caso de error
            self.session.rollback()
            print(f"Error al guardar el corredor: {str(e)}")
            raise ValueError(f"Error al guardar el corredor: {str(e)}") from e

    def get_by_id(self, corredor_id: int) -> tuple[CorredorDomain | None, int | None]:
        """Obtiene un corredor por su ID técnico.
        
        Returns:
            Tupla con la entidad de dominio y el ID técnico
        """
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.id == corredor_id).first()
        return self._get_domain_with_id(db_corredor) if db_corredor else (None, None)

    def get_by_numero(self, numero: int) -> tuple[CorredorDomain | None, int | None]:
        """Obtiene un corredor por su número (identificador de negocio).
        
        Returns:
            Tupla con la entidad de dominio y el ID técnico
        """
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.numero == numero).first()
        return self._get_domain_with_id(db_corredor) if db_corredor else (None, None)

    def get_by_documento(self, documento: str) -> tuple[CorredorDomain | None, int | None]:
        """Obtiene un corredor por su número de documento.
        
        Returns:
            Tupla con la entidad de dominio y el ID técnico
        """
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.documento == documento).first()
        return self._get_domain_with_id(db_corredor) if db_corredor else (None, None)

    def get_by_email(self, email: str) -> tuple[CorredorDomain | None, int | None]:
        """Obtiene un corredor por su dirección de correo electrónico.
        
        Returns:
            Tupla con la entidad de dominio y el ID técnico
        """
        db_corredor = self.session.query(CorredorModel).filter(
            func.lower(CorredorModel.mail) == email.lower()
        ).first()
        return self._get_domain_with_id(db_corredor) if db_corredor else (None, None)
        
    def get_ultimo_corredor(self) -> Corredor | None:
        """Obtiene el último corredor registrado por número de corredor.
        
        Returns:
            La entidad de dominio del último corredor o None si no hay corredores
            
        Raises:
            ValueError: Si ocurre un error al consultar la base de datos
        """
        try:
            db_corredor = self.session.query(CorredorModel).order_by(desc(CorredorModel.numero)).first()
            return self._map_to_domain(db_corredor) if db_corredor else None
        except Exception as e:
            print(f"Error al obtener el último corredor: {str(e)}")
            raise ValueError(f"Error al obtener el último corredor: {str(e)}") from e

    def get_all(self) -> list[tuple[CorredorDomain, int]]:
        """Obtiene todos los corredores.
        
        Returns:
            Lista de tuplas con la entidad de dominio y el ID técnico
        """
        db_corredores = self.session.query(CorredorModel).all()
        return [self._get_domain_with_id(db_corredor) for db_corredor in db_corredores]

    def update(self, corredor: CorredorDomain) -> tuple[CorredorDomain, int]:
        """Actualiza un corredor existente.
        
        Returns:
            Tupla con la entidad de dominio actualizada y el ID técnico
        """
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.numero == corredor.numero).first()
        if db_corredor is None:
            raise ValueError(f"No se encontró un corredor con el número {corredor.numero}")

        db_corredor = self._map_to_db(corredor, db_corredor)
        self.session.commit()
        self.session.refresh(db_corredor)
        return self._get_domain_with_id(db_corredor)

    def delete(self, corredor_id: int):
        """Elimina un corredor por su ID técnico."""
        db_corredor = self.session.query(CorredorModel).filter(CorredorModel.id == corredor_id).first()
        if db_corredor is None:
            raise ValueError(f"No se encontró un corredor con el ID {corredor_id}")

        self.session.delete(db_corredor)
        self.session.commit()

    def search(self, query: str = None, esta_activo: bool = None) -> list[tuple[CorredorDomain, int]]:
        """Busca corredores según criterios específicos.
        
        Returns:
            Lista de tuplas con la entidad de dominio y el ID técnico
        """
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
        return [self._get_domain_with_id(db_corredor) for db_corredor in db_corredores]