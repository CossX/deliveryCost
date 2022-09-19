import pytest
import random
import pandas as pd
from src import CalculatorBase
from src.CalculatorBase import get_delivery_cost

calc = CalculatorBase
exception_assertion_error_text = "Текст ошибки отличается от ожидаемого"


def get_data():
    df = pd.read_csv('src/test_data/pairwise_data.csv')
    return [tuple(row) for row in df.values]


@pytest.mark.parametrize("distance", [-1, 0])
def test_negative_distance_less_zero(distance):
    with pytest.raises(Exception) as e:
        get_delivery_cost(distance, calc.Size.BIG.value, calc.Fragile.NO.value, calc.Rate.HIGH_LOAD.value)
    expected_exception_msg = "Недопустимое значение расстояния до пункта назначения. Расстояние должно быть больше 0"
    actual_exception_msg = e.value.args[0]
    assert expected_exception_msg == actual_exception_msg, exception_assertion_error_text


def test_negative_distance_and_fragile():
    distance = random.uniform(30.1, float('inf'))
    with pytest.raises(Exception) as e:
        get_delivery_cost(distance, calc.Size.SMALL.value, calc.Fragile.YES.value, calc.Rate.VERY_HIGH_LOAD.value)
    expected_exception_msg = "Мы не доставляем хрупкие грузы на расстояния более 30 км"
    actual_exception_msg = e.value.args[0]
    assert expected_exception_msg == actual_exception_msg, exception_assertion_error_text


def test_min_delivery_cost():
    expected_cost = 400
    actual_cost = get_delivery_cost(2, calc.Size.SMALL.value, calc.Fragile.NO.value, calc.Rate.NORMAL_LOAD.value)
    assert expected_cost == actual_cost, "Стоимость доставки оличается от минимальной"


@pytest.mark.parametrize("distance, size, fragile, rate, expected_cost", get_data())
def test_pairwise(distance, size, fragile, rate, expected_cost):
    actual_cost = get_delivery_cost(distance, size, fragile, rate)
    assert expected_cost == actual_cost, "Расчетная стоимость не соответствует ожидаемой"
