import argparse
import json
from http.client import responses

import requests
from faker import Faker

from ProducerTypes import role_types

fake = Faker()
headers = {'Content-Type': 'application/json'}


# region: public functions
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


def verify_roles_exist(hostname="http://localhost:8080"):
    print("Verifying Roles Exists:")
    for role in role_types:
        request = requests.get(
            hostname + "/user-roles/" + str(role_types[role]))

        print(f"\t{role}, status: {responses[request.status_code]}")

        if (request.status_code != 200):
            print("Since the role was not found, making new role!")
            postReq = requests.post(
                hostname + "/user-roles", data=json.dumps({'name': role}), headers=headers)
            print(postReq.text)
# endregion


def main():
    parser = argparse.ArgumentParser(
        description='Creates an N number of random users.')
    parser.add_argument("userscount", type=int)
    parser.add_argument("--host", type=str, default="http://localhost:8080")
    parser.add_argument("--usertype", type=str,
                        choices=role_types.keys(), default="AGENT")
    args = parser.parse_args()

    get_auth(args)
    verify_roles_exist(args.host)

    for _ in range(args.userscount):
        user = json.dumps({
            "role": {"id": role_types[args.usertype]},
            "givenName": fake.first_name(),
            "familyName": fake.last_name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
            "phone": fake.phone_number()
        })

        response = requests.post(args.host + "/users",
                                 data=user, headers=headers)
        print(f"Created new user -> status: {responses[response.status_code]}")
        print(f"Username: {json.loads(user)['username']}\nPassword: {json.loads(user)['password']}\n")


if __name__ == "__main__":
    main()
