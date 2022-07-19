from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_todo, create_todo, get_todo_info_by_id, update_todo_info, delete_todo_info
from database import get_db
from exceptions import TodoInfoException
from schemas import Todo, CreateAndUpdateTodo, PaginatedTodoInfo

router = APIRouter()



@cbv(router)
class Todos:
    session: Session = Depends(get_db)

    # API to get the list of todo info
    @router.get("/todo", response_model=PaginatedTodoInfo)
    def list_todo(self):

        todo_list = get_all_todo(self.session)
        response = {"data": todo_list}
        return response

    # API endpoint to add a todo info to the database
    @router.post("/todo")
    def add_todo(self, todo_info: CreateAndUpdateTodo):

        try:
            result = create_todo(self.session, todo_info)
            return result
        except TodoInfoException as cie:
            raise HTTPException(**cie.__dict__)


# API endpoint to get info of a particular todo
@router.get("/todo/{todo_id}", response_model=Todo)
def get_todo_info(todo_id: int, session: Session = Depends(get_db)):

    try:
        todo_info = get_todo_info_by_id(session, todo_id)
        return todo_info
    except TodoInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to update a existing todo info
@router.put("/todo/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, new_info: CreateAndUpdateTodo, session: Session = Depends(get_db)):

    try:
        todo_info = update_todo_info(session, todo_id, new_info)
        return todo_info
    except TodoInfoException as cie:
        raise HTTPException(**cie.__dict__)


# API to delete a todo info from the data base
@router.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_db)):

    try:
        return delete_todo_info(session, todo_id)
    except TodoInfoException as cie:
        raise HTTPException(**cie.__dict__)



# todos = [
#     {
#         "id": "1",
#         "item": "napa cabbage"
#     },
#     {
#         "id": "2",
#         "item": "yogurt"
#     }
# ]

# @app.get("/", tags=["root"])
# async def read_root() -> dict:
#     return {"message": "Welcome to your todo list."}

# @app.get("/todo", tags=["todos"])
# async def get_todos() -> dict:
#     return { "data": todos }

# @app.post("/todo", tags=["todos"])
# async def add_todo(todo: dict) -> dict:
#     todos.append(todo)
#     return {
#         "data": { "Todo added." }
#     }

# @app.put("/todo/{id}", tags=["todos"])
# async def update_todo(id: int, body: dict) -> dict:
#     for todo in todos:
#         if int(todo["id"]) == id:
#             todo["item"] = body["item"]
#             return {
#                 "data": f"Todo with id {id} has been updated."
#             }

#     return {
#         "data": f"Todo with id {id} not found."
#     }

# @app.delete("/todo/{id}", tags=["todos"])
# async def delete_todo(id: int) -> dict:
#     for todo in todos:
#         if int(todo["id"]) == id:
#             todos.remove(todo)
#             return {
#                 "data": f"Todo with id {id} has been removed."
#             }

#     return {
#         "data": f"Todo with id {id} not found."
#     }