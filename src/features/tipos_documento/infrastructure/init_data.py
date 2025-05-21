from sqlalchemy.orm import Session

from src.features.tipos_documento.domain.entities import TipoDocumento
from src.features.tipos_documento.infrastructure.repositories import SQLAlchemyTipoDocumentoRepository


def init_tipos_documento(db: Session):
    """Inicializa los tipos de documento por defecto si no existen."""
    repository = SQLAlchemyTipoDocumentoRepository(db)
    
    # Verificar si ya existe algún tipo de documento
    tipos = repository.get_all()
    if tipos:
        print("Ya existen tipos de documento en la base de datos.")
        return
    
    # Crear tipos de documento por defecto
    tipos_default = [
        TipoDocumento(
            codigo="DNI",
            nombre="Documento Nacional de Identidad",
            descripcion="Documento de identidad para ciudadanos",
            es_default=True,
            esta_activo=True
        ),
        TipoDocumento(
            codigo="RUT",
            nombre="Rol Único Tributario",
            descripcion="Documento de identidad fiscal",
            es_default=False,
            esta_activo=True
        ),
        TipoDocumento(
            codigo="PASAPORTE",
            nombre="Pasaporte",
            descripcion="Documento de viaje internacional",
            es_default=False,
            esta_activo=True
        )
    ]
    
    # Guardar los tipos de documento
    for tipo in tipos_default:
        try:
            repository.add(tipo)
            print(f"Tipo de documento '{tipo.codigo}' creado correctamente.")
        except Exception as e:
            print(f"Error al crear tipo de documento '{tipo.codigo}': {e}")
