"""Відкриті тести задачі 7: Ранжування пітчів для столу ставок.

Запуск: pytest tests/test_variant_07.py
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

FUNC = "rank_pitches"
CASES = [
    ('T07-S1-1', ([{'code': 'A', 'payout': 9, 'appetite': 6, 'ready': True, 'needs': None},
  {'code': 'B', 'payout': 4, 'appetite': 1, 'ready': True, 'needs': None},
  {'code': 'C', 'payout': 8, 'appetite': 6, 'ready': True, 'needs': None},
  {'code': 'D', 'payout': 5, 'appetite': 2, 'ready': True, 'needs': None},
  {'code': 'E', 'payout': 3, 'appetite': 2, 'ready': True, 'needs': 'A'},
  {'code': 'F', 'payout': 3, 'appetite': 1, 'ready': True, 'needs': None},
  {'code': 'G', 'payout': 4, 'appetite': 2, 'ready': True, 'needs': 'B'},
  {'code': 'H', 'payout': 6, 'appetite': 2, 'ready': False, 'needs': None}],
 12), {'rank': ['B', 'F', 'D', 'G', 'A', 'E', 'C'],
 'bets': ['B', 'F', 'D', 'G', 'A'],
 'deferred': [{'code': 'E', 'reason': 'не вистачає місткості'},
              {'code': 'C', 'reason': 'не вистачає місткості'}],
 'reshape': ['H'],
 'used': 12,
 'left': 0}),
    ('T07-S2-1', ([{'code': 'К1', 'payout': 8, 'appetite': 2, 'ready': True, 'needs': None},
  {'code': 'К2', 'payout': 6, 'appetite': 1, 'ready': True, 'needs': None},
  {'code': 'К3', 'payout': 9, 'appetite': 6, 'ready': True, 'needs': None},
  {'code': 'К4', 'payout': 3, 'appetite': 1, 'ready': False, 'needs': None},
  {'code': 'К5', 'payout': 5, 'appetite': 2, 'ready': True, 'needs': 'К2'},
  {'code': 'К6', 'payout': 4, 'appetite': 1, 'ready': True, 'needs': None},
  {'code': 'К7', 'payout': 7, 'appetite': 6, 'ready': True, 'needs': 'К3'},
  {'code': 'К8', 'payout': 4, 'appetite': 2, 'ready': True, 'needs': None}],
 12), {'rank': ['К2', 'К1', 'К6', 'К5', 'К8', 'К3', 'К7'],
 'bets': ['К2', 'К1', 'К6', 'К5', 'К8'],
 'deferred': [{'code': 'К3', 'reason': 'не вистачає місткості'},
              {'code': 'К7', 'reason': 'залежність К3 не вибрана'}],
 'reshape': ['К4'],
 'used': 8,
 'left': 4}),
    ('T07-S3-3', ([{'code': 'x', 'payout': 4, 'appetite': 2, 'ready': True, 'needs': None},
  {'code': 'y', 'payout': 4, 'appetite': 2, 'ready': True, 'needs': None},
  {'code': 'z', 'payout': 4, 'appetite': 2, 'ready': True, 'needs': None}],
 4), {'rank': ['x', 'y', 'z'],
 'bets': ['x', 'y'],
 'deferred': [{'code': 'z', 'reason': 'не вистачає місткості'}],
 'reshape': [],
 'used': 4,
 'left': 0}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_07(args, expected):
    check(7, FUNC, args, expected)
