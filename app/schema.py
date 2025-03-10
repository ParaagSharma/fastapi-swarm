from pydantic import BaseModel

class Todo(BaseModel):
    task: str
    description: str | None = None
    is_completed: bool = False

