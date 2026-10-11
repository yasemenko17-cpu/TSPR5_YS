"""Відкриті тести задачі 1: Від метрик до інсайту: сегмент із найбільшим відхиленням.

Запуск: pytest tests/test_variant_01.py
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

FUNC = "top_deviation"
CASES = [
    ('T01-S1-1', ([{'segment': 'Мобільний застосунок', 'users': 1200, 'converted': 300},
  {'segment': 'Сайт', 'users': 800, 'converted': 240},
  {'segment': 'Партнерський QR', 'users': 100, 'converted': 5},
  {'segment': 'Корпоративні клієнти', 'users': 400, 'converted': 160}],
 200), {'baseline': 28.2,
 'segment': 'Корпоративні клієнти',
 'rate': 40.0,
 'delta_pp': 11.8,
 'direction': 'вище',
 'excluded': ['Партнерський QR']}),
    ('T01-S1-2', ([{'segment': 'Мобільний застосунок', 'users': 1200, 'converted': 300},
  {'segment': 'Сайт', 'users': 800, 'converted': 240},
  {'segment': 'Партнерський QR', 'users': 100, 'converted': 5},
  {'segment': 'Корпоративні клієнти', 'users': 400, 'converted': 160}],
 50), {'baseline': 28.2,
 'segment': 'Партнерський QR',
 'rate': 5.0,
 'delta_pp': -23.2,
 'direction': 'нижче',
 'excluded': []}),
    ('T01-S2-1', ([{'segment': 'Перша підписка', 'users': 900, 'converted': 108},
  {'segment': 'Повторна підписка', 'users': 600, 'converted': 270},
  {'segment': 'Подарункова', 'users': 150, 'converted': 21},
  {'segment': 'Промокод', 'users': 450, 'converted': 90}],
 200), {'baseline': 23.3,
 'segment': 'Повторна підписка',
 'rate': 45.0,
 'delta_pp': 21.7,
 'direction': 'вище',
 'excluded': ['Подарункова']}),
    ('T01-S2-2', ([{'segment': 'Перша підписка', 'users': 900, 'converted': 108},
  {'segment': 'Повторна підписка', 'users': 600, 'converted': 270},
  {'segment': 'Подарункова', 'users': 150, 'converted': 21},
  {'segment': 'Промокод', 'users': 450, 'converted': 90}],
 300), {'baseline': 23.3,
 'segment': 'Повторна підписка',
 'rate': 45.0,
 'delta_pp': 21.7,
 'direction': 'вище',
 'excluded': ['Подарункова']}),
    ('T01-S3-1', ([{'segment': 'Безкоштовні модулі', 'users': 2000, 'converted': 640},
  {'segment': 'Платні модулі', 'users': 700, 'converted': 357},
  {'segment': 'Корпоративні групи', 'users': 300, 'converted': 183},
  {'segment': 'Пробний тиждень', 'users': 80, 'converted': 16}],
 100), {'baseline': 38.8,
 'segment': 'Корпоративні групи',
 'rate': 61.0,
 'delta_pp': 22.2,
 'direction': 'вище',
 'excluded': ['Пробний тиждень']}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_01(args, expected):
    check(1, FUNC, args, expected)
