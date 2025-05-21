# Plan de Migración Detallado (Actualizado)

## Objetivo

Migrar la arquitectura del proyecto de forma ordenada desde la estructura antigua hacia la arquitectura de rebanadas verticales (vertical slicing), evitando la duplicación de código y asegurando que todas las pruebas sigan pasando durante el proceso.

## Principios Guía

1. **No duplicar código**: Antes de crear nuevos componentes, verificar si ya existen en otra parte del código.
2. **Migración gradual**: Migrar un componente a la vez, asegurándose de que todas las pruebas pasen después de cada cambio.
3. **Compatibilidad hacia atrás**: Mantener la compatibilidad con el código existente durante la transición.
4. **Documentación clara**: Documentar todos los cambios y el estado de la migración.

## Fases de Migración

### Fase 1: Preparación (✅ Completada)

- ✅ Crear la estructura de carpetas para la arquitectura de rebanadas verticales
- ✅ Migrar las entidades, DTOs y casos de uso a sus respectivas características
- ✅ Implementar advertencias de obsolescencia en los archivos antiguos

### Fase 2: Migración de Componentes Compartidos (✅ Completada)

#### Situación Corregida

Se han movido todos los componentes a sus ubicaciones correctas:

- ✅ Excepciones comunes en `src/domain/shared/exceptions.py`
- ✅ Validadores comunes en `src/domain/shared/validators/common.py`
- ✅ Mappers base en `src/infrastructure/mappers.py`
- ✅ Interfaz base genérica para repositorios en `src/infrastructure/interfaces/repositories.py`
- ✅ Utilidades de fecha y hora en `src/infrastructure/utils/datetime.py`
- ✅ Utilidades de validación en `src/infrastructure/utils/validation.py`

### Fase 3: Actualización de Referencias (✅ Completada)

- ✅ Actualizar importaciones en todas las características para usar los nuevos componentes compartidos
- ✅ Ejecutar pruebas después de cada actualización para asegurar la compatibilidad

### Fase 4: Limpieza (✅ Completada)

- ✅ Eliminar archivos obsoletos
- ✅ Eliminar código duplicado (funciones `get_utc_now()`)
- ✅ Eliminar la carpeta `src/features/shared` y todos sus subdirectorios

### Fase 5: Mejoras Adicionales (⏳ En Progreso)

- ✅ Migración de bcrypt a Argon2 para el sistema de contraseñas
- ✅ Implementar mecanismo para actualizar automáticamente los hashes bcrypt a Argon2 cuando los usuarios inicien sesión
- ⏳ Considerar la implementación de un script para migrar masivamente las contraseñas existentes
- ⏳ Eliminar completamente el soporte a bcrypt después de un período de transición
- ⏳ Implementar pruebas automatizadas para verificar la correcta arquitectura del proyecto

## Consideraciones Importantes

- **Configuración centralizada**: Se ha centralizado la configuración de variables de entorno en un único archivo `.env` en la raíz del proyecto para mejorar la coherencia y mantenibilidad.
- **Mantenimiento continuo**: Seguir estos principios en el desarrollo futuro para evitar regresar a patrones de código duplicado.
- **Documentación actualizada**: Mantener la documentación actualizada a medida que evoluciona el proyecto.

## Próximos Pasos

1. **Pruebas exhaustivas**: Ejecutar pruebas completas para asegurar que la migración no ha introducido problemas.
2. **Documentación de API**: Actualizar la documentación de la API para reflejar la nueva estructura.
3. **Capacitación del equipo**: Asegurar que todo el equipo comprende la nueva arquitectura y los patrones de diseño utilizados.
