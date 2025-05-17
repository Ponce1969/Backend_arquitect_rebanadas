from sqlalchemy.orm import Session

from src.features.monedas.domain.entities import Moneda
from src.features.monedas.infrastructure.repositories import SQLAlchemyMonedaRepository


def init_monedas(db: Session):
    """Inicializa las monedas por defecto si no existen."""
    repository = SQLAlchemyMonedaRepository(db)
    
    # Verificar si ya existen monedas
    monedas = repository.get_all()
    if monedas:
        print("Ya existen monedas en la base de datos.")
        return
    
    # Crear monedas por defecto
    monedas_default = [
        Moneda(
            codigo="USD",
            nombre="Dólar Estadounidense",
            simbolo="$"
        ),
        Moneda(
            codigo="EUR",
            nombre="Euro",
            simbolo="€"
        ),
        Moneda(
            codigo="CLP",
            nombre="Peso Chileno",
            simbolo="$"
        ),
        Moneda(
            codigo="ARS",
            nombre="Peso Argentino",
            simbolo="$"
        )
    ]
    
    # Guardar las monedas
    for moneda in monedas_default:
        try:
            repository.add(moneda)
            print(f"Moneda '{moneda.codigo}' creada correctamente.")
        except Exception as e:
            print(f"Error al crear moneda '{moneda.codigo}': {e}")
