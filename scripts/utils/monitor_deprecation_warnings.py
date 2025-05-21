#!/usr/bin/env python
"""
Script para monitorear las advertencias de deprecación en la aplicación.

Este script configura un manejador de advertencias personalizado que registra
todas las advertencias de deprecación en un archivo de log.
"""

import os
import sys
import warnings
import logging
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Configurar el logger
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

log_file = log_dir / 'deprecation_warnings.log'

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('deprecation_monitor')


def custom_warning_handler(message, category, filename, lineno, file=None, line=None):
    """Manejador personalizado para advertencias que las registra en el log."""
    if category == DeprecationWarning:
        # Obtener el módulo que genera la advertencia
        module = filename.replace('/', '.').replace('.py', '')
        if 'site-packages' in module:
            # Ignorar advertencias de paquetes externos
            return
        
        # Registrar la advertencia en el log
        logger.warning(
            f"[{category.__name__}] {message} | En: {filename}:{lineno}"
        )


# Configurar el manejador de advertencias personalizado
warnings.showwarning = custom_warning_handler

# Configurar warnings para que siempre se muestren
warnings.filterwarnings('always', category=DeprecationWarning)


def main():
    """Función principal que importa los módulos de compatibilidad."""
    logger.info(f"Iniciando monitoreo de advertencias de deprecación: {datetime.now()}")
    
    # Importar los módulos de compatibilidad
    modules_to_check = [
        'src.domain.shared.entities',
        'src.domain.shared.dtos',
        'src.domain.shared.dtos_tipo_documento',
        'src.domain.shared.use_cases',
        'src.domain.shared.use_cases_tipo_documento',
        'src.infrastructure.database.models'
    ]
    
    for module_name in modules_to_check:
        try:
            __import__(module_name)
            logger.info(f"Módulo {module_name} importado correctamente.")
        except Exception as e:
            logger.error(f"Error al importar el módulo {module_name}: {e}")
    
    logger.info(f"Monitoreo de advertencias completado: {datetime.now()}")


if __name__ == '__main__':
    main()
