"""Перевірка артефакту частини Б: pytest check -q (змінна DIBB задає інший файл)."""
import os
from pathlib import Path

import pytest
import dibb_rules as dr

PATH = Path(os.environ.get("DIBB", dr.ROOT / "dibb" / "my_dibb.json"))


@pytest.fixture(scope="module")
def artifact():
    data = dr.load_artifact(PATH)
    assert isinstance(data, dict), "артефакт має бути JSON-об'єктом"
    return data


@pytest.mark.parametrize("rule", dr.RULES, ids=lambda r: r.__name__)
def test_rule(artifact, rule):
    problems = rule(artifact)
    assert not problems, "; ".join(problems)
