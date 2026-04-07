from typing import Dict, Any
import random

from .models import Observation, Action
from .tasks import get_task, grade_action


class InboxEnv:
    def __init__(self, task_type="easy"):
        self.current_email = None
        self.done = False
        self.task_type = task_type
        self.email_counter = 0

    def reset(self):
        self.done = False
        self.current_email = get_task(self.task_type)
        self.email_counter += 1

        senders = [
            "boss@company.com",
            "friend@gmail.com",
            "noreply@alerts.com",
            "hr@jobs.com"
        ]

        observation = Observation(
            email_id=self.email_counter,
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender=random.choice(senders)
        )

        return observation

    def step(self, action: Action):
        if self.done:
            return None, 0.0, True, {}

        reward = grade_action(self.current_email, action)
        self.done = True

        observation = Observation(
            email_id=self.email_counter,
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender="system"
        )

        return observation, reward, True, {"correct_label": self.current_email["label"]}

    def close(self):
        pass