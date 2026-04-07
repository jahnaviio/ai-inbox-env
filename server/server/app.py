from fastapi import FastAPI
import uvicorn
from myenv.environment import InboxEnv
from myenv.models import Action

app = FastAPI()
env = InboxEnv()


@app.get("/")
def home():
    return {"message": "AI Inbox Env is running"}


@app.get("/reset")
@app.post("/reset")
async def reset():
    result = await env.reset()
    return result


@app.post("/step")
async def step(action: dict):
    act = Action(**action)
    result = await env.step(act)
    return result


# ✅ REQUIRED FOR OPENENV
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED
if __name__ == "__main__":
    main()
