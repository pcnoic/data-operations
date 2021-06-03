import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
import random
import time
import requests
import json
import calendar
from pyfiglet import Figlet
import argparse

RANDOM_USER_API = "https://randomuser.me/api"


def banner(text):
    banner = Figlet(font="5lineoblique")
    print(banner.renderText(text))


def get_auth_db_instance(creds_file):
    cred = credentials.Certificate(creds_file)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db


def fetch_username():
    randomUsernameApi = RANDOM_USER_API
    r = requests.get(randomUsernameApi)
    r.raise_for_status()

    json_response = r.json()
    results = json_response["results"]
    results = results[0]
    name = results["name"]
    first = name["first"]
    last = name["last"]

    return first + " " + last


def main():
    banner("FirestoreImport")

    parser = argparse.ArgumentParser(
        description="Dataset importer for Firestore collection"
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="The collection name to import eg. 'users'",
    )
    parser.add_argument(
        "--datafile",
        type=str,
        required=True,
        help="The absolute filepath to the file containing the data to import.",
    )
    parser.add_argument(
        "--credentials",
        type=str,
        required=True,
        help="The absolute filepath to the .json file containing the service account to be used for authentication",
    )
    args = parser.parse_args()

    # Fetch authenticated database instance
    db = get_auth_db_instance(args.credentials)

    with open(args.datafile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            doc_ref = db.collection(args.collection).document()
            doc_ref.set(
                {
                    "content": "".join(row),
                    "date": firestore.SERVER_TIMESTAMP,
                    "created_by": fetch_username(),
                    "likedCounter": random.randint(1, 30),
                }
            )
            
if __name__ == "__main__":
    main()
