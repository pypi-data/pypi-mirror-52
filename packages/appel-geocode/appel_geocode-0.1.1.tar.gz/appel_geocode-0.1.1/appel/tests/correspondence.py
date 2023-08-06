import os
import pickle
import statistics
import time
import unittest
from typing import Dict, List, Callable, cast, Tuple, Any

import geopandas
import numpy
import pandas
import psycopg2.extras
import shapely.geometry
from typing_extensions import Final

from appel import config
from appel.searchtree import SearchTree


class CorrespondenceTestCase(unittest.TestCase):
    @staticmethod
    def __checkTestInputArray(xs: numpy.ndarray, ys: numpy.ndarray) -> None:
        assert isinstance(xs, numpy.ndarray)
        assert isinstance(ys, numpy.ndarray)
        assert len(xs) == len(ys)
        xs.astype('float16')
        ys.astype('float16')

    # noinspection SqlResolve,SqlNoDataSourceInspection
    def postGIS(self, xs: numpy.ndarray, ys: numpy.ndarray) -> Tuple[float, pandas.DataFrame]:
        """
        Batch method for quering the postgresql test_name database
        :return: Return the query results: List containing the row of info
        """
        self.__checkTestInputArray(xs, ys)

        connection = psycopg2.connect(
            "dbname='gabrielcoimbra' user='gabrielcoimbra' host='nesped' "
            "password='pass'"
        )

        cur = connection.cursor()
        xs, ys = xs.tolist(), ys.tolist()
        start: Final[float] = time.time()

        sql = "INSERT INTO test_points VALUES (0, ST_SetSRID(ST_MakePoint(%s, %s), 4674))"

        psycopg2.extras.execute_batch(cur, sql, zip(cast(List[float], xs), cast(List[float], ys)))

        cur.execute("CREATE INDEX sidx_points ON test_points USING GIST (geom);")

        cur.execute(
            """select simplified_geometries_cidades.uid 
            from simplified_geometries_cidades, test_points 
            where ST_Contains(simplified_geometries_cidades.geom, test_points.geom)""")
        stop: Final[float] = time.time()

        results: List[Any] = list(cur)

        cur.execute("TRUNCATE test_points")
        cur.execute("DROP INDEX sidx_points")
        connection.commit()
        cur.close()

        return stop - start, pandas.DataFrame(results)

    def geoPandasTest(self, xs: numpy.ndarray, ys: numpy.ndarray) -> Tuple[float, pandas.DataFrame]:
        self.__checkTestInputArray(xs, ys)

        pontos: List[shapely.geometry.Point] = []
        for i in range(len(xs)):
            pontos.append(shapely.geometry.Point(xs[i], ys[i]))
        cidades: Final = geopandas.GeoDataFrame(geopandas.read_file(config.POLYGONS_PATHS['CITIES'])
                                                [['geometry', 'uid']],
                                                crs={'init': 'epsg:4674'})

        points: Final = geopandas.GeoDataFrame(geometry=pontos, crs={'init': 'epsg:4674'})
        start: Final[float] = time.time()
        results: Final[pandas.DataFrame] = geopandas.sjoin(points, cidades, how="inner", op='within')
        return time.time() - start, results

    def appelTest(self, xs: numpy.ndarray, ys: numpy.ndarray) -> Tuple[float, pandas.DataFrame]:
        self.__checkTestInputArray(xs, ys)

        correspondence = SearchTree()
        start: Final[float] = time.time()
        results: Final[pandas.DataFrame] = correspondence.query(xs, ys)
        return time.time() - start, results

    def test(self) -> None:

        for filename in os.listdir(config.RESOURCES_PATH + '/test_points/'):
            if not filename.endswith('.bin'):
                continue
            with open(config.RESOURCES_PATH + '/test_points/' + filename, 'rb') as file:
                testcase = pickle.load(file)

            methods: List[Callable[[numpy.ndarray,
                                    numpy.ndarray], Tuple[float, pandas.DataFrame]]] = \
                [
                    self.appelTest,
                    # self.postGIS,
                    # self.geoPandasTest
                ]

            tempos_dic: Dict[str, List[float]] = {}
            for _ in range(4):
                for method in methods:
                    tempo: float = method(testcase[0], testcase[1])[0]
                    try:
                        tempos_dic[method.__name__].append(tempo)
                    except KeyError:
                        tempos_dic[method.__name__] = [tempo]

            for nome, tempos in tempos_dic.items():
                media, desvio = [str(round(x, ndigits=2)).replace('.', ',')
                                 for x in (statistics.mean(tempos), statistics.stdev(tempos))]
                print(nome, media, desvio)
