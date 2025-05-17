# Tests para API Seguros

Este directorio contiene las pruebas automatizadas para la aplicacion API Seguros, siguiendo los principios de Clean Architecture y Vertical Slicing.

## Estructura

La estructura de los tests refleja la estructura de la aplicacion:

```
tests/
  domain/
    shared/              # Pruebas para componentes compartidos del dominio
      test_exceptions.py # Pruebas para el sistema de manejo de excepciones
  features/
    monedas/            # Pruebas para la feature de monedas
      application/
        test_use_cases.py
      domain/
      infrastructure/
        test_mappers.py
        test_repositories.py
    # Otras features seguiran la misma estructura
  conftest.py           # Configuraciones y fixtures compartidos para pytest
```

## Ejecucion de las pruebas

Para ejecutar todas las pruebas:

```bash
pytest
```

Para ejecutar pruebas de un modulo especifico:

```bash
pytest tests/features/monedas/
```

Para ejecutar pruebas con informacion detallada:

```bash
pytest -v
```

Para generar un informe de cobertura:

```bash
pytest --cov=src tests/
```

## Requisitos

Para ejecutar las pruebas, necesitas instalar las siguientes dependencias:

```bash
pip install pytest pytest-cov fastapi httpx
```

## Convenciones

1. Los nombres de las clases de prueba deben comenzar con `Test`
2. Los nombres de los metodos de prueba deben comenzar con `test_`
3. Cada prueba debe tener un docstring que explique que se esta probando
4. Usar fixtures para compartir configuraciones comunes
5. Usar mocks para aislar las pruebas de dependencias externas
