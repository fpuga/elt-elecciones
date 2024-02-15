import base64
import json
from collections import Counter, OrderedDict
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dagster import AssetExecutionContext, MaterializeResult, MetadataValue, asset
from myconfig import DATA_FOLDER, engine
from parser.main import _zips_to_postgres
from scrapper.main import _extract
from scrapper.requests_utils import authorized_session, download_file_copy


@asset(group_name="elecciones", compute_kind="InfoElectoral API")
def obtener_listado(context: AssetExecutionContext) -> MaterializeResult:
    """Persiste a disco un json con metadatos sobre las convocatorias electorales.

    * Código, fecha, descripción, ... de la convocatoria.
    * Nombre del fichero (.zip) con los datos y url al zip.

    **AVISOS**:

    * Sólo se está almacenando un registro por convocatoria con los resultados
    agregados a nivel de MESA.
    * Sólo se están almacenando las convocatorias al Congreso.
    """
    result = _extract()
    context.log.info("Datos recuperados")
    with (DATA_FOLDER / "listado.json").open("w") as f:
        json.dump(result, f)
    return MaterializeResult(
        metadata={
            "num_records": len(result),  # Metadata can be any key-value pair
            "preview": MetadataValue.json(result[:3]),
            # The `MetadataValue` class has useful static methods to build Metadata
        }
    )


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
def descargar_zips(context: AssetExecutionContext):
    """Descarga los .zip con datos a partir del fichero con el listado de metadatos."""
    with (DATA_FOLDER / "listado.json").open() as f:
        listado = json.load(f)
    for item in listado:
        filepath: Path = DATA_FOLDER / item["nombreDoc"]
        if filepath.exists():
            # TODO(fpuga): Se podría en descargar igual, y hacer un checksum para ver
            # si hay cambios
            context.log.info("%s, ya existe en disco", {item["nombreDoc"]})
            continue
        context.log.info("Descargando: %s", item["nombreDoc"])
        download_file_copy(
            url=item["url"],
            path=str(DATA_FOLDER.resolve()),
            request_or_session=authorized_session(),
        )


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


@asset(deps=[obtener_listado], group_name="elecciones", compute_kind="Plot")
def elecciones_por_anho(context: AssetExecutionContext) -> MaterializeResult:
    """Calcula cuantas elecciones ha habido al año."""
    with (DATA_FOLDER / "listado.json").open() as f:
        data = json.load(f)
    listado = pd.DataFrame.from_dict(data, orient="columns")

    context.log.debug("Calcular contador")
    counter = Counter(listado["convocatoria_fecha"].str[:4].to_list())
    ordered_counter = OrderedDict(
        sorted(counter.items(), key=lambda pair: pair[0], reverse=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(list(ordered_counter.keys()), list(ordered_counter.values()))
    plt.xticks(rotation=45, ha="right")
    plt.title("Nº de convocatorias por año")
    plt.tight_layout()

    # Convert the image to a saveable format
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_data = base64.b64encode(buffer.getvalue())

    # Convert the image to Markdown to preview it within Dagster
    md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    with (DATA_FOLDER / "elecciones_por_anho.json").open("w") as f:
        json.dump(ordered_counter, f)

    # Attach the Markdown content as metadata to the asset
    return MaterializeResult(metadata={"plot": MetadataValue.md(md_content)})
