from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str]
    completed: Optional[bool] = False

    class Config:
        orm_mode = True
        from_attributes = True
