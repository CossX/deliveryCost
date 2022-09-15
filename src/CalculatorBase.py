from enum import Enum


class Size(Enum):
    BIG = 200
    SMALL = 100


class Fragile(Enum):
    YES = 300
    NO = 0


class Rate(Enum):
    VERY_HIGH_LOAD = 1.6
    HIGH_LOAD = 1.4
    HEAVY_LOAD = 1.2
    NORMAL_LOAD = 1


DISTANCE_COST_MAP = {
    2: 50,
    10: 100,
    30: 200,
    float('inf'): 300,
}


def get_distance_margin(distance):
    for max_distance, distance_cost in DISTANCE_COST_MAP.items():
        if distance <= max_distance:
            return distance_cost


def get_delivery_cost(distance: float, size: Size, fragile: Fragile, rate: Rate):
    min_cost = 400
    if distance <= 0:
        raise Exception("Недопустимое значение расстояния до пункта назначения. Расстояние должно быть больше 0")
    if fragile == Fragile.YES.value and distance > 30:
        raise Exception("Мы не доставляем хрупкие грузы на расстояния более 30 км")
    distance_cost = get_distance_margin(distance)
    cost = (distance_cost + size + fragile) * rate
    if cost < min_cost:
        return min_cost
    else:
        return round(cost, 0)
