import os
import shutil
from functools import lru_cache

import requests


def download_file_copy(url, path=".", request_or_session=None, user_filename=None):
    connection = request_or_session or requests
    url_filename = url.split("/")[-1]
    filename = os.path.join(path, user_filename or url_filename)
    with connection.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return filename


@lru_cache
def authorized_session():
    """Creates a request session with basic auth.

    La web del ministerio usa basic auth para las llamadas a la API. Seguramente para
    complicar el _scrapping_. El usuario y password están hardcodeados en algunas
    funciones JS cómo: `loadConvocatoriasDescargas`
    """
    s = requests.Session()
    s.auth = ("apiInfoelectoral", "apiInfoelectoralPro")
    return s
