from pathlib import Path

import pandas as pd
from exceptions import EleccionesError
from myconfig import DATA_FOLDER, engine
from parser.parser_utils import parse_file_parameters
from utils.zip_processor import FileFunction, ZipFileProcessor


def _zips_to_postgres(listado: list[dict]):
    for item in listado:
        filepath: Path = DATA_FOLDER / item["nombreDoc"]
        if not filepath.exists():
            raise EleccionesError
        zip_to_postgres(filepath)


def zip_to_postgres(dataset_path):
    # print(dataset_path)
    processor = ZipFileProcessor(dataset_path)
    processor.add_function(FileFunction(is_dat_file, dat_file_to_postgres))
    processor.process()


def is_dat_file(filename):
    if not Path(filename).suffix.lower().endswith(".dat"):
        return False
    # TODO(fpuga): El código no está preparado para todos los ficheros
    # Chequear que la cantidad y nombre de los ficheros es correcto
    # Comprobar que está FICHEROS.{rtf,doc}

    return int(filename[:2]) <= 4  # noqa: PLR2004


def dat_file_to_postgres(filepath, _):
    widths, names, tablename = parse_file_parameters(filepath)
    # print(filepath)
    datfile = parse_dat_file(filepath, {"widths": widths, "names": names})
    datfile.to_sql(tablename, engine, schema="raw", if_exists="append", index=False)


def parse_dat_file(filepath, config):
    return pd.read_fwf(
        filepath, widths=config["widths"], names=config["names"], encoding="iso8859-1"
    )
