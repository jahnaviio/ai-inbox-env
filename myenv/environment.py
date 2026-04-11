import random
from typing import List
from myenv.models import Action

class Email:
    def __init__(self, id, subject, body, sender, true_label):
        self.id = id
        self.subject = subject
        self.body = body
        self.sender = sender
        self.true_label = true_label


class InboxEnv:
    def __init__(self):
        self.task_type = "easy"
        self.current_step = 0
        self.max_steps = 5
        self.inbox: List[Email] = []
        self.done = False

    # ---------- TASK DATA ----------
    def generate_emails(self):
        if self.task_type == "easy":
            return [
                Email(1, "Meeting Tomorrow", "Project meeting at 10 AM", "boss@mail.com", "important"),
                Email(2, "Win Cash Prize", "Click here to win money", "spam@offer.com", "spam"),
                Email(3, "Dinner Plan", "Shall we go out tonight?", "friend@mail.com", "personal"),
                Email(4, "Job Update", "Your interview is scheduled", "hr@mail.com", "important"),
                Email(5, "Discount Offer", "Flat 50% off", "promo@mail.com", "spam"),
            ]

        if self.task_type == "medium":
            return [
                Email(1, "Workshop Invite", "Join career workshop", "event@mail.com", "important"),
                Email(2, "Limited Offer", "Buy now limited sale", "sales@mail.com", "spam"),
                Email(3, "Family Function", "Don't forget the event", "family@mail.com", "personal"),
                Email(4, "Account Update", "Please update profile", "service@mail.com", "important"),
                Email(5, "Newsletter", "Weekly updates", "news@mail.com", "spam"),
            ]

        if self.task_type == "hard":
            return [
                Email(1, "Free Career Webinar", "Enhance your skills", "career@mail.com", "important"),
                Email(2, "Urgent: Account Suspended", "Verify now", "fakebank@mail.com", "spam"),
                Email(3, "Catch up soon", "Long time no see", "friend@mail.com", "personal"),
                Email(4, "Project Deadline Reminder", "Submit work today", "manager@mail.com", "important"),
                Email(5, "Special Promotion", "Exclusive deal for you", "ads@mail.com", "spam"),
            ]

    # ---------- RESET ----------
    async def reset(self):
        self.current_step = 0
        self.done = False
        self.inbox = self.generate_emails()

        return {
            "observation": self._get_obs(),
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    # ---------- STEP ----------
    async def step(self, action: Action):
        if self.done:
            return {
                "observation": self._get_obs(),
                "reward": 0.0,
                "done": True,
                "info": {}
            }

        email = self.inbox[self.current_step]

        reward = self.calculate_reward(email, action)

        self.current_step += 1

        if self.current_step >= self.max_steps:
            self.done = True

        return {
            "observation": self._get_obs(),
            "reward": reward,
            "done": self.done,
            "info": {}
        }

    # ---------- OBS ----------
    def _get_obs(self):
        if self.current_step >= len(self.inbox):
            return None

        email = self.inbox[self.current_step]

        return {
            "email_id": email.id,
            "subject": email.subject,
            "body": email.body,
            "sender": email.sender
        }

    # ---------- REWARD ----------
    def calculate_reward(self, email: Email, action: Action):
        reward = 0.0

        # correct classification
        if action.label == email.true_label:
            reward += 0.7
        else:
            reward -= 0.4

        # penalize unnecessary reply
        if action.action_type == "respond" and email.true_label == "spam":
            reward -= 0.3

        # penalize ignoring important
        if action.action_type == "ignore" and email.true_label == "important":
            reward -= 0.6

        # small cost for replying
        if action.action_type == "respond":
            reward -= 0.1

        # 🔥 clamp into (0,1)
        if reward <= 0:
            reward = 0.05
        elif reward >= 1:
            reward = 0.95

        return reward

    # ---------- CLOSE ----------
    async def close(self):
        pass
