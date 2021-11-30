import argparse
import csv
import json
import random
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from distutils.util import strtobool
from http.client import responses

import requests
from faker import Faker
from requests.models import Response

from ProducerTypes import *

fake = Faker()
headers = { 'Content-Type': 'application/json' }


# region: public functions
def get_auth(args):
    """Gets the authorization header to properly access the Rest APIs"""

    response = requests.post(
        args.user_host + "/login",
        data=json.dumps({
            "username" : "admin",
            "password" : "admin"
        })
    )

    print("Authorizing...")
    print(f"Status: {responses[response.status_code]}\n")
    print(f"Token: {response.headers['Authorization']}\n")

    headers["Authorization"] = response.headers["Authorization"]


def add_bookings(args: Namespace) -> None:
    """Adds bookings via the Rest APIs"""

    get_auth(args)

    for _ in range(args.count):
        confirmation_code = str(random.randrange(10 ** 5, 10 ** 6))
        booking: Booking = Booking(args.is_active, confirmation_code)

        post_request: Response = requests.post(
            args.booking_host + "/bookings",
            data=json.dumps(booking.__dict__),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])
        if (post_request.status_code == 400):
            exit(0)


def add_agents(args: Namespace) -> None:
    """Adds agents via the Rest APIs"""

    get_auth(args)

    # Gets all the bookings using a list comprehesion while discarding the id field
    bookings: list[int] = [list(x.values())[0]
        for x in requests.get(args.booking_host + "/bookings", headers=headers)
            .json()]

    # Gets all the users using a list comprehesion while discarding the id field
    users: list[int] = [list(x.values())[0]
        for x in requests.get(args.user_host + "/users/all", headers=headers)
            .json() if x["role"]["id"] == role_types["AGENT"]]

    for _ in range(args.count):
        booking: int = bookings[random.randint(0, len(bookings) - 1)]
        user: int = users[random.randint(0, len(users) - 1)]

        agent: BookingAgent = BookingAgent(booking, user)

        post_request: Response = requests.post(
            args.booking_host + "/booking-agents",
            data=json.dumps(agent.__dict__),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])



def add_guests(args: Namespace) -> None:
    """Adds guests via the Rest APIs"""

    get_auth(args)

    # Gets all the bookings using a list comprehesion while discarding the id field
    bookings: list[int] = [list(x.values())[0]
        for x in requests.get(args.booking_host + "/bookings", headers=headers)
            .json()]

    for _ in range(args.count):
        booking: int = bookings[random.randint(0, len(bookings) - 1)]
        email: int = fake.email()
        phone: int = fake.phone_number()

        guest: BookingGuest = BookingGuest(booking, email, phone)

        post_request: Response = requests.post(
            f"{args.booking_host}/booking-guests",
            data=json.dumps(guest.__dict__),
            headers=headers
        )

        print("Post Status: " + str(post_request.status_code) + "-" + responses[post_request.status_code])


def add_users(args: Namespace) -> None:
    """Adds users via the Rest APIs"""

    get_auth(args)

    # Gets all the bookings using a list comprehesion while discarding the id field
    bookings: list[int] = [list(x.values())[0]
        for x in requests.get(args.booking_host + "/bookings", headers=headers)
            .json()]

    # Gets all the users using a list comprehesion while discarding the id field
    users: list[int] = [list(x.values())[0]
        for x in requests.get(args.user_host + "/users/all", headers=headers)
            .json() if x["role"]["id"] == role_types["USER"]]

    for _ in range(args.count):
        booking: int = bookings[random.randint(0, len(bookings) - 1)]
        user: int = users[random.randint(0, len(users) - 1)]

        booking_user: BookingUser = BookingUser(booking, user)

        post_request: Response = requests.post(
            args.booking_host + "/booking-users",
            data=json.dumps(booking_user.__dict__),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])


def add_payments(args: Namespace) -> None:
    """Adds payments via the Rest APIs"""

    get_auth(args)

    # Gets all the bookings using a list comprehesion while discarding the id field
    bookings: list[int] = [list(x.values())[0]
        for x in requests.get(args.booking_host + "/bookings", headers=headers)
            .json()]

    for _ in range(args.count):
        booking: int = bookings[random.randint(0, len(bookings) - 1)]
        stripe_id = fake.credit_card_number()
        refunded: bool = False

        payment: BookingPayment = BookingPayment(booking, stripe_id, refunded)

        post_request: Response = requests.post(
            args.booking_host + "/booking-payments",
            data=json.dumps(payment.__dict__),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])


def add_passengers(args: Namespace) -> None:
    """Adds passengers via the Rest APIs"""

    get_auth(args)

    # Gets all the bookings using a list comprehesion while discarding the id field
    bookings: list[int] = [list(x.values())[0]
        for x in requests.get(args.booking_host + "/bookings", headers=headers)
            .json()]

    for _ in range(args.count):
        booking = {
            "id": bookings[random.randint(0, len(bookings) - 1)]
        }

        given_name = fake.first_name()
        family_name = fake.last_name()
        gender = random.choice(["Male", "Female", "Other"])
        address = fake.street_address() + " " + fake.postcode()
        dob = fake.date_of_birth(minimum_age=12).strftime("%Y-%m-%d")

        passenger: Passenger = Passenger(booking, given_name, family_name, dob, gender, address)

        post_request: Response = requests.post(
            args.booking_host + "/passengers",
            data=json.dumps(passenger.__dict__),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])


def add_flight_bookings(args: Namespace) -> None:
    """Adds flight bookigns via the Rest APIs"""

    get_auth(args)

    # Gets all the bookings using a list comprehesion while discarding the id field
    bookings: list[int] = [list(x.values())[0]
        for x in requests.get(args.booking_host + "/bookings", headers=headers)
            .json()]

    flights: list[int] = [list(x.values())[0]
    for x in requests.get(args.flight_host + "/flights", headers=headers)
        .json()]

    for _ in range(args.count):
        booking: int = bookings[random.randint(0, len(bookings) - 1)]
        flight: int = flights[random.randint(0, len(flights) - 1)]

        flight_bookings: FlightBookings = FlightBookings(flight, booking)

        post_request: Response = requests.post(
            args.booking_host + "/flight-bookings",
            data=json.dumps(flight_bookings.__dict__),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])
# endregion


def main() -> None:
    parser = ArgumentParser(description='Creates an N number of bookings')
    parser.add_argument("--user-host", type=str, default="http://localhost:8080")
    parser.add_argument("--flight-host", type=str, default="http://localhost:8081")
    parser.add_argument("--booking-host", type=str, default="http://localhost:8082")
    subparsers = parser.add_subparsers()

    bookings_func = subparsers.add_parser("add-bookings", help="Adds bookings of a certain type")
    bookings_func.add_argument("--count", type=int, default=1)
    bookings_func.add_argument("--is_active", type=lambda x:bool(strtobool(x)), default=True)
    bookings_func.set_defaults(func=add_bookings)

    agents_func = subparsers.add_parser("add-agents", help="Adds agents of a certain type")
    agents_func.add_argument("--count", type=int, default=1)
    agents_func.set_defaults(func=add_agents)

    guests_func = subparsers.add_parser("add-guests", help="Adds guests of a certain type")
    guests_func.add_argument("--count", type=int, default=1)
    guests_func.set_defaults(func=add_guests)

    users_func = subparsers.add_parser("add-users", help="Adds users of a certain type")
    users_func.add_argument("--count", type=int, default=1)
    users_func.set_defaults(func=add_users)

    payments_func = subparsers.add_parser("add-payments", help="Adds payments of a certain type")
    payments_func.add_argument("--count", type=int, default=1)
    payments_func.set_defaults(func=add_payments)

    passengers_func = subparsers.add_parser("add-passengers", help="Adds passengers of a certain type")
    passengers_func.add_argument("--count", type=int, default=1)
    passengers_func.set_defaults(func=add_passengers)

    flight_bookings_func = subparsers.add_parser("add-flight-bookings", help="Adds flight bookings of a certain type")
    flight_bookings_func.add_argument("--count", type=int, default=1)
    flight_bookings_func.set_defaults(func=add_flight_bookings)

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == "__main__":
    main()