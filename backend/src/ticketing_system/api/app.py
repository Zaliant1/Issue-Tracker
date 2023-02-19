from bson import ObjectId
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from .routes import issue, project

app = FastAPI()
app.include_router(issue.router)
app.include_router(project.router)


@app.get("/")
async def root():
    return "asdf"
