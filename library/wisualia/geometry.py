from typing import Iterable, Iterator, Union, Tuple
from wisualia import core
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

PointLike = Union[Tuple[float,float], Point]
'''Pointlike is either Point or tuple of floats'''
