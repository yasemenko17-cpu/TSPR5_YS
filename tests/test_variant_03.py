"""Відкриті тести задачі 3: Узгодженість ланцюжка DIBB.

Запуск: pytest tests/test_variant_03.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


def check(number, func, args, expected):
    call = getattr(load(number), func)
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            call(*args)
        assert str(info.value) == str(expected)
    else:
        result = call(*args)
        assert norm(result) == norm(expected)
        assert type(result) is type(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"

FUNC = "check_dibb"
CASES = [
    ('T03-S1-1', ({'data': [{'id': 'D1'}, {'id': 'D2'}, {'id': 'D3'}],
  'insights': [{'id': 'I1', 'data': ['D1', 'D2']}, {'id': 'I2', 'data': ['D3']}],
  'beliefs': [{'id': 'B1', 'insights': ['I1']}, {'id': 'B2', 'insights': ['I2']}],
  'bets': [{'id': 'T1', 'beliefs': ['B1']}, {'id': 'T2', 'beliefs': ['B2']}]},), {'ok': True, 'problems': [], 'traceable_bets': ['T1', 'T2']}),
    ('T03-S1-2', ({'data': [{'id': 'D1'}],
  'insights': [{'id': 'I1', 'data': ['D1']}, {'id': 'I2', 'data': ['D9']}],
  'beliefs': [{'id': 'B1', 'insights': ['I1', 'I2']}],
  'bets': [{'id': 'T1', 'beliefs': ['B1']}]},), {'ok': False, 'problems': ['I2: невідоме посилання D9'], 'traceable_bets': []}),
    ('T03-S2-1', ({'data': [{'id': 'D1'}, {'id': 'D2'}],
  'insights': [{'id': 'I1', 'data': ['D1', 'D2']}],
  'beliefs': [{'id': 'B1', 'insights': ['D1']}],
  'bets': [{'id': 'T1', 'beliefs': ['B1']}]},), {'ok': False, 'problems': ['B1: невідоме посилання D1', 'I1: інсайт без переконання'], 'traceable_bets': []}),
    ('T03-S2-2', ({'data': [{'id': 'D1'}, {'id': 'D2'}],
  'insights': [{'id': 'I1', 'data': ['D1']}, {'id': 'I2', 'data': ['D2']}],
  'beliefs': [{'id': 'B1', 'insights': ['I1']}, {'id': 'B2', 'insights': ['I2']}],
  'bets': [{'id': 'T1', 'beliefs': ['B1', 'B2']}]},), {'ok': True, 'problems': [], 'traceable_bets': ['T1']}),
    ('T03-S3-1', ({'data': [{'id': 'D1'}, {'id': 'D2'}, {'id': 'D3'}, {'id': 'D4'}],
  'insights': [{'id': 'I1', 'data': ['D1']},
               {'id': 'I2', 'data': ['D2', 'D3']},
               {'id': 'I3', 'data': ['D4']}],
  'beliefs': [{'id': 'B1', 'insights': ['I1']},
              {'id': 'B2', 'insights': ['I2']},
              {'id': 'B3', 'insights': ['I3']}],
  'bets': [{'id': 'T1', 'beliefs': ['B1']},
           {'id': 'T2', 'beliefs': ['B2']},
           {'id': 'T3', 'beliefs': ['B3']}]},), {'ok': True, 'problems': [], 'traceable_bets': ['T1', 'T2', 'T3']}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_03(args, expected):
    check(3, FUNC, args, expected)
