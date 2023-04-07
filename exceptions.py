class CantGetCoordinates(Exception):
    """Program can't get current coordinates"""


class ApiServiceError(Exception):
    """Program can't get current weather via API"""


class InputChoiceError(Exception):
    """Error in input data"""
