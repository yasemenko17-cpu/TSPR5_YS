"""Відкриті тести задачі 10: Ставка проти результату.

Запуск: pytest tests/test_variant_10.py
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

FUNC = "compare_results"
CASES = [
    ('T10-S1-1', ([{'title': 'Бронювання в два дотики', 'baseline': 28, 'target': 33, 'actual': 34.0, 'min_effect': 2},
  {'title': 'Карта залу', 'baseline': 28, 'target': 31, 'actual': 29.5, 'min_effect': 1},
  {'title': 'Нагадування', 'baseline': 28, 'target': 30, 'actual': 27.5, 'min_effect': 1}],), {'rows': [{'title': 'Бронювання в два дотики',
           'effect_pp': 6.0,
           'gap_pp': 1.0,
           'verdict': 'ціль досягнута',
           'belief': 'підтверджено'},
          {'title': 'Карта залу',
           'effect_pp': 1.5,
           'gap_pp': -1.5,
           'verdict': 'частково',
           'belief': 'підтверджено частково'},
          {'title': 'Нагадування',
           'effect_pp': -0.5,
           'gap_pp': -2.5,
           'verdict': 'шкодить',
           'belief': 'спростовано'}],
 'counts': {'ціль досягнута': 1, 'частково': 1, 'не підтверджено': 0, 'шкодить': 1},
 'mean_abs_gap': 1.7,
 'largest_miss': 'Нагадування'}),
    ('T10-S1-2', ([{'title': 'A', 'baseline': 28, 'target': 33, 'actual': 28.5, 'min_effect': 2}],), {'rows': [{'title': 'A',
           'effect_pp': 0.5,
           'gap_pp': -4.5,
           'verdict': 'не підтверджено',
           'belief': 'не підтверджено'}],
 'counts': {'ціль досягнута': 0, 'частково': 0, 'не підтверджено': 1, 'шкодить': 0},
 'mean_abs_gap': 4.5,
 'largest_miss': 'A'}),
    ('T10-S2-1', ([{'title': 'Ціна на картці', 'baseline': 12, 'target': 15, 'actual': 15.4, 'min_effect': 1.5},
  {'title': 'Пауза', 'baseline': 12, 'target': 14, 'actual': 12.2, 'min_effect': 1}],), {'rows': [{'title': 'Ціна на картці',
           'effect_pp': 3.4,
           'gap_pp': 0.4,
           'verdict': 'ціль досягнута',
           'belief': 'підтверджено'},
          {'title': 'Пауза',
           'effect_pp': 0.2,
           'gap_pp': -1.8,
           'verdict': 'не підтверджено',
           'belief': 'не підтверджено'}],
 'counts': {'ціль досягнута': 1, 'частково': 0, 'не підтверджено': 1, 'шкодить': 0},
 'mean_abs_gap': 1.1,
 'largest_miss': 'Пауза'}),
    ('T10-S3-1', ([{'title': 'Короткі уроки', 'baseline': 41, 'target': 48, 'actual': 51.0, 'min_effect': 3}],), {'rows': [{'title': 'Короткі уроки',
           'effect_pp': 10.0,
           'gap_pp': 3.0,
           'verdict': 'ціль досягнута',
           'belief': 'підтверджено'}],
 'counts': {'ціль досягнута': 1, 'частково': 0, 'не підтверджено': 0, 'шкодить': 0},
 'mean_abs_gap': 3.0,
 'largest_miss': 'Короткі уроки'}),
    ('T10-S3-2', ([{'title': 'Нагадування', 'baseline': 41, 'target': 44, 'actual': 40.0, 'min_effect': 1}],), {'rows': [{'title': 'Нагадування',
           'effect_pp': -1.0,
           'gap_pp': -4.0,
           'verdict': 'шкодить',
           'belief': 'спростовано'}],
 'counts': {'ціль досягнута': 0, 'частково': 0, 'не підтверджено': 0, 'шкодить': 1},
 'mean_abs_gap': 4.0,
 'largest_miss': 'Нагадування'}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_10(args, expected):
    check(10, FUNC, args, expected)
