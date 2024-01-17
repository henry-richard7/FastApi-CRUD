from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from typing import Annotated, List

import database_model
import api_models
import response_models

from database import engine, Sessionlocal

app = FastAPI()
database_model.Base.metadata.create_all(bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db

    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/api/lists", status_code=status.HTTP_200_OK)
async def list_todo(db: db_dependency) -> List[response_models.TodoListModel]:
    todo_list = db.query(database_model.Todo).all()
    return todo_list


@app.post(
    "/api/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successful Response",
            "model": response_models.SuccessResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error Response",
            "model": response_models.InternalServerErrorResponse,
        },
    },
)
async def create_todo(
    todo: api_models.TodoModel, db: db_dependency
) -> response_models.SuccessResponse:
    try:
        todo_element = database_model.Todo(**todo.model_dump())
        db.add(todo_element)
        db.commit()
        return JSONResponse(
            content=response_models.SuccessResponse(
                message=f"Added {todo_element.todo_title}!."
            ).model_dump()
        )

    except Exception as e:
        return JSONResponse(
            content=response_models.InternalServerErrorResponse(
                message="Error occured on insert.", reason=e
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.put(
    "/api/update",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "description": "Successful Response",
            "model": response_models.SuccessResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Response",
            "model": response_models.NotFoundErrorResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error Response",
            "model": response_models.InternalServerErrorResponse,
        },
    },
)
async def update_status(todo_id: int, is_completed: bool, db: db_dependency):
    try:
        selected_todo_list = (
            db.query(database_model.Todo)
            .filter(database_model.Todo.todo_id == todo_id)
            .first()
        )
        if selected_todo_list:
            selected_todo_list.completed = is_completed
            db.commit()
            return JSONResponse(
                content=response_models.SuccessResponse(
                    message=f"Update {selected_todo_list.todo_title}'s status to {is_completed}!"
                ).model_dump(),
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            return JSONResponse(
                content=response_models.NotFoundErrorResponse(
                    message=f"No record found for ToDo-id: {todo_id}."
                ).model_dump(),
                status_code=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return JSONResponse(
            content=response_models.InternalServerErrorResponse(
                message="Error occured on update.", reason=str(e)
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.delete(
    "/api/delete",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "model": response_models.SuccessResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Response",
            "model": response_models.NotFoundErrorResponse,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error Response",
            "model": response_models.InternalServerErrorResponse,
        },
    },
)
async def delete_todo(todo_id: int, db: db_dependency):
    try:
        selected_todo_list = (
            db.query(database_model.Todo)
            .filter(database_model.Todo.todo_id == todo_id)
            .first()
        )

        if selected_todo_list:
            db.delete(selected_todo_list)
            db.commit()
            return JSONResponse(
                content=response_models.SuccessResponse(
                    message=f"Deleted {selected_todo_list.todo_title}!"
                ).model_dump(),
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content=response_models.NotFoundErrorResponse(
                    message=f"No record found for {todo_id}."
                ).model_dump(),
                status_code=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return JSONResponse(
            content=response_models.InternalServerErrorResponse(
                message="Error occured on Delete.", reason=str(e)
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
