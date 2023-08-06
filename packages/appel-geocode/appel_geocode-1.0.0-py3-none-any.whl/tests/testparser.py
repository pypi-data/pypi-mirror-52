import unittest
from typing import List, Any, cast, Iterable, Union

import matplotlib.pyplot
import numpy
import shapely.geometry
from typing_extensions import Final

from generate_tree import GenerateTree
from _region import Region


class ParserTestCase(unittest.TestCase):
    tree: numpy.ndarray

    def testGenerate(self) -> None:
        GenerateTree.generate()
        self.testAll()

    def __plot(self) -> None:
        matplotlib.pyplot.plot(*self.tree[1].polygon.exterior.xy)
        matplotlib.pyplot.show()
        matplotlib.pyplot.plot(*self.tree[1][0].polygon.exterior.xy)
        matplotlib.pyplot.show()
        matplotlib.pyplot.plot(*self.tree[1][0][0].polygon.exterior.xy)
        matplotlib.pyplot.show()
        matplotlib.pyplot.plot(*self.tree[1][0][0][0].polygon.exterior.xy)
        matplotlib.pyplot.show()

    def __testcoordinate(self) -> None:
        xy: Final[Any] = self.tree[0][0][0][0].polygon.centroid.xy
        x = float(xy[0][0])
        y = float(xy[1][0])
        xl = -46.6481
        yl = -23.651
        x, y, xl, yl = [round(w, 3) for w in [x, y, xl, yl]]

        if x != xl or y != yl:
            raise RuntimeError("Coordenadas de sp erradas:", x, y, xl, yl)

    @staticmethod
    def __checkRegion(region: Region) -> None:
        if region.uid <= 0:
            raise RuntimeError("inválido" + region.__str__())
        if isinstance(region.polygon, shapely.geometry.MultiPolygon):
            for polygon in region.polygon:
                if not polygon.is_valid:
                    x: List[float] = []
                    y: List[float] = []
                    x += polygon.exterior.xy[0]
                    y += polygon.exterior.xy[1]
                    matplotlib.pyplot.plot(x, y)
                    matplotlib.pyplot.show()
        else:
            if not region.polygon.is_valid:
                print("region " + str(region.uid) + " not valid")
                x, y = region.polygon.xy
                matplotlib.pyplot.plot(x, y)
                matplotlib.pyplot.show()

    def __checkTree(self,
                    region: Union[Region, None] = None,
                    depth: int = 0) -> None:
        if region is None:
            for state in self.tree:
                self.__checkTree(state, 1)
        elif depth < 4:
            # noinspection Mypy
            for subregion in region:
                self.__checkRegion(subregion)
                self.__checkTree(subregion, depth + 1)
        else:
            self.__checkRegion(region)

    def __simplifiedPlot(self) -> None:
        city = self.tree[0][0]
        x: List[float] = []
        y: List[float] = []
        for region in city:
            x_, y_ = None, None
            if isinstance(region.polygon, shapely.geometry.MultiPolygon):
                for polygon in region.polygon:
                    x_, y_ = polygon.exterior.xy
            else:
                x_, y_ = region.polygon.exterior.xy
            x += list(cast(Iterable[float], x_))
            y += list(cast(Iterable[float], y_))

            matplotlib.pyplot.plot(x, y)
        matplotlib.pyplot.show()

    def testAll(self) -> None:
        self.tree = GenerateTree.read()

        self.__plot()
        self.__testcoordinate()
        self.__checkTree()
        self.__simplifiedPlot()
