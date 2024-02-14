# ELT de Resultados Electorales con stack Python

Este repositorio es el código de ejemplo para una charla sobre construir un ELT con stack Python, usando como ejemplo, el montar una base de datos a partir de los datos oficiales de resultados electorales de España.

No debe tomarse el código como normativo o un ejemplo de buenas prácticas. Está hecho para que sea fácil de seguir a lo largo de la charla.

# Presentación

```
cd talk
python3 -m http.server 8000
xdg-open http://localhost:8000
```

# Instalación

El script de instalación crea un entorno virtual con virtualenwrapper, e instala python 3.11.3 con pyenv.

## Pre-requisitos

-   docker
-   virtualenwrapper
-   pyenv

## Instalar

```
./scripts/install.sh
```

# Ejecutar

```
docker compose up -d
python -m back.main
```

También se puede jugar con los Jupyter de la carpeta `notebooks`.

# Desarrollo

Hace falta tener instalado `shfmt` y `shellcheck` o hacer los commits con `--no-verify`.

Contribuciones, estrellas e issues son gratamente aceptadas.

# License

The documentation of this project is licensed under the [CC-BY-SA-4.0](https://choosealicense.com/licenses/cc-by-sa-4.0/).

The underlying source code is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/).

Media could have their own trademarks and licenses.
