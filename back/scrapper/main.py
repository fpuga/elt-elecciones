from scrapper.infoelectoral_utils import (
    Agg,
    Convocatoria,
    criteria_filter,
    extract_listado_zips_por_convocatoria,
    run_checks,
)
from utils.dict_utils import flat_nested_recursively


def _extract():
    response = extract_listado_zips_por_convocatoria(Convocatoria())
    flat_response = [flat_nested_recursively(r, sep="_") for r in response]
    run_checks(flat_response)
    # TODO(fpuga): Filtramos por Congreso (2) para simplificar el proceso.
    criteria = Convocatoria(agg=Agg.MESA, tipo="2")
    return criteria_filter(flat_response, criteria)
