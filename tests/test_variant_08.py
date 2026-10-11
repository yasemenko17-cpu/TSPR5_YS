"""Відкриті тести задачі 8: Стан робіт на hill chart і запобіжник.

Запуск: pytest tests/test_variant_08.py
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

FUNC = "hill_status"
CASES = [
    ('T08-S1-2', ([{'name': 'План залу', 'must': True, 'history': [10, 30, 55, 75, 95, 100]},
  {'name': 'Оплата', 'must': True, 'history': [5, 20, 40, 60, 85, 100]},
  {'name': 'Нагадування', 'must': False, 'history': [0, 10, 25, 45, 60, 70]}],
 6,
 6), {'week': 6,
 'scopes': [{'name': 'План залу', 'phase': 'готово', 'position': 100, 'projected': 100, 'status': 'готово'},
            {'name': 'Оплата', 'phase': 'готово', 'position': 100, 'projected': 100, 'status': 'готово'},
            {'name': 'Нагадування',
             'phase': 'вниз',
             'position': 70,
             'projected': 70,
             'status': 'під ризиком'}],
 'must_done': '2 з 2',
 'decision': 'випуск за графіком з урізанням обсягу',
 'focus': ['Нагадування']}),
    ('T08-S2-1', ([{'name': 'Картка набору', 'must': True, 'history': [10, 35, 60, 85, 100, 100]},
  {'name': 'Підписка', 'must': True, 'history': [5, 15, 25, 30, 35, 40]},
  {'name': 'Пауза', 'must': False, 'history': [0, 0, 10, 20, 30, 45]}],
 6,
 6), {'week': 6,
 'scopes': [{'name': 'Картка набору',
             'phase': 'готово',
             'position': 100,
             'projected': 100,
             'status': 'готово'},
            {'name': 'Підписка', 'phase': 'вгору', 'position': 40, 'projected': 40, 'status': 'не встигає'},
            {'name': 'Пауза', 'phase': 'вгору', 'position': 45, 'projected': 45, 'status': 'не встигає'}],
 'must_done': '1 з 2',
 'decision': 'запобіжник спрацював: повернути пітч на шейпінг',
 'focus': ['Підписка']}),
    ('T08-S3-1', ([{'name': 'Короткі уроки', 'must': True, 'history': [20, 45, 70, 90, 100, 100]},
  {'name': 'Тест', 'must': True, 'history': [10, 30, 50, 70, 90, 100]},
  {'name': 'Значок', 'must': False, 'history': [0, 10, 30, 50, 80, 100]}],
 6,
 6), {'week': 6,
 'scopes': [{'name': 'Короткі уроки',
             'phase': 'готово',
             'position': 100,
             'projected': 100,
             'status': 'готово'},
            {'name': 'Тест', 'phase': 'готово', 'position': 100, 'projected': 100, 'status': 'готово'},
            {'name': 'Значок', 'phase': 'готово', 'position': 100, 'projected': 100, 'status': 'готово'}],
 'must_done': '2 з 2',
 'decision': 'випуск за графіком',
 'focus': []}),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_08(args, expected):
    check(8, FUNC, args, expected)
