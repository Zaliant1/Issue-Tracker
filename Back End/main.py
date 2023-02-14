import os
import json
import urllib.parse
import pymongo
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from urllib.parse import quote_plus
import json



load_dotenv()

USERNAME = urllib.parse.quote_plus(os.getenv('USERNAME'))
PASSWORD = urllib.parse.quote_plus(os.getenv('PASSWORD'))
URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.81uebtg.mongodb.net/?retryWrites=true&w=majority"


client = pymongo.MongoClient(URI)

app = FastAPI()
db = client.test

def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)

    return obj



@app.get("/")
async def root():
    return "asdf"


@app.get('/findexact')
async def get_exact(request: Request):
    req_info = await request.json()
    issue_id = ObjectId(req_info['_id']["$oid"])

    issues = list(db.issues.find({'_id' : issue_id}))
    return json.dumps(issues, default=json_serial)



@app.get('/api/category/{category}')
async def get_all_by_category(category: str):
    issues = list(db.issues.find({'category': {category}}))
    return json.dumps(issues, default=json_serial)


@app.post('/')
async def update_issue(request: Request):
    req_info = await request.json()

    issue_id = ObjectId(req_info['_id']["$oid"])
    req_info.pop('_id')

    db.issues.find_one_and_update({'_id': issue_id}, {"$set": req_info}, upsert=False)

    issues = list(db.issues.find({'_id' : issue_id}))
    return json.dumps(issues, default=json_serial)


@app.put('/')
async def create_issue(request: Request):
    req_info = await request.json()
    db.issues.insert_one(req_info)
    search_query = {k:v for k,v in req_info.items()}
   
   
    issues = list(db.issues.find(search_query))

    return json.dumps(issues, default=json_serial)



@app.delete("/")
async def delete_issue(request: Request):
   req_info = await request.json()
   issue_id = ObjectId(req_info)
   db.issues.find_one_and_delete({'_id': issue_id})