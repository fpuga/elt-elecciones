from pathlib import Path

from myconfig import DATA_FOLDER
from scrapper.requests_utils import authorized_session, download_file_copy


def _descargar_zips(listado: list[dict]):
    for item in listado:
        filepath: Path = DATA_FOLDER / item["nombreDoc"]
        if filepath.exists():
            # TODO(fpuga): Se podría en descargar igual, y hacer un checksum para ver
            # si hay cambios
            continue
        download_file_copy(
            url=item["url"],
            path=str(DATA_FOLDER.resolve()),
            request_or_session=authorized_session(),
        )
