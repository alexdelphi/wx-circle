"""
Различные константы для построения модели
TODO rewrite the algorithm to build two symmetric constructs instead of one
"""
import itertools
import math
import wx
import typing


class Model:
    def __init__(self, centre: wx.Point2D, size: int=3, radius: int=120):
        """
        :param size: Размер модели (количество дуг с одной стороны, всегда больше 2)
        :param radius: Радиус вписанной окружности
        """
        self.size = size
        self.centre = centre
        self.radius = radius
        self.arc_length: float = radius / size  # расстояние одной дуги

    def _get_points(self) -> typing.List[wx.Point2D]:
        """
        Получаем точки ("сетку") для рисования.
        """
        # Полный угол
        full_angle: float = 2 * math.pi
        # Названия направлений, для удобства
        # Они же определяют количество углов поворота.
        directions: typing.List[str] = ['up', 'right', 'left']
        direction_count: int = len(directions)
        # Углы поворота
        angles: typing.Dict[str, float] = {name: i * full_angle / len(directions) for i, name in enumerate(directions)}
        # Векторы, соответствующие углам поворота.
        # На основании этих векторов потом вычисляется дистанция между точками
        # Эти векторы "математические", с длиной 1 по построению
        base_vectors: typing.List[typing.Tuple[str, wx.Point2D]] = [(name, wx.Point2D(
            math.cos(a), math.sin(a)
        )) for name, a in angles]
        vectors: typing.List[wx.Point2D] = [angle for name, angle in base_vectors]
        rotated_vectors = (vectors[(i + 1) % direction_count] for i in range(direction_count))
        # Множество векторов на осях
        points: typing.List[wx.Point2D] = [v * i for i in range (direction_count) for v in base_vectors]
        # Все остальные векторы не на осях
        points.extend([vec[0] * i + vec[1] * j
                      for i in range(1, direction_count)
                      for j in range(1, direction_count)
                      for vec in itertools.zip_longest(vectors, rotated_vectors)])
        return points

    @staticmethod
    def distance(x: wx.Point2D, y: wx.Point2D) -> float:
        return math.sqrt((y[1] - x[1]) ** 2 + (y[0] - x[0]) ** 2)

    def nearest_points(self) -> typing.List[typing.Tuple[wx.Point2D, wx.Point2D]]:
        points: typing.List[wx.Point2D] = self._get_points()
        return [
            (x, y) for x in points for y in points if abs(__class__.distance(x, y) - 1) <= 1e-3
        ]
