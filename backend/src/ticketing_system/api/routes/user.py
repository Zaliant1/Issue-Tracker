from fastapi import APIRouter, Request, HTTPException
from bson import ObjectId
from .. import utils
from .. import webhooks
import traceback
import time

router = APIRouter(prefix="/api")
db = utils.get_db_client()


@router.put("/user/create")
async def get_project(request: Request):
    req_info = await request.json()
    find_user = db.users.find_one({"user_id": req_info["user_id"]})
    print(req_info)

    if not find_user:
        print("didnt find the user")
        db.users.insert_one(req_info)

    elif find_user and not db.users.find_one(
        {"user_id": req_info["user_id"], "projects": req_info["projects"]}
    ):
        db.projects.update_one(
            {"user_id": req_info["user_id"]},
            {"$push": {"projects": req_info["projects"]}},
        )
        print("found user but didn't find the project, so we update with the project")

    elif find_user and db.users.find_one(
        {"user_id": req_info["user_id"], "projects": req_info["projects"]}
    ):
        print(
            "found the user and it's a part of the project we are looking for, so we reject"
        )

    else:
        raise HTTPException(
            status_code=503,
            detail=f"Unable write webhook for channel to database",
        )
