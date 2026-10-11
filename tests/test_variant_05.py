"""Відкриті тести задачі 5: Апетит і вирізання обсягу.

Запуск: pytest tests/test_variant_05.py
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

FUNC = "fit_scope"
CASES = [
    ('T05-S1-1', ([{'name': 'План залу з вибором місця', 'weeks': 2, 'must': True, 'priority': 0},
  {'name': 'Оплата карткою', 'weeks': 1, 'must': True, 'priority': 0},
  {'name': 'Нагадування про бронь', 'weeks': 1, 'must': False, 'priority': 2},
  {'name': 'Повторні бронювання', 'weeks': 2, 'must': False, 'priority': 1},
  {'name': 'Історія бронювань', 'weeks': 1, 'must': False, 'priority': 3, 'needs': 'Нагадування про бронь'}],
 6,
 1), {'capacity': 6,
 'kept': ['План залу з вибором місця', 'Оплата карткою', 'Нагадування про бронь', 'Повторні бронювання'],
 'cut': [{'name': 'Історія бронювань', 'reason': 'не вистачає тижнів (потрібно 1, залишилось 0)'}],
 'used': 6,
 'left': 0}),
    ('T05-S1-2', ([{'name': 'План залу з вибором місця', 'weeks': 2, 'must': True, 'priority': 0},
  {'name': 'Оплата карткою', 'weeks': 1, 'must': True, 'priority': 0},
  {'name': 'Нагадування про бронь', 'weeks': 1, 'must': False, 'priority': 2},
  {'name': 'Повторні бронювання', 'weeks': 2, 'must': False, 'priority': 1},
  {'name': 'Історія бронювань', 'weeks': 1, 'must': False, 'priority': 3, 'needs': 'Нагадування про бронь'}],
 2,
 1), ValueError("Обов'язкові скоупи (3 тижн.) не вкладаються в апетит (2 тижн.)")),
    ('T05-S2-1', ([{'name': 'Картка набору з ціною за порцію', 'weeks': 1, 'must': True, 'priority': 0},
  {'name': 'Оформлення підписки', 'weeks': 2, 'must': True, 'priority': 0},
  {'name': 'Порівняння наборів', 'weeks': 2, 'must': False, 'priority': 1},
  {'name': 'Пауза підписки', 'weeks': 1, 'must': False, 'priority': 2},
  {'name': 'Промокод у кошику', 'weeks': 1, 'must': False, 'priority': 3, 'needs': 'Оформлення підписки'}],
 6,
 1), {'capacity': 6,
 'kept': ['Картка набору з ціною за порцію', 'Оформлення підписки', 'Порівняння наборів', 'Пауза підписки'],
 'cut': [{'name': 'Промокод у кошику', 'reason': 'не вистачає тижнів (потрібно 1, залишилось 0)'}],
 'used': 6,
 'left': 0}),
    ('T05-S2-2', ([{'name': 'Картка набору з ціною за порцію', 'weeks': 1, 'must': True, 'priority': 0},
  {'name': 'Оформлення підписки', 'weeks': 2, 'must': True, 'priority': 0},
  {'name': 'Порівняння наборів', 'weeks': 2, 'must': False, 'priority': 1},
  {'name': 'Пауза підписки', 'weeks': 1, 'must': False, 'priority': 2},
  {'name': 'Промокод у кошику', 'weeks': 1, 'must': False, 'priority': 3, 'needs': 'Оформлення підписки'}],
 2,
 2), {'capacity': 4,
 'kept': ['Картка набору з ціною за порцію', 'Оформлення підписки', 'Пауза підписки'],
 'cut': [{'name': 'Порівняння наборів', 'reason': 'не вистачає тижнів (потрібно 2, залишилось 1)'},
         {'name': 'Промокод у кошику', 'reason': 'не вистачає тижнів (потрібно 1, залишилось 0)'}],
 'used': 4,
 'left': 0}),
    ('T05-S3-1', ([{'name': 'Короткі уроки', 'weeks': 2, 'must': True, 'priority': 0},
  {'name': 'Тест наприкінці модуля', 'weeks': 1, 'must': True, 'priority': 0},
  {'name': 'Нагадування в месенджері', 'weeks': 1, 'must': False, 'priority': 1},
  {'name': 'Значок за модуль', 'weeks': 1, 'must': False, 'priority': 2, 'needs': 'Тест наприкінці модуля'},
  {'name': 'Таблиця лідерів', 'weeks': 2, 'must': False, 'priority': 3, 'needs': 'Значок за модуль'}],
 6,
 1), {'capacity': 6,
 'kept': ['Короткі уроки', 'Тест наприкінці модуля', 'Нагадування в месенджері', 'Значок за модуль'],
 'cut': [{'name': 'Таблиця лідерів', 'reason': 'не вистачає тижнів (потрібно 2, залишилось 1)'}],
 'used': 5,
 'left': 1}),
    ('T05-S3-2', ([{'name': 'Короткі уроки', 'weeks': 2, 'must': True, 'priority': 0},
  {'name': 'Тест наприкінці модуля', 'weeks': 1, 'must': True, 'priority': 0},
  {'name': 'Нагадування в месенджері', 'weeks': 1, 'must': False, 'priority': 1},
  {'name': 'Значок за модуль', 'weeks': 1, 'must': False, 'priority': 2, 'needs': 'Тест наприкінці модуля'},
  {'name': 'Таблиця лідерів', 'weeks': 2, 'must': False, 'priority': 3, 'needs': 'Значок за модуль'}],
 2,
 1), ValueError("Обов'язкові скоупи (3 тижн.) не вкладаються в апетит (2 тижн.)")),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_05(args, expected):
    check(5, FUNC, args, expected)
