from bson import ObjectId
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from . import webhooks
from .routes import issue, project, user

app = FastAPI()
app.include_router(issue.router)
app.include_router(project.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return "asdf"


@app.get("/modding-help")
async def modding_help_send():
    return webhooks.modding_help()


@app.post("api/auth/")
async def get_auth_info(request: Request):
    req_info = await request.json()
    print(req_info)
