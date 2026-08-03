from pydantic import BaseModel, EmailStr
from typing import Optional


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    assignee: Optional[EmailStr] = None
