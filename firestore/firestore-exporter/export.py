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


def banner(text):
    banner = Figlet(font="5lineoblique")
    print(banner.renderText(text))


def get_auth_db_instance(creds_file):
    cred = credentials.Certificate(creds_file)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db


def main():
    banner("FirestoreExport")

    parser = argparse.ArgumentParser(
        description="Dataset exporter for Firestore collection"
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="The collection name to export eg. 'users'",
    )
    parser.add_argument(
        "--datafile",
        type=str,
        required=True,
        help="The absolute filepath to the CSV file to write the data eg. users.csv",
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

    docs = db.collection(args.collection).stream()

    with open(args.datafile, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for doc in docs:
            datum = f"{doc.id} => {doc.to_dict()}"
            csv_writer.writerow(datum.split(','))


if __name__ == "__main__":
    main()
