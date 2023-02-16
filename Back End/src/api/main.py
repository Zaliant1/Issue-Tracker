import os
import json
import urllib.parse
import pymongo
import discord
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from urllib.parse import quote_plus
import json

from ..bot.main import category as bot_category
from ..bot import main as bot
from . import webhooks
from . import utils

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


@app.get("/bot-test")
async def root():
    return


@app.post('/api/issue/findexact')
async def get_exact(request: Request):
    req_info = await request.json()
    if req_info.get('_id'):
        del req_info['_id']

    return utils.prepare_json(db.issues.find_one(req_info))

@app.get('/api/issue/{issue_id}')
async def get_exact(issue_id):
    return utils.prepare_json(db.issues.find_one({'_id' : ObjectId(issue_id)}))



@app.get('/api/issue/category/{category}')
async def get_all_by_category(category: str):
    issues = list(db.issues.find({'category': category}))
    return utils.prepare_json(issues)


@app.post('/api/issue/{issue_id}')
async def update_issue(issue_id, request: Request):
    req_info = await request.json()

    issue_id = ObjectId(issue_id)
    req_info.pop('_id')

    issue = db.issues.find_one_and_update({'_id': issue_id}, {"$set": req_info}, upsert=False)

    diff = []

    for key, value in req_info.items():
        if value == issue[key]:
            continue

        diff.append({"new": value, "old": issue[key], "key": key})

    webhooks.send_update_issue(diff)

    return utils.prepare_json(issue)


@app.put('/api/issue')
async def create_issue(request: Request):
    req_info = await request.json()
    issue = db.issues.insert_one(req_info)
   
    webhooks.send_new_issue(req_info)

    return utils.json_ready(issue.inserted_id)



@app.delete("/api/issue/{issue_id}")
async def delete_issue(issue_id):
    db.issues.find_one_and_delete({'_id': ObjectId(issue_id)})