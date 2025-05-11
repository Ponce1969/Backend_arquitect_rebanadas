from sqlalchemy.orm import Session

from src.infrastructure.database.models import TipoDocumento


def init_tipos_documento(db: Session):
    """Inicializa los tipos de documento predeterminados en la base de datos."""
    # Lista de tipos de documento predeterminados
    tipos_documento_default = [
        {"codigo": "DNI", "nombre": "Documento Nacional de Identidad", "descripcion": "Documento Nacional de Identidad", "es_default": True},
        {"codigo": "PASAPORTE", "nombre": "Pasaporte Internacional", "descripcion": "Pasaporte Internacional"},
        {"codigo": "CUIT", "nombre": "Clave Única de Identificación Tributaria", "descripcion": "Clave Única de Identificación Tributaria"},
        {"codigo": "CUIL", "nombre": "Clave Única de Identificación Laboral", "descripcion": "Clave Única de Identificación Laboral"},
        {"codigo": "CEDULA", "nombre": "Cédula de Identidad", "descripcion": "Cédula de Identidad"}
    ]
    
    # Verificar si ya existen tipos de documento
    existing_count = db.query(TipoDocumento).count()
    if existing_count > 0:
        print(f"Ya existen {existing_count} tipos de documento en la base de datos. Omitiendo inicialización.")
        return
    
    # Crear los tipos de documento
    for tipo_doc in tipos_documento_default:
        db_tipo_doc = TipoDocumento(**tipo_doc)
        db.add(db_tipo_doc)
    
    db.commit()
    print(f"Se han inicializado {len(tipos_documento_default)} tipos de documento predeterminados.")
