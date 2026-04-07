import asyncio
import time
from typing import List, Optional

from myenv.environment import InboxEnv
from myenv.models import Action


BENCHMARK = "ai_inbox_env"

MAX_STEPS = 5
SUCCESS_THRESHOLD = 0.5


def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model=rule-based-agent", flush=True)


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


def decide_action(obs) -> Action:
    text = (obs.subject + " " + obs.body).lower()

    # 🔥 strong spam detection
    if any(word in text for word in [
        "free", "click", "earn", "offer", "apply",
        "money", "internship", "win", "urgent"
    ]):
        return Action(action_type="ignore", label="spam")

    # 🔥 important emails
    if any(word in text for word in [
        "meeting", "project", "deadline", "review", "submission"
    ]):
        return Action(
            action_type="respond",
            label="important",
            response_text="Noted, I will handle it."
        )

    # 🔥 personal emails
    return Action(
        action_type="respond",
        label="personal",
        response_text="Sounds good!"
    )


async def run_agent(task_name):
    env = InboxEnv(task_type=task_name)

    rewards = []
    steps_taken = 0
    success = False

    log_start(task_name, BENCHMARK, "rule-based-agent")

    try:
        obs = env.reset()

        for step in range(1, MAX_STEPS + 1):

            action = decide_action(obs)
            action_str = f"{action.action_type}:{action.label}"

            obs, reward, done, info = env.step(action)

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_str, reward, done, None)

            if done:
                break

        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = max(0.0, min(score, 1.0))
        success = score >= SUCCESS_THRESHOLD

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        asyncio.run(run_agent(task))

    # keep container alive
    while True:
        time.sleep(60)