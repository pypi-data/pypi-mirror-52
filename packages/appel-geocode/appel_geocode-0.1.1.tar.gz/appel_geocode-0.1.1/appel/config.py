from typing import Dict

import numpy
from typing_extensions import Final

RESOURCES_PATH: Final[str] = "appel/resources/"
DOTS_PER_CITY_TYPE = Dict[int, int]

DATASETS_TESTS_PATH: Final[str] = RESOURCES_PATH + "/test_points/"

TREE_PATH: Final[str] = "tree.bin"
CITIES_INFO_PATH: Final[str] = RESOURCES_PATH + "cidades_info_2016.csv.xz"
POLYGONS_PATHS: Final[Dict[str, str]] = {
    "STATES": RESOURCES_PATH + "estados",
    "CITIES": RESOURCES_PATH + "cidades",
    "MESOS": RESOURCES_PATH + "mesos",
    "MICROS": RESOURCES_PATH + "micros",
    "CITIES_ATTRS": RESOURCES_PATH + "cities_attrs.bin",
}
MAX_STATES: numpy.uint8 = numpy.uint8(27)
# Simplification values on each polygon

SIMPLIFICATION: float = 0.01
