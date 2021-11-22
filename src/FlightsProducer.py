import json, requests, argparse, csv, random
from faker import Faker
from datetime import datetime, timedelta

from requests.models import Response
from ProducerTypes import Airplane, AirplaneType, Airport, Route, Flight
from argparse import Namespace, ArgumentParser

fake = Faker()
headers = { 'Content-Type': 'application/json' }


# region: public functions
def add_airplane_types(args: Namespace) -> None:
    """Adds Airplane types via the Rest APIs"""

    with open(args.data_location + "plane_types.csv") as file:
        csv_file = csv.DictReader(file, delimiter=';')

        for row in csv_file:
            dict_val = dict(row)
            current_type = AirplaneType(dict_val["max_capacity"])

            post_response = requests.post(
                args.host + "/airplane-types",
                data=json.dumps(current_type.__dict__),
                headers=headers
            )
            print("Post Status: " + str(post_response.status_code))


def add_airplanes(args: Namespace) -> None:
    """Adds Airplanes via the Rest APIs"""

    for _ in range(args.count):
        post_request = requests.post(
            args.host + "/airplanes",
            data=json.dumps({ "airplaneType" : { "id" : args.type_id }}),
            headers=headers
        )

        print("Post Status: " + str(post_request.status_code))
        if (post_request.status_code == 400):
            print("Error: Airplane type cannot be added because it doesn't exist.\nExiting...")
            exit(0)


def add_airports(args: Namespace) -> None:
    """Adds Airports via the Rest APIs"""

    with open(args.data_location + "airports.csv") as file:
        csv_file = csv.DictReader(file, delimiter=';')

        for row in csv_file:
            dict_val = dict(row)

            current_airport = Airport(dict_val["iata_code"], dict_val["city"])
            response = requests.get(
                args.host + "/airports/" + dict_val["iata_code"],
                headers=headers
            )

            if (response.status_code != 200):
                post_response = requests.post(
                    args.host + "/airports",
                    data=json.dumps(current_airport.__dict__),
                    headers=headers
                )
                print("Post Status: " + str(post_response.status_code))


def add_routes(args: Namespace) -> None:
    """Adds Routes via the Rest APIs"""

    airports_list = requests.get(args.host + "/airports", headers=headers).json()

    for airport_dict1 in airports_list:
        for _ in range(args.count):
            origin = Airport(**airport_dict1)
            destination = Airport(**(airports_list[random.randint(0, len(airports_list)) - 1]))

            route = Route(origin.__dict__, destination.__dict__)

            post_response = requests.post(
                args.host + "/routes",
                data=json.dumps(route.__dict__),
                headers=headers
            )

            if (post_response.status_code == 200):
                print(post_response)


def add_flights(args: Namespace) -> None:
    """Adds Flights via the Rest APIs"""

    # Puts all the airplane ids in a list
    aiplane_ids: list[int] = [x["id"] for x in requests.get(
        args.host + "/airplanes",
        headers=headers
    ).json()]

    # Puts all the airplane routes in a list
    route_ids: list[int] = [x["id"] for x in requests.get(
        args.host + "/routes",
        headers=headers
    ).json()]

    current_date_time = args.departure_date.replace(second=0, microsecond=0)

    print(aiplane_ids)
    print(route_ids)
    print(current_date_time)

    # flight1: Flight = Flight(
    #     seatPrice=0,
    #     reservedSeats=0,
    #     departureTime=datetime(2021, 11, 14, 12, 0, 0),
    #     airplane= {
    #         "id" : 0
    #     },
    #     route= {
    #         "id" : 0
    #     }
    # )

    """
    {
        "seatPrice" : 50,
        "reservedSeats" : 10,
        "departureTime" : "2021-11-14T12:00:00",
        "airplane" : {
            "id": 1
        },
        "route" : {
            "id": 1
        }
    }
    """

# endregion


def main() -> None:
    parser = ArgumentParser(description='Creates an N number flights')
    parser.add_argument("--host", type=str, default="http://localhost:8080")
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
    routes_func.add_argument("--count-per-route", type=int, default=1)
    routes_func.set_defaults(func=add_routes)

    flight_func = subparsers.add_parser("add-flights", help="Creates random flights")
    flight_func.add_argument("--departure-date", type=str, default=(datetime.now().replace(minute=0) + timedelta(7)))
    flight_func.add_argument("--count", type=int, default=1)
    flight_func.set_defaults(func=add_flights)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
