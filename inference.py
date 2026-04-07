import asyncio
from myenv.environment import InboxEnv
from myenv.tasks import decide_action


async def run():
    env = InboxEnv(task_type="easy")

    result = await env.reset()
    obs = result["observation"]

    action = decide_action(obs.subject, obs.body)
    result = await env.step(action)

    print("Observation:", obs)
    print("Action:", action)
    print("Reward:", result["reward"])


if __name__ == "__main__":
    asyncio.run(run())
