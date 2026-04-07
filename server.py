from fastapi import FastAPI
from myenv.environment import InboxEnv
from myenv.models import Action

app = FastAPI()

env = InboxEnv()


@app.get("/")
def home():
    return {"message": "AI Inbox Env is running"}


# ✅ RESET (GET + POST both supported)
@app.get("/reset")
@app.post("/reset")
async def reset():
    result = await env.reset()
    return result


# ✅ STEP (POST only)
@app.post("/step")
async def step(action: dict):
    act = Action(**action)
    result = await env.step(act)
    return result
