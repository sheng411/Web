from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    time: Optional[datetime] = None

    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    completed: bool

    class Config:
        orm_mode = True