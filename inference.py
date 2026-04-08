import asyncio
import os
from typing import List, Optional
from openai import OpenAI

from myenv.environment import InboxEnv
from myenv.models import Action

# ENV VARIABLES
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

BENCHMARK = "ai_inbox_env"

MAX_STEPS = 5
SUCCESS_THRESHOLD = 0.5

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


# ---------- LOG FUNCTIONS ----------
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


# ---------- LLM DECISION ----------
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

    # ACTION MAPPING
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
    score = 0.5
    success = False

    log_start(task_name, BENCHMARK, MODEL_NAME)

    try:
        result = await env.reset()
        obs = result["observation"]

        for step in range(1, MAX_STEPS + 1):

            if result["done"]:
                break

            action = decide_action_llm(obs.subject, obs.body)
            action_str = f"{action.action_type}:{action.label}"

            result = await env.step(action)

            obs = result["observation"]
            reward = result["reward"]
            done = result["done"]

            # 🔥 FIX: clamp reward into (0,1)
            if reward <= 0.0:
                reward = 0.01
            elif reward >= 1.0:
                reward = 0.99

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_str, reward, done, None)

            if done:
                break

        # 🔥 FIX: safe score calculation
        if rewards:
            score = sum(rewards) / len(rewards)
        else:
            score = 0.5

        # 🔥 STRICT RANGE FIX
        if score <= 0.0:
            score = 0.01
        elif score >= 1.0:
            score = 0.99

        success = score > SUCCESS_THRESHOLD

    finally:
        await env.close()
        log_end(success, steps_taken, score, rewards)


# ---------- RUN ----------
if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        asyncio.run(run_agent(task))
