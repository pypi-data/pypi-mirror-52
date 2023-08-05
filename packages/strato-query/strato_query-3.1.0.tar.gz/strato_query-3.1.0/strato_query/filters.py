"""
StratoDem Analytics : filters
Principal Author(s) : Eric Linden, Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

import abc
from typing import List, Union, Optional


__all__ = [
    'BaseFilter',
    'BetweenFilter',
    'EqualToFilter',
    'InFilter',
    'GreaterThanFilter',
    'LessThanFilter',
    'GreaterThanOrEqualToFilter',
    'LessThanOrEqualToFilter',
    'NotEqualToFilter',
    'NotInFilter',
    'DrivetimeFilter',
    'MileRadiusFilter',
    'IntersectsFilter',
    'OverlapsMileRadiusFilter',
    'OverlapsDrivetimeFilter',
    'OverlapsWalktimeFilter',
]


class BaseFilter(abc.ABC):
    def __init__(self, filter_type: str, filter_value, filter_variable: str):
        self._filter_type = filter_type
        self._filter_value = filter_value
        self._filter_variable = filter_variable

    def to_dict(self) -> dict:
        return dict(
            filter_type=self._filter_type,
            filter_value=self._filter_value,
            filter_variable=self._filter_variable)


class EqualToFilter(BaseFilter):
    """Construct a filter that generates var = val comparisons"""
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='eq',
                         filter_value=val,
                         filter_variable=var)


class BetweenFilter(BaseFilter):
    def __init__(self, var: str, val: List[Union[float, int]]):
        super().__init__(filter_type='between',
                         filter_value=val,
                         filter_variable=var)


class InFilter(BaseFilter):
    def __init__(self, var: str, val: List[Union[float, int, str]]):
        if val is None or len(val) < 1:
            raise ValueError('InFilter does not accept an empty list, nor a None value. \n'
                             'var: {}, val: {}'.format(var, val))
        super().__init__(filter_type='in',
                         filter_value=val,
                         filter_variable=var)


class GreaterThanFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='gt',
                         filter_value=val,
                         filter_variable=var)


class LessThanFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='lt',
                         filter_value=val,
                         filter_variable=var)


class GreaterThanOrEqualToFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='ge',
                         filter_value=val,
                         filter_variable=var)


class LessThanOrEqualToFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='le',
                         filter_value=val,
                         filter_variable=var)


class NotEqualToFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='ne',
                         filter_value=val,
                         filter_variable=var)


class NotInFilter(BaseFilter):
    def __init__(self, var: str, val: List[Union[float, int, str]]):
        if val is None or len(val) < 1:
            raise ValueError('NotInFilter does not accept an empty list, nor a None value. \n'
                             'var: {}, val: {}'.format(var, val))
        super().__init__(filter_type='nin',
                         filter_value=val,
                         filter_variable=var)


class MileRadiusFilter(BaseFilter):
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 miles: Union[int, float],
                 detailed_type: str = 'mile_radius'):
        """
        Filter a query to geographies contained by the drive time area

        Parameters
        ----------
        latitude: float
            Center latitude
        longitude: float
            Center longitude
        miles: int or float
            Miles from latitude-longitude center
        detailed_type: str
            One of:
            - 'mile_radius': use a normal mile radius, which weights results
            - 'mile_radius_simple': use a mile radius with weights, but using simplified shapes
            - 'mile_radius_unweighted': return unweighted results (used to get all geographies
                intersecting at all with the mile radius buffer)
        """
        assert detailed_type in {'mile_radius', 'mile_radius_simple', 'mile_radius_unweighted'}

        super().__init__(
            filter_type=detailed_type,
            filter_variable='',
            filter_value=dict(latitude=latitude, longitude=longitude, miles=miles))


class DrivetimeFilter(BaseFilter):
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 minutes: Union[int, float],
                 detailed_type: str = 'drivetime',
                 with_traffic: bool = False,
                 start_time: Optional[str] = None):
        """
        Filter a query to geographies contained by the drive time area

        Parameters
        ----------
        latitude: float
            Center latitude
        longitude: float
            Center longitude
        minutes: int or float
            Minutes drive from latitude-longitude center
        detailed_type: str
            One of:
            - 'drivetime': use a normal drivetime, which weights results
            - 'drivetime_simple': use a drivetime with weights, but using simplified shapes
            - 'drivetime_unweighted': return unweighted results (used to get all geographies
                intersecting at all with the drive time area)
        with_traffic: bool
            Use traffic estimates to compute the drive time area?
        start_time: str
            The departure time for the drivetime, used in concert with "with_traffic" set to True
            e.g., "2019-05-25T18:00:00"
        """
        assert detailed_type in {'drivetime', 'drivetime_simple', 'drivetime_unweighted'}
        assert isinstance(with_traffic, bool)
        assert start_time is None or isinstance(start_time, str)

        super().__init__(
            filter_type=detailed_type,
            filter_variable='',
            filter_value=dict(
                latitude=latitude,
                longitude=longitude,
                minutes=minutes,
                traffic='enabled' if with_traffic else 'disabled',
                start_time=start_time))


class IntersectsFilter(BaseFilter):
    def __init__(self, var: str, val: dict):
        super().__init__(
            filter_type='intersects',
            filter_variable=var,
            filter_value=val)


class OverlapsMileRadiusFilter(BaseFilter):
    def __init__(self,
                 var: str,
                 latitude: float,
                 longitude: float,
                 miles: Union[int, float]):
        """
        Filter a query by geometries overlapping the point's surrounding buffer

        Parameters
        ----------
        var: str
            The name of the geometry column against which this filter will check
        latitude: float
        longitude: float
        miles: Union[int, float]
            The number of miles around the provided latitude and longitude point.
        """
        assert isinstance(var, str)
        assert isinstance(latitude, float)
        assert isinstance(longitude, float)
        assert miles is None or isinstance(miles, (int, float))

        super().__init__(
            filter_type='overlaps_mile_radius',
            filter_variable=var,
            filter_value=dict(
                latitude=latitude,
                longitude=longitude,
                miles=miles))


class OverlapsDrivetimeFilter(BaseFilter):
    def __init__(self,
                 var: str,
                 latitude: float,
                 longitude: float,
                 minutes: Union[int, float],
                 with_traffic: bool = False,
                 start_time: Optional[str] = None):
        """
        Filter a query by geometries overlapping the point's surrounding buffer

        Parameters
        ----------
        var: str
            The name of the geometry column against which this filter will check
        latitude: float
        longitude: float
        minutes: int or float
            Minutes drive from latitude-longitude center
        with_traffic: bool
            Use traffic estimates to compute the drive time area?
        start_time: str
            The departure time for the drivetime, used in concert with "with_traffic" set to True
            e.g., "2019-05-25T18:00:00"
        """
        assert isinstance(var, str)
        assert isinstance(latitude, float)
        assert isinstance(longitude, float)
        assert isinstance(minutes, (int, float))
        assert with_traffic is None or isinstance(with_traffic, bool)
        assert start_time is None or isinstance(start_time, str)

        super().__init__(
            filter_type='overlaps_drivetime',
            filter_variable=var,
            filter_value=dict(
                latitude=latitude,
                longitude=longitude,
                minutes=minutes,
                with_traffic='enabled' if with_traffic else 'disabled',
                start_time=start_time))


class OverlapsWalktimeFilter(BaseFilter):
    def __init__(self,
                 var: str,
                 latitude: float,
                 longitude: float,
                 minutes: Union[int, float]):
        """
        Filter a query by geometries overlapping the point's surrounding buffer

        Parameters
        ----------
        var: str
            The name of the geometry column against which this filter will check
        latitude: float
        longitude: float
        minutes: int or float
            Minutes walk from latitude-longitude center
        """
        assert isinstance(var, str)
        assert isinstance(latitude, float)
        assert isinstance(longitude, float)
        assert isinstance(minutes, (int, float))

        super().__init__(
            filter_type='overlaps_walktime',
            filter_variable=var,
            filter_value=dict(
                latitude=latitude,
                longitude=longitude,
                minutes=minutes))
