"""Data types for the data producers"""

from datetime import datetime, timedelta

role_types = {
    "AGENT": 1,
    "USER": 2,
    "GUEST": 3,
    "ADMIN": 4
}


class UserRole:
    def __init__(self, name: str) -> None:
        self.name = name


class User:
    def __init__(self, role: UserRole, givenName: str, familyName: str, username: str, email: str, password: str, phone: str) -> None:
        self.role = role
        self.givenName = givenName
        self.familyName = familyName
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone


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
    def __init__(self, isActive: bool, confirmationCode: str) -> None:
        self.isActive = isActive
        self.confirmationCode = confirmationCode


class BookingAgent:
    def __init__(self, booking: Booking, agent: User) -> None:
        self.booking = booking
        self.agent = agent


class BookingGuest:
    def __init__(self, booking: Booking, email: str, phone: str) -> None:
        self.booking = booking
        self.email = email
        self.phone = phone


class BookingPayment:
    def __init__(self, booking: Booking, stripeId: str, refunded: bool) -> None:
        self.booking = booking
        self.stripeId = stripeId
        self.refunded = refunded


class BookingUser:
    def __init__(self, booking: Booking, user: User) -> None:
        self.booking = booking
        self.user = user


class FlightBookings:
    def __init__(self, flight: Flight, booking: Booking) -> None:
        self.flight = flight
        self.booking = booking


class Passenger:
    def __init__(self, booking: Booking, givenName: str, familyName: str, dateOfBirth: datetime, gender: str, address: str) -> None:
        self.booking = booking
        self.givenName = givenName
        self.familyName = familyName
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.address = address
