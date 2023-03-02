import os
import pymongo
from dotenv import load_dotenv
from bson import ObjectId
from urllib.parse import quote_plus

load_dotenv()


def alphanumeric_check(data):
    if data.replace(" ", "").isalnum():
        data.replace(" ", "-")
    else:
        return False


def json_ready(data):
    if isinstance(data, ObjectId):
        return str(data)
    # elif instance(data, datetime.datetime):
    #     return str(data)
    else:
        return data


def prepare_json(data):
    if isinstance(data, dict):
        output = {}
        for key, value in data.items():
            if (
                isinstance(value, dict)
                or isinstance(value, list)
                or isinstance(value, set)
            ):
                output[key] = prepare_json(value)
            else:
                output[key] = json_ready(value)

        return output

    elif isinstance(data, list) or isinstance(data, set):
        output = []
        for value in data:
            if (
                isinstance(value, dict)
                or isinstance(value, list)
                or isinstance(value, set)
            ):
                output.append(prepare_json(value))
            else:
                output.append(json_ready(value))

        return output
    else:
        return json_ready(data)


def get_db_client(db="test"):
    USERNAME = quote_plus(os.getenv("USERNAME"))
    PASSWORD = quote_plus(os.getenv("PASSWORD"))
    URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.81uebtg.mongodb.net/?retryWrites=true&w=majority"

    return pymongo.MongoClient(URI)[db]
