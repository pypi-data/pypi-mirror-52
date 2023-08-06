import pickle
from typing import Dict, Union, Sized

import geopandas
import numpy
import pandas
from typing_extensions import Final

from appel import config, region


class Parser(object):
    """Stores a global access for a prefixed
    This is uddsed to ensure a
    """

    # array sorted by population containing tree
    tree = numpy.empty(config.MAX_STATES, dtype=object)

    @staticmethod
    def __mergeToUpperRegionAndSort(uppers: Dict[int, region.Region],
                                    lowers: Dict[int, region.Region]) -> None:
        def add(x: region.Region) -> None:
            try:
                uppers[x.upper].add(x)
            except KeyError as e:
                print("Não ache poly", e)
            except AttributeError as e:
                print("Erro de atributo", e)

        list(map(add, lowers.values()))

        # noinspection Mypy
        list(map(lambda x: x.sort(), uppers.values()))

    @classmethod
    def __readAndValidateAndSetTypesGDF(cls, path: str, upper_cast: bool = True,
                                        simplification: Union[float, None] = None) -> geopandas.GeoDataFrame:

        gdf: Final[geopandas.GeoDataFrame] = geopandas.read_file(path, engine="c")

        if simplification is None:
            gdf.geometry = gdf.geometry.simplify(config.SIMPLIFICATION)
        else:
            gdf.geometry = gdf.geometry.simplify(simplification)

        gdf.dropna(inplace=True)
        if upper_cast:
            # Tem que ser antes de passar para unsigned, pois checa valores negativos
            cls.__checkGDFValidity(gdf)
            gdf.uid = gdf.uid.astype('uint64', copy=False)
            gdf.upper = gdf.upper.astype('uint64', copy=False)

        print("Dropando\n ", gdf[gdf.isnull()])
        gdf.uid = gdf.uid.astype('uint64', copy=False)

        return gdf

    @staticmethod
    def __checkGDFValidity(gdf: geopandas.GeoDataFrame) -> None:
        """
        Auto explicatorio
        """
        inv: Final[Sized] = gdf[(gdf.uid.astype('int') <= 0) |
                                (gdf.upper.astype('int') <= 0)]
        if len(inv) > 0:
            print(inv)
            print("Dataset errado em uid ou upper.", len(inv))

        inv_poly: Final[pandas.DataFrame] = gdf[gdf.is_valid]
        if (len(gdf) - len(inv_poly)) > 0:
            print(inv_poly)
            print("Runtime polígonos inválidos", len(gdf) - len(inv_poly))

    @classmethod
    def _getCities(cls) -> Dict[int, region.Region]:
        """
        Get cities information and it's polygons
        :return: Dict[int, Region]
        """
        # xz loads faster
        cinfo: Final[pandas.DataFrame] = pandas.read_csv(config.CITIES_INFO_PATH, engine="c")

        cities: Dict[int, region.Region] = {}
        for _, row in cinfo.iterrows():
            uid: numpy.uintc = numpy.uint32(row["Código do Município"])
            population: numpy.uintc = numpy.uint32(
                str(row["População (Nº de habitantes)"]).replace(".", "")
            )
            cities[uid] = population

        gdf: Final[geopandas.GeoDataFrame] = cls.__readAndValidateAndSetTypesGDF(config.POLYGONS_PATHS["CITIES"],
                                                                                 simplification=0.005)
        for row in gdf.itertuples():
            cities[row.uid] = region.Region(row.uid, row.upper, numpy.uint32(cities[row.uid]), row.geometry)

        return cities

    @classmethod
    def _getMicros(cls) -> Dict[int, region.Region]:
        """
        Map microrregions
        :return: Dict[int, Region]
        """
        gdf: Final[geopandas.GeoDataFrame] = cls.__readAndValidateAndSetTypesGDF(config.POLYGONS_PATHS["MICROS"])

        micros: Dict[int, region.Region] = {}
        for row in gdf.itertuples():
            micros[row.uid] = region.Region(row.uid, row.upper, numpy.uint32(0), row.geometry)

        cls.__mergeToUpperRegionAndSort(micros, cls._getCities())

        return micros

    @classmethod
    def _getMesos(cls) -> Dict[int, region.Region]:
        """
        Map mesosregions
        :return: Dict[int, Region]
        """
        gdf: Final[geopandas.GeoDataFrame] = cls.__readAndValidateAndSetTypesGDF(config.POLYGONS_PATHS["MESOS"])

        mesos: Dict[int, region.Region] = {}
        for row in gdf.itertuples():
            mesos[row.uid] = region.Region(row.uid, row.upper, numpy.uint32(0), row.geometry)

        cls.__mergeToUpperRegionAndSort(mesos, cls._getMicros())

        return mesos

    @classmethod
    def _getStates(cls) -> Dict[int, region.Region]:
        """
        Iterate datasets
        Itera datasets para obter polígonos das cidades e somar população
        :return: Mapping id estado -> Estado
        """
        # Mapping id estado -> Estado

        gdf: Final[geopandas.GeoDataFrame] = cls.__readAndValidateAndSetTypesGDF(config.POLYGONS_PATHS["STATES"],
                                                                                 upper_cast=False)
        states: Dict[int, region.Region] = {}

        # Get tree polygon
        for row in gdf.itertuples():
            states[row.uid] = region.Region(row.uid, numpy.uint64(0), numpy.uint32(0), row.geometry)

        cls.__mergeToUpperRegionAndSort(states, cls._getMesos())

        return states

    @classmethod
    def _clean(cls, subregion: region.Region) -> None:
        if not subregion.subregions:
            subregion.clean(True)
        else:
            subregion.clean(False)
            # noinspection Mypy
            list(map(lambda x: cls._clean(x), subregion.subregions))

    @classmethod
    def generate(cls) -> None:
        """
        Generate the search structure for the cities.
        """
        # Pega dicionário não ordenado
        states: Final[Dict[int, region.Region]] = cls._getStates()

        cls.tree = numpy.array([x for x in states.values()])
        # Ordena os estados em si
        cls.tree[::-1].sort()

        # noinspection Mypy
        list(map(lambda x: cls._clean(x), cls.tree))

        # Escreve em disco
        cls._write()

    @classmethod
    def _write(cls) -> None:
        """ Write to disk generated tree list"""
        with open(config.TREE_PATH, "wb") as file:
            pickle.dump(cls.tree, file, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def read() -> numpy.ndarray:
        """ Read from disk generated tree"""
        with open(config.TREE_PATH, "rb") as file:
            return pickle.load(file)
