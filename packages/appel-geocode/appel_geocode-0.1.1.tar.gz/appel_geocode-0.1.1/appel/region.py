from typing import Set, List, Union, TypeVar, cast

import numpy
import shapely.geometry
from typing_extensions import Final

TRegion = TypeVar('TRegion', bound='Region')


class Region(object):
    """A city representation. Will store just the needed information"""

    uid: Final[numpy.uint64]
    polygon: Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon]
    population: numpy.uint32
    upper: Final[numpy.uint64]  # Temporary attribute
    ids: Final[Set[int]]  # Temporary attribute
    # noinspection Mypy
    subregions: Final[List[Union[TRegion]]]  # Cities doesn't have this attribute

    def __init__(
            self,
            uid: numpy.uint64,
            upper: numpy.uint64,
            population: numpy.uint32,
            polygon: shapely.geometry.Polygon,

    ):
        """
        :param polygon: Shapefile polygon representing the Region
        """
        self.uid = uid
        self.population = population
        self.ids = set()
        self.subregions = []
        self.upper = upper
        self.polygon = polygon

    def __getitem__(self, item: int) -> TRegion:
        return self.subregions[item]

    def __str__(self) -> str:
        return str(self.uid + len(self.subregions) + self.upper)

    def __gt__(self, other: TRegion) -> bool:
        """Useful for numpy sort"""
        return cast(bool, self.population > other.population)

    def __lt__(self, other: TRegion) -> bool:
        """Useful for numpy sort"""
        return cast(bool, self.population < other.population)

    def add(self, subregion: TRegion) -> None:
        """
        Add subregion to dataset and sum it's population to our own
        :param subregion: Region
        :return:
        """
        if subregion.uid not in self.ids:
            self.population += subregion.population
            self.subregions.append(subregion)
            self.ids.add(subregion.uid)
        else:
            raise RuntimeError("Tried to add the same id: " + str(subregion.uid) + "to this region:" + str(type(self)))

    def clean(self, final_region: bool) -> None:
        """
        Delete unused memories after parsing
        """
        del self.ids
        if final_region:
            del self.subregions
        del self.population
        del self.upper

    def sort(self) -> None:
        """
        Sort region based on it's population
        """
        self.subregions.sort(reverse=True)

    def contains(self, point: shapely.geometry.Point) -> bool:
        """
        Check if a point is inside our polygon
        :param point: shapely Point
        :return: True if it's inside False if not
        """
        return cast(bool, self.polygon.contains(point))
