from myenv.models import Action
import random

TASKS = {
    "easy": [
        {
            "subject": "Team meeting tomorrow",
            "body": "We will discuss project updates",
            "label": "important"
        }
    ],

    "medium": [
        {
            "subject": "Limited offer! Earn money fast",
            "body": "Click here to earn money instantly",
            "label": "spam"
        },
        {
            "subject": "Lunch plans?",
            "body": "Are you free this weekend?",
            "label": "personal"
        }
    ],

    "hard": [
        {
            "subject": "Project deadline reminder",
            "body": "Final submission tomorrow, please review attached files",
            "label": "important"
        },
        {
            "subject": "Internship opportunity",
            "body": "Apply now to gain experience and earn money",
            "label": "spam"
        },
        {
            "subject": "Re: Last discussion",
            "body": "Let's continue our previous conversation about the trip",
            "label": "personal"
        }
    ]
}


def get_task(task_type):
    return random.choice(TASKS[task_type])


def grade_action(task, action: Action) -> float:
    correct = task["label"]

    if action.label == correct:
        return 1.0

    # partial credit
    if correct == "important" and action.label == "personal":
        return 0.5

    if correct == "personal" and action.label == "important":
        return 0.5

    # spam mistakes = strict
    if correct == "spam" and action.label != "spam":
        return 0.0

    return 0.0