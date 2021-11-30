import argparse
import csv
import json
import random
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from http.client import responses

import requests
from faker import Faker
from requests.models import Response

from ProducerTypes import Airplane, AirplaneType, Airport, Flight, Route

fake = Faker()
headers = { 'Content-Type': 'application/json' }


# region: public functions# region: public functions
def get_auth(args):
    """Gets the authorization header to properly access the Rest APIs"""

    response = requests.post(
        args.host + "/login",
        data=json.dumps({
            "username" : "admin",
            "password" : "admin"
        })
    )

    print("Authorizing...")
    print(f"Status: {responses[response.status_code]}\n")
    print(f"Token: {response.headers['Authorization']}\n")

    headers["Authorization"] = response.headers["Authorization"]


def add_airplane_types(args: Namespace) -> None:
    """Adds Airplane types via the Rest APIs"""

    get_auth(args)

    with open(args.data_location + "plane_types.csv") as file:
        csv_file = csv.DictReader(file, delimiter=';')

        for row in csv_file:
            dict_val = dict(row)
            current_type = AirplaneType(dict_val["max_capacity"])

            post_response: Response = requests.post(
                args.host + "/airplane-types",
                data=json.dumps(current_type.__dict__),
                headers=headers
            )
            print("Post Status: " + responses[post_response.status_code])


def add_airplanes(args: Namespace) -> None:
    """Adds Airplanes via the Rest APIs"""

    get_auth(args)

    for _ in range(args.count):
        post_request: Response = requests.post(
            args.host + "/airplanes",
            data=json.dumps({ "airplaneType" : { "id" : args.type_id }}),
            headers=headers
        )

        print("Post Status: " + responses[post_request.status_code])
        if (post_request.status_code == 400):
            print("Error: Airplane type cannot be added because it doesn't exist.\nExiting...")
            exit(0)


def add_airports(args: Namespace) -> None:
    """Adds Airports via the Rest APIs"""

    get_auth(args)

    with open(args.data_location + "airports.csv") as file:
        csv_file = csv.DictReader(file, delimiter=';')

        for row in csv_file:
            dict_val = dict(row)

            current_airport = Airport(dict_val["iata_code"], dict_val["city"])
            response: Response = requests.get(
                args.host + "/airports/" + dict_val["iata_code"],
                headers=headers
            )

            print("Get response status: " + responses[response.status_code])
            if (response.status_code != 200):
                post_response: Response = requests.post(
                    args.host + "/airports",
                    data=json.dumps(current_airport.__dict__),
                    headers=headers
                )
                print("Post Status: " + responses[post_response.status_code])


def add_routes(args: Namespace) -> None:
    """Adds Routes via the Rest APIs"""

    get_auth(args)

    airports_list = requests.get(args.host + "/airports", headers=headers).json()

    for _ in range(args.count):
        origin = Airport(**(airports_list[random.randint(0, len(airports_list)) - 1]))
        destination = Airport(**(airports_list[random.randint(0, len(airports_list)) - 1]))

        route = Route(origin.__dict__, destination.__dict__)

        post_response: Response = requests.post(
            args.host + "/routes",
            data=json.dumps(route.__dict__),
            headers=headers
        )

        print("Get response status: " + responses[post_response.status_code])
        if (post_response.status_code == 200):
            print(post_response)


def add_flights(args: Namespace) -> None:
    """Adds Flights via the Rest APIs"""

    get_auth(args)

    # Puts all the airplane ids in a list
    aiplane_ids: list[int] = [x["id"] for x in requests.get(
        args.host + "/airplanes",
        headers=headers
    ).json()]

    if (len(aiplane_ids) < 1):
        print("Cannot create flights without airplanes!")
        exit(0)

    # Puts all the airplane routes in a list
    route_ids: list[int] = [x["id"] for x in requests.get(
        args.host + "/routes",
        headers=headers
    ).json()]

    if (len(route_ids) < 1):
        print("Cannot create flights without airplanes!")
        exit(0)

    # Cleans up the date to be of a proper format for Json
    current_date_time: str = args.departure_date \
        .replace(second=0, microsecond=0) \
        .strftime('%Y-%m-%dT%H:%M:%S.%f')

    for _ in range(args.count):
        # Gets random ids from the given list
        airplane_id = random.randint(1, len(aiplane_ids) - 1)
        route_id = random.randint(1, len(route_ids) - 1)

        flight: Flight = Flight(
            seatPrice = random.randint(100, 500),
            reservedSeats = 0,
            departureTime = current_date_time,
            airplane = { "id" : airplane_id },
            route = { "id" : route_id }
        )

        post_response: Response = requests.post(
            args.host + "/flights",
            headers=headers,
            data=json.dumps(flight.__dict__)
        )

        print("Post Status: " + responses[post_response.status_code])

# endregion


def main() -> None:
    parser = ArgumentParser(description='Creates an N number flights')
    parser.add_argument("--host", type=str, default="http://localhost:8081")
    subparsers = parser.add_subparsers()

    airplane_type_func = subparsers.add_parser("add-airplane-types", help="Adds airplane types from a csv file")
    airplane_type_func.add_argument("--data-location", type=str, default="../data/")
    airplane_type_func.set_defaults(func=add_airplane_types)

    airplane_func = subparsers.add_parser("add-airplanes", help="Adds airplanes of a certain type")
    airplane_func.add_argument("--count", type=int, default=1)
    airplane_func.add_argument("--type_id", type=int, default=1)
    airplane_func.set_defaults(func=add_airplanes)

    airport_func = subparsers.add_parser("add-airports", help="Adds airports from a csv file")
    airport_func.add_argument("--data-location", type=str, default="../data/")
    airport_func.set_defaults(func=add_airports)

    routes_func = subparsers.add_parser("add-routes", help="Creates random routes from an existing set of airports")
    routes_func.add_argument("--count", type=int, default=1)
    routes_func.set_defaults(func=add_routes)

    flight_func = subparsers.add_parser("add-flights", help="Creates random flights")
    flight_func.add_argument("--count", type=int, default=1)
    flight_func.add_argument("--departure-date", type=str, default=(datetime.now() + timedelta(7)))
    flight_func.set_defaults(func=add_flights)

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == "__main__":
    main()
