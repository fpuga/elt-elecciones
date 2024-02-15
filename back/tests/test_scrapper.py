import json
from pathlib import Path

import deepdiff
from scrapper.main import _extract


def test_extract():
    filepath = Path(__file__).resolve().parent / "golden" / "listado_mesa_congreso.json"
    expected = json.load(filepath.open())
    actual = _extract()
    diff = deepdiff.DeepDiff(expected, actual, ignore_order=True)

    assert not diff, json.dumps(diff, indent=4)
