from fastapi import FastAPI
from pydantic import BaseModel
from myenv.environment import InboxEnv
from myenv.models import Action

app = FastAPI()

env = InboxEnv()


@app.get("/")
def home():
    return {"message": "AI Inbox Env is running"}


@app.get("/reset")
async def reset():
    result = await env.reset()
    return result


class ActionInput(BaseModel):
    action_type: str
    label: str = None
    response_text: str = None


@app.post("/step")
async def step(action: ActionInput):
    action_obj = Action(**action.dict())
    result = await env.step(action_obj)
    return result
