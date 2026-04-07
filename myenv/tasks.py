import random
from myenv.models import Action


def get_task(task_type="easy"):
    if task_type == "easy":
        return random.choice([
            {"subject": "Meeting Tomorrow", "body": "Project meeting at 10 AM", "label": "important"},
            {"subject": "Hey!", "body": "Let's catch up this weekend", "label": "personal"},
            {"subject": "Free Offer!", "body": "Click to win money", "label": "spam"},
        ])

    if task_type == "medium":
        return random.choice([
            {"subject": "Job Opportunity", "body": "Apply now for high salary", "label": "spam"},
            {"subject": "Project Update", "body": "Deadline is approaching", "label": "important"},
            {"subject": "Dinner Plan", "body": "Shall we go out tonight?", "label": "personal"},
        ])

    if task_type == "hard":
        return random.choice([
            {"subject": "Limited Time Offer", "body": "Urgent offer just for you", "label": "spam"},
            {"subject": "Team Sync", "body": "Important project discussion", "label": "important"},
            {"subject": "Long time no see", "body": "We should meet soon", "label": "personal"},
        ])


def decide_action(subject: str, body: str) -> Action:
    text = (subject + " " + body).lower()

    spam_keywords = [
        "free", "click", "win", "offer",
        "earn", "money", "job", "apply",
        "limited time", "urgent", "lottery"
    ]

    if any(word in text for word in spam_keywords):
        return Action(action_type="move", label="spam")

    if any(word in text for word in [
        "noreply", "mailer-daemon", "delivery status"
    ]):
        return Action(action_type="ignore", label="system")

    if "meeting" in text or "project" in text:
        return Action(
            action_type="respond",
            label="important",
            response_text="I will attend."
        )

    return Action(
        action_type="respond",
        label="personal",
        response_text="Sounds good!"
    )
