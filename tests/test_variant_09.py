"""Відкриті тести задачі 9: Підсумок циклу.

Запуск: pytest tests/test_variant_09.py
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

FUNC = "cycle_summary"
CASES = [
    ('T09-S1-1', ([{'title': 'План залу', 'appetite': 6, 'outcome': 'випущено', 'weeks_spent': 6},
  {'title': 'Нагадування', 'appetite': 2, 'outcome': 'випущено', 'weeks_spent': 1}],
 12,
 2), {'bets': 2,
 'shipped': 2,
 'cut_scope': 0,
 'breaker': [],
 'hit_rate_pct': 100.0,
 'planned': 8,
 'spent': 7,
 'unused': 5,
 'verdict': 'цикл вдалий',
 'next': {'reshape': [], 'cooldown': 2}}),
    ('T09-S1-2', ([{'title': 'План залу', 'appetite': 6, 'outcome': 'випущено з урізанням', 'weeks_spent': 6},
  {'title': 'Оплата', 'appetite': 6, 'outcome': 'запобіжник', 'weeks_spent': 6},
  {'title': 'Нагадування', 'appetite': 2, 'outcome': 'випущено', 'weeks_spent': 2}],
 14,
 2), {'bets': 3,
 'shipped': 2,
 'cut_scope': 1,
 'breaker': ['Оплата'],
 'hit_rate_pct': 66.7,
 'planned': 14,
 'spent': 14,
 'unused': 0,
 'verdict': 'цикл змішаний',
 'next': {'reshape': ['Оплата'], 'cooldown': 2}}),
    ('T09-S2-1', ([{'title': 'Підписка', 'appetite': 6, 'outcome': 'випущено', 'weeks_spent': 6},
  {'title': 'Пауза', 'appetite': 2, 'outcome': 'запобіжник', 'weeks_spent': 2},
  {'title': 'Промокод', 'appetite': 1, 'outcome': 'випущено', 'weeks_spent': 1}],
 12,
 2), {'bets': 3,
 'shipped': 2,
 'cut_scope': 0,
 'breaker': ['Пауза'],
 'hit_rate_pct': 66.7,
 'planned': 9,
 'spent': 9,
 'unused': 3,
 'verdict': 'цикл змішаний',
 'next': {'reshape': ['Пауза'], 'cooldown': 2}}),
    ('T09-S3-1', ([{'title': 'Короткі уроки', 'appetite': 6, 'outcome': 'випущено', 'weeks_spent': 6}], 6, 2), {'bets': 1,
 'shipped': 1,
 'cut_scope': 0,
 'breaker': [],
 'hit_rate_pct': 100.0,
 'planned': 6,
 'spent': 6,
 'unused': 0,
 'verdict': 'цикл вдалий',
 'next': {'reshape': [], 'cooldown': 2}}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_09(args, expected):
    check(9, FUNC, args, expected)
