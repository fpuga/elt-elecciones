import json

import pandas as pd
from dagster import asset
from downloader.main import _descargar_zips
from myconfig import DATA_FOLDER, engine
from parser.main import _zips_to_postgres
from scrapper.main import _extract


@asset(group_name="elecciones", compute_kind="InfoElectoral API")
def obtener_listado() -> None:
    """Persiste a disco un json con metadatos sobre las convocatorias electorales.

    * Código, fecha, descripción, ... de la convocatoria.
    * Nombre del fichero (.zip) con los datos y url al zip.

    **AVISOS**:

    * Sólo se está almacenando un registro por convocatoria con los resultados
    agregados a nivel de MESA.
    * Sólo se están almacenando las convocatorias al Congreso.

    Ejemplo de json:

    ```json
    [
        {
            "convocatoria_cod": "201512",
            "convocatoria_fecha": "201512",
            "convocatoria_descripcion": "Diciembre 2015",
            "convocatoria_tipoConvocatoria": 2,
            "convocatoria_ambitoTerritorio": "Nacional",
            "url": "https://infoelectoral.interior.gob.es/estaticos/docxl/apliextr/02201512_MESA.zip",
            "nombreDoc": "02201512_MESA.zip",
            "descripcion": "20 de Diciembre de 2015 (Mesa)"
        },
    ...
    ]
    ```
    """
    # 1 / 0
    result = _extract()
    with (DATA_FOLDER / "listado.json").open("w") as f:
        json.dump(result, f)


@asset(deps=[obtener_listado], group_name="elecciones", compute_kind="Load")
def listado_a_postgres():
    """Almacena en PostgreSQL el fichero con el listado de metadatos de convocatorias.

    Si la tabla ya existe la recrea. Los datos son almacenados en columnas, no cómo un
    tipo JSON.
    """
    with (DATA_FOLDER / "listado.json").open() as f:
        data = json.load(f)
    listado = pd.DataFrame.from_dict(data, orient="columns")
    listado.to_sql("listado", engine, schema="raw", if_exists="replace", index=False)


@asset(deps=[listado_a_postgres], group_name="elecciones", compute_kind="Extract")
def descargar_zips():
    """Descarga los .zip con datos a partir del fichero con el listado de metadatos."""
    with (DATA_FOLDER / "listado.json").open() as f:
        data = json.load(f)
    _descargar_zips(data)


@asset(deps=[descargar_zips], group_name="elecciones", compute_kind="Load")
def zips_to_postgres():
    """Descomprime los zips y parsea los ficheros .DAT para subirlos a PostgreSQL.

    Usa el fichero con el listado de metadatos para _descubrir_ que .zip leer.

    **AVISOS**:

    * No se están procesando todos los ficheros sólo: CONTROL, IDENTIFICACIÓN,
      CANDIDATURAS y CANDIDATOS.
    """
    with (DATA_FOLDER / "listado.json").open() as f:
        data = json.load(f)
    _zips_to_postgres(data)
