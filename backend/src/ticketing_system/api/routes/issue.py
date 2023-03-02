from fastapi import APIRouter, Request, HTTPException
from bson import ObjectId
from .. import utils
from .. import webhooks
import traceback

router = APIRouter(prefix="/api")
db = utils.get_db_client()


@router.get("/issue/{issue_id}")
async def get_one(issue_id):
    return utils.prepare_json(db.issues.find_one({"_id": ObjectId(issue_id)}))


@router.post("/issue/findexact")
async def get_exact(request: Request):
    req_info = await request.json()
    if req_info.get("_id"):
        del req_info["_id"]

    return utils.prepare_json(db.issues.find_one(req_info))


@router.post("/issue/{issue_id}")
async def update_issue(issue_id, request: Request):
    req_info = await request.json()

    issue_id = ObjectId(issue_id)
    req_info.pop("_id")

    issue = db.issues.find_one_and_update(
        {"_id": issue_id}, {"$set": req_info}, upsert=False
    )

    diff = []

    for key, value in req_info.items():
        if value == issue[key]:
            continue

        diff.append({"new": value, "old": issue[key], "key": key})

    webhooks.send_update_issue(diff, issue_id)

    return utils.prepare_json(issue)


@router.put("/issue")
async def create_issue(request: Request):
    req_info = await request.json()

    # TODO: check to see if user_id is allowed to create this issue on the project_name

    try:
        issue = db.issues.insert_one(req_info)
    except:
        print(traceback.format_exc())
        raise HTTPException(status_code=503, detail="Unable write issue to database")

    webhooks.send_new_issue(req_info)
    return utils.json_ready(issue.inserted_id)


@router.delete("/issue/{issue_id}")
async def delete_issue(issue_id):
    issue = db.issues.find_one({"_id": ObjectId(issue_id)})
    db.issues.find_one_and_delete({"_id": ObjectId(issue_id)})
    webhooks.send_deleted_issue(issue)
