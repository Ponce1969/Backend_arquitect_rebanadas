import warnings

# Emitir una advertencia de que este archivo está obsoleto
warnings.warn(
    "El archivo 'src/domain/shared/entities.py' está obsoleto y será eliminado en futuras versiones. "\
    "Por favor, actualice sus importaciones para usar directamente las entidades desde sus nuevas ubicaciones.",
    DeprecationWarning, stacklevel=2
)

# Importamos las entidades desde sus respectivos slices para mantener compatibilidad

# Estas importaciones permiten que el código existente siga funcionando sin cambios
# mientras refactorizamos la arquitectura para seguir el patrón de vertical slicing
