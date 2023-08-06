import math
import multiprocessing
import pickle
from typing import List, Union, Any

import numpy
import pandas
import shapely.vectorized
from typing_extensions import Final


class SearchTree:
    tree: numpy.ndarray
    THREAD_TRIGGER: Final[int] = 100
    MAX_WAIT: Final[float] = 200.0

    def __init__(self, tree_path: str = 'tree.bin') -> None:
        """
        Read state database generated tree list
        :return: array sorted by population containing tree
        """
        # Não precisa carregar se já estiver no disco
        with open(tree_path, "rb") as file:
            self.tree = pickle.load(file)

    def _wait(self, events: numpy.ndarray, tasks: List[multiprocessing.Process]) -> None:
        """
        Wait for threads to finish
        :return:
        """
        # _wait for all processes to finish

        for event in events:
            if not event.wait(timeout=self.MAX_WAIT):
                for task in tasks:
                    task.terminate()
                raise RuntimeError("Dataset demorou muito tempo para processar!")

    def query(self, longitudes: numpy.ndarray, latitudes: numpy.ndarray) -> pandas.DataFrame:
        """
        Multiprocessed function for looking up which city a point is on.
        divided in three phases map -> _wait -> reduce.
        :return: dictionary to   map: city uid -> test_points counted
        """

        ds_size: Final[int] = len(longitudes)
        if ds_size < self.THREAD_TRIGGER:
            return self._doMap(None, None, latitudes, longitudes, False)
        else:
            # noinspection Mypy
            queue: multiprocessing.Queue = multiprocessing.Queue()

            events: numpy.ndarray = numpy.empty(multiprocessing.cpu_count(), dtype=object)
            chunk_size: Final[int] = numpy.uint32(math.ceil(len(longitudes) / multiprocessing.cpu_count()))
            tasks: List[multiprocessing.Process] = []

            for i in range(multiprocessing.cpu_count()):
                events[i] = multiprocessing.Event()
                begin: int = chunk_size * i
                end: int = chunk_size * (i + 1)

                task: multiprocessing.Process = multiprocessing.Process(
                    target=self._doMap,
                    args=(
                        queue,
                        events[i],
                        longitudes[begin:end],
                        latitudes[begin:end],
                        True
                    ),
                )
                tasks.append(task)
                task.start()

            self._wait(events, tasks)
            return self._doReduce(queue)

    # noinspection Mypy
    @staticmethod
    def _doReduce(queue: multiprocessing.Queue) -> pandas.DataFrame:
        """
        Reduce phase: if different thread found a point on the same city
        this functions sum all these equals id
        This subfunction has access to the main function scope.
        :return:
        """
        results: List[pandas.DataFrame] = []
        for _ in range(queue.qsize()):
            results.append(queue.get())

        return pandas.concat(results)

    @staticmethod
    def __finishMap(xs: List[numpy.ndarray],
                    ys: List[numpy.ndarray],
                    cids: List[int]) -> pandas.DataFrame:

        return pandas.DataFrame({'uid': pandas.Series(cids, dtype='uint64'),
                                 'longitude': numpy.concatenate(xs).astype('float32', copy=False),
                                 'latitude': numpy.concatenate(ys).astype('float32', copy=False)})

    # Complexidade é necessária para questões de performance
    # noinspection Mypy
    def _doMap(  # NOSONAR
            self,
            queue: Union[multiprocessing.Queue, None],
            event: Union[Any, None],  # TODO: type callable how?
            x: numpy.ndarray,
            y: numpy.ndarray,
            parallel: bool
    ) -> Union[pandas.DataFrame, None]:

        """
        """
        # Initilize not found count
        ds_size: Final[int] = len(x)
        uids: List[int] = []
        lats: List[numpy.ndarray] = []
        longs: List[numpy.ndarray] = []
        states_acc: int = 0
        for state in self.tree:
            l0 = shapely.vectorized.contains(state.polygon, x, y)
            x0, y0 = x[l0], y[l0]
            states_found = x[l0].shape[0]
            states_acc += states_found
            if states_found > 0:
                meso_acc = 0
                for meso in state:
                    l1 = shapely.vectorized.contains(meso.polygon, x0, y0)
                    x01, y01 = x0[l1], y0[l1]
                    mesos_found = x01.shape[0]
                    meso_acc += mesos_found
                    if mesos_found > 0:
                        micro_acc = 0
                        for micro in meso:
                            l2 = shapely.vectorized.contains(
                                micro.polygon, x01, y01
                            )
                            x012, y012 = x01[l2], y01[l2]
                            micros_found = x012.shape[0]
                            micro_acc += micros_found
                            if micros_found > 0:
                                city_acc = 0
                                for city in micro:
                                    l3 = shapely.vectorized.contains(
                                        city.polygon, x012, y012
                                    )
                                    x0123, y0123 = x012[l3], y012[l3]
                                    city_acc += x0123.shape[0]
                                    if city_acc > 0:
                                        uids += [city.uid for x in range(len(x0123))]
                                        longs.append(x0123)
                                        lats.append(y0123)

                                    if city_acc == micros_found:
                                        break
                            if mesos_found == micro_acc:
                                break
                    if meso_acc == states_found:
                        break
            if states_acc == ds_size:
                break

        results: Final[pandas.DataFrame] = self.__finishMap(longs, lats, uids)
        if parallel:

            # noinspection Mypy
            queue.put(results)

            # noinspection Mypy
            event.set()
            return None
        else:
            return results
