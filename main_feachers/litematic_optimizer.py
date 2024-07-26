from litemapy import Schematic, BlockState, Region
from tqdm import tqdm

from main_feachers.boundary_finder_3D import BoundaryFinder3D


class LitematicOptimizer:
    def __init__(self, path: str):
        """
        Инициализация LitematicOptimizer с загрузкой схемы.

        :param path: Путь к файлу схемы.
        """
        self._schematic = Schematic.load(path)
        self._ignored_blocks = {"minecraft:air"}
        self._regions = {}

    def set_ignored_blocks(self, ignored_blocks: set):
        """
        Установить блоки, которые будут игнорироваться при оптимизации.

        :param ignored_blocks: Набор идентификаторов блоков для игнорирования.
        """
        self._ignored_blocks = ignored_blocks

    def optimize(self):
        """
        Оптимизация схемы путем удаления блоков, не находящихся на границах.
        """
        for i, region in enumerate(self._schematic.regions.values()):
            grid = self._create_grid(region)
            mask = self._find_boundaries(grid)
            self._apply_mask_to_region(region, mask)
            self._regions[str(i)] = region

        self._save_optimized_schematic()

    def _create_grid(self, region: Region) -> list:
        """
        Создание 3D-сетки, представляющей регион.

        :param region: Регион схемы.
        :return: 3D-сетка региона.
        """
        return [
            [
                [self._check_block_availability(region, x, y, z) for z in region.zrange()]
                for y in region.yrange()
            ]
            for x in region.xrange()
        ]

    def _check_block_availability(self, region: Region, x: int, y: int, z: int) -> int:
        """
        Определение полных блоков.

        :param region: Регион схемы.
        :param x: Координата x.
        :param y: Координата y.
        :param z: Координата z.
        :return: 1 если блок не игнорируется, иначе 0.
        """
        block_id = region.getblock(x, y, z).blockid
        return 1 if block_id not in self._ignored_blocks else 0

    def _find_boundaries(self, grid: list) -> list:
        """
        Нахождение границ в 3D-сетке.

        :param grid: 3D-сетка.
        :return: Маска с границами.
        """
        boundary_finder = BoundaryFinder3D(grid)
        boundary_finder.find_boundaries()
        return boundary_finder.mask

    def _apply_mask_to_region(self, region: Region, mask: list):
        """
        Применение маски к региону для удаления лишних блоков.

        :param region: Регион схемы.
        :param mask: Маска с границами.
        """
        air = BlockState("minecraft:air")

        for x in tqdm(region.xrange()):
            for y in region.yrange():
                for z in region.zrange():
                    if mask[x][y][z] == 0 and self._check_block_availability(region, x, y, z):
                        region.setblock(x, y, z, air)

    def _save_optimized_schematic(self):
        """
        Сохранение оптимизированной схемы в файл.
        """
        temp_schematic = Schematic(name="optimized", author="Modecstap", regions=self._regions)
        temp_schematic.save("optimized_schematic.litematic")
