import warnings

# Emitir una advertencia de que este archivo está obsoleto
warnings.warn(
    "El archivo 'src/infrastructure/database/models.py' está obsoleto y será eliminado en futuras versiones. "\
    "Por favor, actualice sus importaciones para usar directamente los modelos desde sus nuevas ubicaciones.",
    DeprecationWarning, stacklevel=2
)

# Este archivo se mantiene para compatibilidad con código existente
# Las definiciones de modelos se han movido a sus respectivos slices

# Importamos los modelos desde sus nuevas ubicaciones

# Importamos las entidades de dominio desde sus nuevas ubicaciones

# Nota: Este archivo será eliminado en futuras versiones.
# Por favor, actualice sus importaciones para usar directamente los modelos
# desde sus nuevas ubicaciones en los slices correspondientes.
