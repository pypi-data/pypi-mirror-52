from math import floor
from pickle import dump
from typing import List, Tuple

import geopandas
import numpy.random.mtrand
import pandas
import shapely
import shapely.geometry
import shapely.vectorized
from numpy import ndarray, array
from typing_extensions import Final

from appel import config, generate_tree

TEST_RANGE: Final[ndarray] = array([10000, 100000, 1000000])
BRASIL_POPULATION: Final[int] = 206081432


def __decreaseToFitTestSize(test_size: int,
                            lats_final: List[float],
                            longs_final: List[float]) -> Tuple[List[float],
                                                               List[float]]:
    if len(lats_final) > test_size:
        return lats_final[0:test_size], longs_final[0:test_size]
    else:
        return lats_final, longs_final


def __checkConsistency(test_size: int,
                       lats_final: List[float],
                       longs_final: List[float],
                       p: shapely.geometry.Polygon) -> None:
    if len(lats_final) != len(longs_final):
        raise RuntimeError("Quantidade de longitudes e latitudes diferentes")

    matched_test: Final[ndarray] = shapely.vectorized.contains(p, longs_final, lats_final)

    if matched_test.sum() < test_size:
        raise RuntimeError("Ainda faltam alguns pontos", matched_test.sum(), test_size)


def randomDatasetGenerate() -> None:
    for test_size in TEST_RANGE:
        lats_final: List[float] = []
        longs_final: List[float] = []
        brp: shapely.geometry.Polygon = geopandas.read_file(config.RESOURCES_PATH + 'brasil').geometry.iloc[0]
        (minx, miny, maxx, maxy) = brp.bounds  # type: float, float, float, float

        while len(lats_final) < test_size:
            lats: ndarray = numpy.random.mtrand.uniform(miny, maxy, test_size)

            longs: ndarray = numpy.random.mtrand.uniform(minx, maxx, test_size)

            matched: ndarray = shapely.vectorized.contains(brp, longs, lats)

            lats_final += lats[matched].tolist()
            longs_final += longs[matched].tolist()

        lats_final, longs_final = __decreaseToFitTestSize(test_size, lats_final, longs_final)
        __checkConsistency(test_size, lats_final, longs_final, brp)

        with open('rand' + str(test_size) + '.bin', 'wb') as file:
            dump((longs_final, lats_final), file)


def gaussianDatasetGenerate() -> None:  # NOSONAR
    cities_info: pandas.DataFrame = \
        pandas.read_csv(config.CITIES_INFO_PATH, engine='c')[['Código do Município', 'População (Nº de habitantes)']]
    cities_info = cities_info.set_index('Código do Município')

    for test_size in TEST_RANGE:

        tree = generate_tree.GenerateTree.read('brazil.bin')
        lats_final: List[float] = []
        longs_final: List[float] = []

        for state in tree:
            for meso in state:
                for micro in meso:
                    for city in micro:
                        polygon: shapely.geometry.Polygon = city.polygon
                        (minx, miny, maxx, maxy) = polygon.bounds

                        lats_local: List[float] = []
                        longs_local: List[float] = []
                        size_local = floor((cities_info.loc[city.uid] / BRASIL_POPULATION) * test_size)

                        while len(lats_local) < size_local:
                            lats = numpy.random.mtrand.uniform(miny, maxy, size_local)

                            longs = numpy.random.mtrand.uniform(minx, maxx, size_local)

                            conts = shapely.vectorized.contains(polygon, longs, lats)

                            lats_local += lats[conts].tolist()
                            longs_local += longs[conts].tolist()

                        lats_final, longs_final = __decreaseToFitTestSize(test_size, lats_final, longs_final)

                        __checkConsistency(test_size, lats_local, longs_local, polygon)

                        lats_final += lats_local
                        longs_final += longs_local

        with open('gauss' + str(test_size) + '.bin', 'wb') as file:
            dump((array(longs_final).astype('float16'), array(lats_final).astype('float16')), file)
