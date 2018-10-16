"""Различные константы для построения модели"""
import math
import wx
from wx import RealPoint


class Model:
    def __init__(self, size=3, radius=120):
        """
        :param size: Размер модели (количество дуг с одной стороны, всегда больше 2)
        :param radius: Радиус вписанной окружности
        """
        self.size = size
        self.seq = [r for r in range(self.size, self.size * 2 + 1)]
        self.seq.extend([r for r in range(self.size * 2 - 1, self.size - 1, -1)])
        self.radius = radius
        self.arc_length = radius / size  # расстояние   одной дуги

    def _draw(self, offset: wx.RealPoint, start: wx.RealPoint):
        """
        Получаем прямые для рисования, 1 проход
        :param offset: Вектор, задающий перемещение при продвижении на следующую
        :param start:
        :return:
        """
        cur = start
        for arc_count in self.seq:
            for current_arc in range(arc_count):
                pass

    def arcs(self):
        """
        Получаем прямые для рисования.
        """

        offset: wx.RealPoint = wx.RealPoint(self.arc_length * math.sqrt(3) / 2, self.arc_length / 2)
        start: wx.RealPoint = -self.size * offset
        self._draw(offset, start)
