import asyncio
import os
from typing import List, Optional
from openai import OpenAI

from myenv.environment import InboxEnv
from myenv.models import Action

# ENV
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

TASK_NAME = "easy"
BENCHMARK = "ai_inbox_env"

MAX_STEPS = 5
SUCCESS_THRESHOLD = 0.5

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

# ---------- LOG ----------
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}",
        flush=True
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True
    )

# ---------- SAFE OBS ACCESS ----------
def get_obs_fields(obs):
    try:
        return obs["subject"], obs["body"]
    except:
        return "", ""

# ---------- LLM ----------
def decide_action_llm(subject: str, body: str) -> Action:
    prompt = f"""
    Classify this email into one of:
    spam, important, personal

    Subject: {subject}
    Body: {body}

    Only return one word.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )

        label = response.choices[0].message.content.strip().lower()

    except:
        label = "personal"

    if "spam" in label:
        return Action(action_type="move", label="spam")

    if "important" in label:
        return Action(
            action_type="respond",
            label="important",
            response_text="Noted."
        )

    return Action(
        action_type="respond",
        label="personal",
        response_text="Sounds good!"
    )

# ---------- MAIN ----------
async def run_agent(task_name):
    env = InboxEnv()
    env.task_type = task_name

    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task_name, BENCHMARK, MODEL_NAME)

    try:
        result = await env.reset()
        obs = result["observation"]

        for step in range(1, MAX_STEPS + 1):

            if result["done"]:
                break

            subject, body = get_obs_fields(obs)

            action = decide_action_llm(subject, body)
            action_str = f"{action.action_type}:{action.label}"

            result = await env.step(action)

            obs = result["observation"]
            reward = result["reward"]
            done = result["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_str, reward, done, None)

            if done:
                break

        # ---------- SCORE FIX ----------
        if rewards:
            score = sum(rewards) / len(rewards)
        else:
            score = 0.01

        # clamp STRICTLY (0,1)
        if score <= 0.0:
            score = 0.01
        elif score >= 1.0:
            score = 0.99

        success = score >= SUCCESS_THRESHOLD

    finally:
        await env.close()
        log_end(success, steps_taken, score, rewards)

# ---------- RUN ----------
if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        asyncio.run(run_agent(task))
