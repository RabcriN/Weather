from typing import NamedTuple

import geocoder  # type: ignore

from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """Returns your coordinates based on IP"""
    myloc = geocoder.ip('me')
    latitude = longitude = None
    latitude = myloc.latlng[0]
    longitude = myloc.latlng[1]
    if longitude is None or latitude is None:
        raise CantGetCoordinates
    return Coordinates(latitude=latitude, longitude=longitude)


def get_ip():
    g = geocoder.ipinfo('me')
    return g.ip
