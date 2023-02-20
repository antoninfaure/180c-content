import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from os import path
from collections import Counter
import json
from utils import check_place

load_dotenv()

client = MongoClient(f"mongodb+srv://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_URL']}/?retryWrites=true&w=majority")

db = client[os.environ['DB_NAME']]


def print_err(msg):
    print('\033[91m' + msg + '\033[0m')

def print_ignore(msg):
    print('\033[93m' + msg + '\033[0m')

# First query all available places of DB
all_places_codes = list(map(lambda x: x['code'], db.places.find({ 'available' : True})))

# List all folders names in folder crieur
crieur_places_folders = Counter(list(filter(lambda x: path.isdir(path.join('.', 'crieur', x)), os.listdir('crieur'))))

added_places_codes = []
for place_code, k in crieur_places_folders.items():
    # If folders duplicates
    if (k > 1):
        print_err(f'[{place_code}] error: duplicates folders, solution: skipped')
        continue

    # If no place.json file
    place_path = path.join('.', 'crieur', place_code, 'place.json')
    if (not path.exists(place_path)):
        print_err(f'[{place_code}] error: no place.json file, solution: skipped')
        continue
    
    try:
        f = open(place_path, "r", encoding='utf8')
    except OSError:
        print_err(f'[{place_code}] error: could not open file {place_path}, solution: skipped')
        continue
    
    with f:
        place_json = json.load(f)
        f.close()
        try:
            place = check_place(place_code, place_json)
            db.places.replace_one({ 'code' : place_code }, place, upsert=True)
            added_places_codes.append(place_code)
        except Exception as e:
            print_err(f'[{place_code}] error: {e}, solution: skipped ')
            continue


places_to_unavailable = list(filter(lambda x: x not in added_places_codes, all_places_codes))

if (len(places_to_unavailable) > 0):
    db.places.update_many({ 'code' : { '$in' : places_to_unavailable } }, { '$set' : { 'available': False }})
    print(f'Made unavailable : {places_to_unavailable}')

