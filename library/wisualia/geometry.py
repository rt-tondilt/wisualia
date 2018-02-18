from typing import Iterable, Iterator, Union, Tuple
from typing_extensions import Protocol

from math import sqrt

from wisualia import core

class PointLike(Protocol):
    '''Any object that can be used as a point.

    There are currently 2 PointLike objects ``Tuple[float, float]`` and
    ``Point``.
    '''

    def __iter__(self) -> Iterator[float]:
        ...
    def __getitem__(self, key:int) -> float:
        ...

class Point(Iterable[float]):
    '''Point object'''
    def __init__(self,x:float,y:float) -> None:
        cr = core.context
        self._data = cr.user_to_device(x,y)
    def __iter__(self) -> Iterator[float]:
        cr = core.context
        return iter(cr.device_to_user(*self._data))
    def __getitem__(self, key:int) -> float:
        cr = core.context
        return cr.device_to_user(*self._data)[key] #type: ignore
    @property
    def x(self) -> float:
        return self[0]
    @property
    def y(self) -> float:
        return self[1]
    def __repr__(self) -> str:
        return 'Point({}, {})'.format(self[0], self[1])
    def distance(self, other:PointLike) -> float:
        return sqrt((self[0]-other[0])**2 + (self[1]-other[1])**2)
