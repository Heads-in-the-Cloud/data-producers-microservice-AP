"""Data types for the data producers"""

from datetime import datetime, timedelta

class AirplaneType:
    def __init__(self, maxCapacity: int) -> None:
        self.maxCapacity = maxCapacity


class Airplane:
    def __init__(self, airplaneType: AirplaneType) -> None:
        self.airplaneType = airplaneType


class Airport:
    def __init__(self, iataID: str, cityName: str) -> None:
        self.iataID = iataID
        self.cityName = cityName


class Route:
    def __init__(self, origin: Airport, destination: Airport) -> None:
        self.origin = origin
        self.destination = destination


class Flight:
    def __init__(self, seatPrice: float, reservedSeats: int, departureTime: datetime, airplane: Airplane, route: Route) -> None:
        self.seatPrice = seatPrice
        self.reservedSeats = reservedSeats
        self.departureTime = departureTime
        self.airplane = airplane
        self.route = route


class Booking:
    def __init__(self) -> None:
        pass


class BookingAgent:
    def __init__(self) -> None:
        pass


class BookingGuest:
    def __init__(self) -> None:
        pass


class BookingPayment:
    def __init__(self) -> None:
        pass


class BookingUser:
    def __init__(self) -> None:
        pass


class FlightBookings:
    def __init__(self) -> None:
        pass


class Passenger:
    def __init__(self) -> None:
        pass