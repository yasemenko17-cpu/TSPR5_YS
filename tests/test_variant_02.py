"""Відкриті тести задачі 2: Переконання й ставка за шаблоном.

Запуск: pytest tests/test_variant_02.py
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

FUNC = "parse_belief_bet"
CASES = [
    ('T02-S1-1', ('Віримо, що довга форма бронювання відлякує нових користувачів. Метрика «частка бронювань серед '
 'відкриттів»: з 28 % до 33 %.',
 'Ставка «Бронювання в два дотики»: апетит 2 тижн., метрика «частка бронювань серед відкриттів».'), {'claim': 'довга форма бронювання відлякує нових користувачів',
 'metric': 'частка бронювань серед відкриттів',
 'baseline': 28,
 'target': 33,
 'effect_pp': 5,
 'title': 'Бронювання в два дотики',
 'appetite': 2}),
    ('T02-S2-1', ('Віримо, що незрозуміла ціна на сторінці набору зупиняє покупців. Метрика «частка оформлених підписок»: з '
 '12 % до 15 %.',
 'Ставка «Ціна за порцію на картці набору»: апетит 1 тижн., метрика «частка оформлених підписок».'), {'claim': 'незрозуміла ціна на сторінці набору зупиняє покупців',
 'metric': 'частка оформлених підписок',
 'baseline': 12,
 'target': 15,
 'effect_pp': 3,
 'title': 'Ціна за порцію на картці набору',
 'appetite': 1}),
    ('T02-S3-1', ('Віримо, що перший модуль занадто довгий для вечірнього навчання. Метрика «частка завершених перших '
 'модулів»: з 41 % до 48 %.',
 'Ставка «Модуль із трьох коротких уроків»: апетит 6 тижн., метрика «частка завершених перших модулів».'), {'claim': 'перший модуль занадто довгий для вечірнього навчання',
 'metric': 'частка завершених перших модулів',
 'baseline': 41,
 'target': 48,
 'effect_pp': 7,
 'title': 'Модуль із трьох коротких уроків',
 'appetite': 6}),
    ('T02-S3-2', ('Віримо, що все добре. Метрика «a»: з 1 % до 2 %.', 'Ставка «X»: апетит 1 тижн., метрика «a».'), ValueError('Твердження має містити щонайменше три слова')),

]


@pytest.mark.parametrize("args, expected", [pytest.param(a, e, id=c) for c, a, e in CASES])
def test_task_02(args, expected):
    check(2, FUNC, args, expected)
