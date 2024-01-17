from pydantic import BaseModel


class TodoModel(BaseModel):
    todo_title: str
    todo_description: str
    completed: bool
