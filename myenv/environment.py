from typing import Dict, Any
from .models import Observation, Action
from .tasks import get_task


class InboxEnv:
    def __init__(self, task_type="easy"):
        self.current_email = None
        self.done = False
        self.task_type = task_type
        self.email_counter = 0

    async def reset(self) -> Dict[str, Any]:
        self.done = False
        self.current_email = get_task(self.task_type)
        self.email_counter += 1

        observation = Observation(
            email_id=self.email_counter,
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender="test@example.com"
        )

        return {
            "observation": observation,
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    async def step(self, action: Action) -> Dict[str, Any]:
        if self.done:
            return {
                "observation": None,
                "reward": 0.0,
                "done": True,
                "info": {}
            }

        correct_label = self.current_email["label"]
        reward = 1.0 if action.label == correct_label else 0.0

        self.done = True

        observation = Observation(
            email_id=self.email_counter,
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender="test@example.com"
        )

        return {
            "observation": observation,
            "reward": reward,
            "done": True,
            "info": {"correct_label": correct_label}
        }

    async def close(self):
        pass
