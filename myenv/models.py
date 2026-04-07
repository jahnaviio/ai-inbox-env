from pydantic import BaseModel
from typing import Optional


class Observation(BaseModel):
    email_id: int
    subject: str
    body: str
    sender: str


class Action(BaseModel):
    action_type: str
    label: Optional[str] = None
    response_text: Optional[str] = None