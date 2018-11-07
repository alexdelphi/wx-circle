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

    def arcs(self) -> typing.Dict[float, typing.List[typing.Tuple[wx.Point2D, wx.Point2D]]]:
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
        angles: typing.Dict[str, float] = {name: i * full_angle / direction_count for i, name in enumerate(directions)}
        # Векторы, соответствующие углам поворота.
        # На основании этих векторов потом вычисляется дистанция между точками
        # Эти векторы "математические", с длиной 1 по построению
        base_vectors: typing.List[typing.Tuple[str, wx.Point2D]] = [(name, wx.Point2D(
            math.cos(a), math.sin(a)
        )) for name, a in angles]
        points: typing.Dict[float, typing.List[typing.Tuple[wx.Point2D, wx.Point2D]]] = []
        for displacement, name in enumerate(directions):
            # Повернем векторы, заодно конвертируем List<Tuple<str, int>> -> Dictionary<str, int>
            vectors: typing.Dict[str, wx.Point2D] = {k: v
                                                     for i, _ in enumerate(base_vectors)
                                                     for k, v in base_vectors[(i + displacement) % direction_count]}
            points_below: typing.List[wx.Point2D] = [
                row_disp * vectors['up'] + col_disp * v
                # чтобы не повторять отдельно последовательность для "правого" и "левого" векторов
                for v, start in {vectors['right']: 0, vectors['left']: 1}.items()
                for col_disp in range(start, self.size)
                for row_disp in range(-col_disp, self.size)
            ]
            points[angles[name]] = [(x + vectors['up'], x) for x in points_below]
        return points
