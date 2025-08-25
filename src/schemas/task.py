from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int

class TaskGet(TaskCreate):
    id: int
    done: bool
    user_id: int

    class Config:
        from_attributes = True

