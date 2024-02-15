from dataclasses import dataclass
from enum import Enum

import requests
from exceptions import EleccionesError
from scrapper.requests_utils import authorized_session


Agg = Enum("Agg", ["MESA", "MUNI", "TOTA"])


class Tipo(Enum):
    Referendum = 1  # "Referéndum"
    Congreso = 2
    Senado = 3
    Municipales = 4
    Cabildos = 5
    Parlamento_Europeo = 6  # "Parlamento Europeo"


@dataclass(frozen=True, kw_only=True)
class Convocatoria(object):
    tipo: str | None = None
    id_: str | None = None
    agg: Agg | None = None

    @property
    def params(self) -> dict | None:
        """Returns a dict suitable for use as `params` parameter in requests library.

        If there are not params it returns None
        """
        params = {}
        if self.tipo:
            params.update(tipoConvocatoria=self.tipo)
        if self.id_:
            params.update(idConvocatoria=self.id_)
        return params or None


def _response_data(response: requests.Response) -> list[dict]:
    response.raise_for_status()
    if response.json()["cod"] != "200":
        raise EleccionesError
    return response.json()["data"]


def extract_tipos_convocatoria() -> list[dict]:
    url = "https://infoelectoral.interior.gob.es/min/convocatorias/tipos/"
    response = authorized_session().get(url, timeout=5)
    return _response_data(response)


def extract_listado_convocatorias_por_tipo(convocatoria: Convocatoria):
    url = "https://infoelectoral.interior.gob.es/min/convocatorias"
    response = authorized_session().get(url, params=convocatoria.params)
    return _response_data(response)


def run_checks(_: list[dict]) -> None:
    """Raises an error if a check does not pass."""


def criteria_filter(data: list[dict], criteria: Convocatoria) -> list[dict]:
    result = []
    for d in data:
        if criteria.agg and not d["nombreDoc"].endswith(f"_{criteria.agg.name}.zip"):
            continue
        if criteria.id_ and d["convocatoria_cod"] != criteria.id_:
            continue
        if criteria.tipo and str(d["convocatoria_tipoConvocatoria"]) != str(
            criteria.tipo
        ):
            continue
        result.append(d)
    return result


def extract_listado_zips_por_convocatoria(convocatoria: Convocatoria):
    """Devuelve una estructura de datos con las url de los zips y otros metadatos.

    Si `convocatoria` está en blanco devuelve los datos de todas las convocatorias.

    Ejemplo de respuesta:

    ```json
    [
        {
            "convocatoria": {
                "cod": "201512", "fecha": "201512",  "descripcion": "Diciembre 2015",
                "tipoConvocatoria": 2, "ambitoTerritorio": "Nacional"
            },
            "url": "https://infoelectoral.interior.gob.es/estaticos/docxl/apliextr/02201512_MESA.zip",
            "nombreDoc": "02201512_MESA.zip",
            "descripcion": "20 de Diciembre de 2015 (Mesa)"
        },
        {
            "convocatoria": {
                "cod": "201512", "fecha": "201512",  "descripcion": "Diciembre 2015",
                "tipoConvocatoria": 2, "ambitoTerritorio": "Nacional"
            },
            "url": "https://infoelectoral.interior.gob.es/estaticos/docxl/apliextr/02201512_MUNI.zip",
            "nombreDoc": "02201512_MUNI.zip",
            "descripcion": "20 de Diciembre de 2015 (Municipio)"
        },
    ...
    ]
    ```
    """
    url = "https://infoelectoral.interior.gob.es/min/archivos/extraccion"
    response = authorized_session().get(url, params=convocatoria.params)
    return _response_data(response)
    # convocatoria_cod == convocatoria_fecha
    # convocatoria_cod in nombreDoc
    # url == base + tipo + cod + mesa .zip
    # mesa in descripcion
    # str fecha  in convocatoria_descripcion
    # str fecha in descripcion
