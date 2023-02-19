from fastapi import APIRouter, Request, HTTPException
from bson import ObjectId
from .. import utils
from .. import webhooks
import traceback

router = APIRouter(prefix="/api")


@router.get("/project/{project_id}")
async def get_project(project_id):
    db = utils.get_db_client()
    project = db.projects.find_one({"project_id": project_id})

    if project:
        return utils.json_ready(
            {
                **project,
                "webhooks": [i for i in db.webhooks.find({"project_id": project_id})],
            }
        )


# @app.put("/project")
# async def get_project(request: Request):
#     req_info = await request.json()

#     project = db.projects.find_one({"project_id": project_id})

#     if project:
#         return utils.json_ready(
#             {
#                 **project,
#                 "webhooks": [i for i in db.webhooks.find({"project_id": project_id})],
#             }
#         )


@router.get("/project/{project_id}/issues")
async def get_exact(project_id: str):
    db = utils.get_db_client()
    return utils.prepare_json(db.issues.find({"project_id": ObjectId(project_id)}))


@router.get("/project/{project_id}/category/{category}/issues")
async def get_all_by_category(project_id: str, category: str):
    db = utils.get_db_client()
    issues = list(
        db.issues.find({"project_id": ObjectId(project_id), "category": category})
    )
    return utils.prepare_json(issues)
