import os
import json
import urllib.parse
import pymongo
from bson import ObjectId
from bson.objectid import ObjectId
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


@app.get('/api/category/{category}')
async def get_all_by_category(category: str):
    issues = list(db.issues.find({'category': {category}}))
    return json.dumps(issues, default=json_serial)


   
@app.post("/id")
async def delete_issue(request: Request):

    # issues = list(db.issues.find({'category': 'zemer'}))
    # get_issue_id = json.dumps(issues[0]["_id"] , default=json_serial)


    # get_id = ObjectId(request.params)
    return request.params



# router.put("/", async (req, res) => {
#   const issue = new Issue(req.body);

#   try {
#     const newIssue = await issue.save();
#     res.status(201).json(newIssue);
#   } catch (error) {
#     res.status(400).json({ error: error.message });
#   }
# });






