from typing import List, Tuple
from enum import Enum

from tqdm import tqdm

from typing import TypedDict

class BoundaryFinder3D:
    def __init__(self, grid: List[List[List[int]]]):
        """
        Инициализация BoundaryFinder3D с заданной 3D-сеткой. Если значение ячейки = 0, то ячейка пуста,
        если = 1 ячейка заполнена

        :param grid: 3D-сетка, представляющая блоки.
        """
        self._grid = grid
        self.mask = [[[0] * len(grid[0][0]) for _ in range(len(grid[0]))] for _ in range(len(grid))]
        self._checked = set()
        self._to_check = []

    def find_boundaries(self):
        """
        Поиск границ в 3D-сетке.
        """
        self._to_check.append((0, 0, 0))
        total_blocks = len(self._grid) * len(self._grid[0]) * len(self._grid[0][0])
        pbar = tqdm(total=total_blocks)

        while self._to_check:
            self._process_points(pbar)

        pbar.close()

    def _process_points(self, pbar: tqdm):
        """
        Обработка точек и обновление прогресс-бара.

        :param pbar: Прогресс-бар для отображения прогресса.
        """

        points = self._to_check[:]
        self._to_check.clear()
        for point in points:
            self._process_cell(point)
        pbar.n = len(self._checked)
        pbar.refresh()

    def _process_cell(self, coord: Tuple[int, int, int]):
        """
        Обработка отдельной ячейки в сетке.

        :param coord: Координаты ячейки.
        """
        x, y, z = coord
        if coord in self._checked:
            return

        self._checked.add(coord)

        if self._grid[x][y][z] == 1:
            self.mask[x][y][z] = 1
        else:
            self._scan_nearby_points(x, y, z)

    def _scan_nearby_points(self, x, y, z):
        self._add_to_check(x + 1, y, z)
        self._add_to_check(x - 1, y, z)
        self._add_to_check(x, y + 1, z)
        self._add_to_check(x, y - 1, z)
        self._add_to_check(x, y, z + 1)
        self._add_to_check(x, y, z - 1)

    def _add_to_check(self, x: int, y: int, z: int):
        """
        Добавление координат в список для проверки.

        :param x: Координата x.
        :param y: Координата y.
        :param z: Координата z.
        """
        if self._is_within_bounds(x, y, z) and (x, y, z) not in self._checked:
            self._to_check.append((x, y, z))

    def _is_within_bounds(self, x: int, y: int, z: int) -> bool:
        """
        Проверка, находятся ли координаты в пределах границ сетки.

        :param x: Координата x.
        :param y: Координата y.
        :param z: Координата z.
        :return: True, если координаты в пределах границ, иначе False.
        """
        return 0 <= x < len(self._grid) and 0 <= y < len(self._grid[0]) and 0 <= z < len(self._grid[0][0])
