"""Відкриті тести задачі 6: Кролячі нори й межі пітчу.

Запуск: pytest tests/test_variant_06.py
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

FUNC = "check_rabbit_holes"
CASES = [
    ('T06-S1-1', ({'appetite': 2,
  'elements': [{'name': 'План залу', 'unknown': False},
               {'name': 'Вибір місця', 'unknown': False},
               {'name': 'Оплата карткою', 'unknown': True}],
  'rabbit_holes': [{'element': 'Оплата карткою', 'resolution': 'беремо готовий платіжний віджет'}],
  'no_gos': ['Оплата частинами']},), {'verdict': 'готовий до столу ставок', 'issues': [], 'open_unknowns': []}),
    ('T06-S1-2', ({'appetite': 2,
  'elements': [{'name': 'План залу', 'unknown': False},
               {'name': 'Вибір місця', 'unknown': False},
               {'name': 'Оплата карткою', 'unknown': True}],
  'rabbit_holes': [],
  'no_gos': ['Оплата частинами']},), {'verdict': 'доопрацювати',
 'issues': ['«Оплата карткою»: невідоме без закритої нори'],
 'open_unknowns': ['Оплата карткою']}),
    ('T06-S2-1', ({'appetite': 6,
  'elements': [{'name': 'Картка набору', 'unknown': False},
               {'name': 'Підписка', 'unknown': True},
               {'name': 'Платіж', 'unknown': True},
               {'name': 'Склад', 'unknown': True}],
  'rabbit_holes': [{'element': 'Підписка', 'resolution': 'лише тижневий цикл'},
                   {'element': 'Платіж', 'resolution': 'беремо готовий шлюз'},
                   {'element': 'Склад', 'resolution': 'ручне підтвердження'}],
  'no_gos': ['Знижки', 'Подарунки']},), {'verdict': 'готовий до столу ставок', 'issues': [], 'open_unknowns': []}),
    ('T06-S2-2', ({'appetite': 6,
  'elements': [{'name': 'A', 'unknown': True},
               {'name': 'B', 'unknown': True},
               {'name': 'C', 'unknown': True},
               {'name': 'D', 'unknown': True}],
  'rabbit_holes': [{'element': 'A', 'resolution': 'готове рішення'},
                   {'element': 'B', 'resolution': 'готове рішення'},
                   {'element': 'C', 'resolution': 'готове рішення'},
                   {'element': 'D', 'resolution': 'готове рішення'}],
  'no_gos': ['X']},), {'verdict': 'доопрацювати',
 'issues': ['Забагато невідомого: 4 замість допустимих 3 для апетиту 6 тижн.'],
 'open_unknowns': []}),
    ('T06-S3-1', ({'appetite': 2,
  'elements': [{'name': 'Короткі уроки', 'unknown': False}, {'name': 'Тест після модуля', 'unknown': True}],
  'rabbit_holes': [{'element': 'Тест після модуля', 'resolution': 'лише тест із вибором відповіді'}],
  'no_gos': ['Відеоредактор']},), {'verdict': 'готовий до столу ставок', 'issues': [], 'open_unknowns': []}),
    ('T06-S3-2', ({'appetite': 1,
  'elements': [{'name': 'Нагадування', 'unknown': True}, {'name': 'Сегментація', 'unknown': True}],
  'rabbit_holes': [{'element': 'Нагадування', 'resolution': 'лише email'},
                   {'element': 'Сегментація', 'resolution': 'один сегмент'}],
  'no_gos': ['SMS']},), {'verdict': 'доопрацювати',
 'issues': ['Забагато невідомого: 2 замість допустимих 1 для апетиту 1 тижн.'],
 'open_unknowns': []}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_06(args, expected):
    check(6, FUNC, args, expected)
