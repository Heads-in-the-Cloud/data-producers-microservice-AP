import json
from faker import Faker
import requests, argparse

AGENT = 0
USER  = 1
GUEST = 2
ADMIN = 3

fake = Faker()

def main():
    parser = argparse.ArgumentParser(description='Creates an N number of random users.')
    parser.add_argument("userscount", type=int)
    parser.add_argument("--host", type=str, default="http://localhost:8080")
    parser.add_argument("--usertype", type=int, default=AGENT)
    args = parser.parse_args()

    headers = {
        'Content-Type': 'application/json'
    }

    for i in range(args.userscount):
        user = json.dumps({
            "role" : {
                "id" : args.usertype
            },
            "givenName" : fake.first_name(),
            "familyName" : fake.last_name(),
            "username" : fake.user_name(),
            "email" : fake.email(),
            "password" : fake.password(),
            "phone" : fake.phone_number()
        })

        response = requests.post(args.host + "/users", data=user, headers=headers)
        print(response)

if __name__ == "__main__":
    main()
