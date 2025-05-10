from sqlalchemy.orm import Session
from datetime import date

from src.features.corredores.infrastructure.models import Corredor


def init_corredores(db: Session):
    """Inicializa los corredores predeterminados en la base de datos."""
    # Lista de corredores predeterminados
    corredores_default = [
        {
            "numero": 1,
            "tipo": "corredor",
            "nombres": "Juan",
            "apellidos": "Pérez",
            "documento": "12345678",
            "direccion": "Av. Principal 123",
            "localidad": "Ciudad",
            "telefonos": "11-1234-5678",
            "movil": "11-9876-5432",
            "mail": "juan.perez@ejemplo.com",
            "fecha_alta": date.today(),
            "matricula": "MAT-001"
        },
        {
            "numero": 2,
            "tipo": "productor",
            "nombres": "María",
            "apellidos": "González",
            "documento": "87654321",
            "direccion": "Calle Secundaria 456",
            "localidad": "Provincia",
            "telefonos": "11-8765-4321",
            "movil": "11-2345-6789",
            "mail": "maria.gonzalez@ejemplo.com",
            "fecha_alta": date.today(),
            "matricula": "MAT-002",
            "especializacion": "Seguros de Vida"
        }
    ]
    
    # Verificar si ya existen corredores
    existing_count = db.query(Corredor).count()
    if existing_count > 0:
        print(f"Ya existen {existing_count} corredores en la base de datos. Omitiendo inicialización.")
        return
    
    # Crear los corredores
    for corredor_data in corredores_default:
        db_corredor = Corredor(**corredor_data)
        db.add(db_corredor)
    
    db.commit()
    print(f"Se han inicializado {len(corredores_default)} corredores predeterminados.")
