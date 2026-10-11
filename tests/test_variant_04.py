"""Відкриті тести задачі 4: Критерій успіху ставки й мінімальний ефект.

Запуск: pytest tests/test_variant_04.py
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

FUNC = "success_criterion"
CASES = [
    ('T04-S1-1', ({'baseline': 28,
  'target': 33,
  'users_per_month': 5000,
  'value_per_conversion': 150,
  'weekly_cost': 30000,
  'appetite': 2,
  'horizon_months': 6},), {'cost': 60000,
 'extra_conversions': 400,
 'min_effect_pp': 1.5,
 'planned_effect_pp': 5,
 'verdict': 'окупається'}),
    ('T04-S1-2', ({'baseline': 28,
  'target': 30,
  'users_per_month': 5000,
  'value_per_conversion': 150,
  'weekly_cost': 30000,
  'appetite': 2,
  'horizon_months': 6},), {'cost': 60000,
 'extra_conversions': 400,
 'min_effect_pp': 1.5,
 'planned_effect_pp': 2,
 'verdict': 'окупається на межі'}),
    ('T04-S2-1', ({'baseline': 12,
  'target': 15,
  'users_per_month': 8000,
  'value_per_conversion': 90,
  'weekly_cost': 20000,
  'appetite': 1,
  'horizon_months': 3},), {'cost': 20000,
 'extra_conversions': 223,
 'min_effect_pp': 1.0,
 'planned_effect_pp': 3,
 'verdict': 'окупається'}),
    ('T04-S2-2', ({'baseline': 12,
  'target': 16,
  'users_per_month': 8000,
  'value_per_conversion': 90,
  'weekly_cost': 20000,
  'appetite': 6,
  'horizon_months': 4},), {'cost': 120000,
 'extra_conversions': 1334,
 'min_effect_pp': 4.5,
 'planned_effect_pp': 4,
 'verdict': 'не окупається'}),
    ('T04-S3-1', ({'baseline': 41,
  'target': 48,
  'users_per_month': 12000,
  'value_per_conversion': 60,
  'weekly_cost': 25000,
  'appetite': 6,
  'horizon_months': 6},), {'cost': 150000,
 'extra_conversions': 2500,
 'min_effect_pp': 3.5,
 'planned_effect_pp': 7,
 'verdict': 'окупається'}),
    ('T04-S3-2', ({'baseline': 41,
  'target': 42,
  'users_per_month': 12000,
  'value_per_conversion': 60,
  'weekly_cost': 25000,
  'appetite': 6,
  'horizon_months': 6},), {'cost': 150000,
 'extra_conversions': 2500,
 'min_effect_pp': 3.5,
 'planned_effect_pp': 1,
 'verdict': 'не окупається'}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_04(args, expected):
    check(4, FUNC, args, expected)
