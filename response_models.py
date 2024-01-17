from pydantic import BaseModel


class TodoListModel(BaseModel):
    todo_id: int
    todo_title: str
    todo_description: str
    completed: bool


class SuccessResponse(BaseModel):
    message: str


class InternalServerErrorResponse(BaseModel):
    message: str
    reason: str


class NotFoundErrorResponse(BaseModel):
    message: str
