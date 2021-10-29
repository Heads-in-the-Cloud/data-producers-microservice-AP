import json
from faker import Faker
import requests, argparse

fake = Faker()
headers = { 'Content-Type': 'application/json' }

role_types = {
    "AGENT" : 0,
    "USER"  : 1,
    "GUEST" : 2,
    "ADMIN" : 3
}

def verify_roles_exist(hostname="http://localhost:8080"):
    print("Verifying Roles Exists:")
    for role in role_types:
        request = requests.get(hostname + "/user-roles/" + str(role_types[role]))

        print("\t" + role + ", status: " + str(request.status_code))

        if (request.status_code != 200):
            print("Since the role was not found, making new role!")
            postReq = requests.post(hostname + "/user-roles", data= json.dumps({ 'name' : role }), headers=headers)
            print(postReq.text)

def main():
    parser = argparse.ArgumentParser(description='Creates an N number of random users.')
    parser.add_argument("userscount", type=int)
    parser.add_argument("--host", type=str, default="http://localhost:8080")
    parser.add_argument("--usertype", type=str, choices=role_types.keys(), default="AGENT")
    args = parser.parse_args()

    verify_roles_exist(args.host)

    for _ in range(args.userscount):
        user = json.dumps({
            "role" : { "id" : role_types[args.usertype] },
            "givenName" : fake.first_name(),
            "familyName" : fake.last_name(),
            "username" : fake.user_name(),
            "email" : fake.email(),
            "password" : fake.password(),
            "phone" : fake.phone_number()
        })

        response = requests.post(args.host + "/users", data=user, headers=headers)
        print("Created new user -> status: " + str(response.status_code))

if __name__ == "__main__":
    main()
