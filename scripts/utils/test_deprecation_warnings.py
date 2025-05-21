#!/usr/bin/env python
"""
Script para probar las advertencias de deprecación en los archivos de compatibilidad.
"""

import os
import sys
import warnings

# Agregar el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# Configurar warnings para que siempre se muestren
warnings.filterwarnings('always', category=DeprecationWarning)

print("Importando archivos de compatibilidad...")

# Importar los archivos de compatibilidad
try:
    print("\nImportando src.domain.shared.entities...")
    import src.domain.shared.entities
    print("OK")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\nImportando src.domain.shared.dtos...")
    import src.domain.shared.dtos
    print("OK")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\nImportando src.domain.shared.dtos_tipo_documento...")
    import src.domain.shared.dtos_tipo_documento
    print("OK")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\nImportando src.domain.shared.use_cases...")
    import src.domain.shared.use_cases
    print("OK")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\nImportando src.domain.shared.use_cases_tipo_documento...")
    import src.domain.shared.use_cases_tipo_documento
    print("OK")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\nImportando src.infrastructure.database.models...")
    import src.infrastructure.database.models
    print("OK")
except Exception as e:
    print(f"Error: {e}")

print("\nPrueba completada.")
