#!/bin/bash

USERS_HOST="http://localhost:8080"
FLIGHTS_HOST="http://localhost:8081"
BOOKINGS_HOST="http://localhost:8082"

HOST_ARGS="--user-host $USERS_HOST --flight-host $FLIGHTS_HOST --booking-host $BOOKINGS_HOST"

# Intialize Users:
python UsersProducer.py --host $USERS_HOST --usertype ADMIN 1
python UsersProducer.py --host $USERS_HOST --usertype AGENT 5
python UsersProducer.py --host $USERS_HOST --usertype USER 10
python UsersProducer.py --host $USERS_HOST --usertype GUEST 20

# Initialize Flight Information
python FlightsProducer.py --host $FLIGHTS_HOST add-airports
python FlightsProducer.py --host $FLIGHTS_HOST add-airplane-types
python FlightsProducer.py --host $FLIGHTS_HOST add-airplanes --count 1 --type_id 0
python FlightsProducer.py --host $FLIGHTS_HOST add-airplanes --count 5 --type_id 1
python FlightsProducer.py --host $FLIGHTS_HOST add-airplanes --count 10 --type_id 2
python FlightsProducer.py --host $FLIGHTS_HOST add-airplanes --count 15 --type_id 3
python FlightsProducer.py --host $FLIGHTS_HOST add-airplanes --count 20 --type_id 4
python FlightsProducer.py --host $FLIGHTS_HOST add-routes --count 50
python FlightsProducer.py --host $FLIGHTS_HOST add-flights --count 20

# Initialize Booking Information
python BookingsProducer.py $HOST_ARGS add-bookings --count 25 --is_active true
python BookingsProducer.py $HOST_ARGS add-bookings --count 25 --is_active false
python BookingsProducer.py $HOST_ARGS add-agents --count 25
python BookingsProducer.py $HOST_ARGS add-users --count 10
python BookingsProducer.py $HOST_ARGS add-guests --count 20
python BookingsProducer.py $HOST_ARGS add-payments --count 30
python BookingsProducer.py $HOST_ARGS add-passengers --count 10
python BookingsProducer.py $HOST_ARGS add-flight-bookings --count 5