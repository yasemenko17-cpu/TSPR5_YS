import pytest
from conftest import load

M = load(8)

@pytest.mark.parametrize("args, expected", [
    (
        ([{"name": "Скоуп А", "must": True, "history": [100]}], 1, 1),
        {
            "week": 1,
            "scopes": [{"name": "Скоуп А", "phase": "готово", "position": 100, "projected": 100, "status": "готово"}],
            "must_done": "1 з 1",
            "decision": "випуск за графіком",
            "focus": []
        }
    ),
    (
        ([{"name": "Скоуп Б", "must": True, "history": [20, 40]}], 2, 4),
        {
            "week": 2,
            "scopes": [{"name": "Скоуп Б", "phase": "вгору", "position": 40, "projected": 80, "status": "під ризиком"}],
            "must_done": "0 з 1",
            "decision": "стежити за обов'язковим",
            "focus": ["Скоуп Б"]
        }
    )
])
def test_my_hill_cases(args, expected):
    assert M.hill_status(*args) == expected

def test_my_error_cases():
    with pytest.raises(ValueError, match="Немає скоупів"):
        M.hill_status([], 1, 1)
    with pytest.raises(ValueError, match="Тиждень поза циклом"):
        M.hill_status([{"name": "А", "must": True, "history": [50]}], 3, 2)