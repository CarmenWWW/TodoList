# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import TodoInfoAlreadyExistError, TodoInfoNotFoundError
from models import TodoInfo
from schemas import CreateAndUpdateTodo


# Function to get list of car info
def get_all_todo(session: Session) -> List[TodoInfo]:
    return session.query(TodoInfo).all()


# Function to  get info of a particular todo
def get_todo_info_by_id(session: Session, _id: int) -> TodoInfo:
    todo_info = session.query(TodoInfo).get(_id)

    if todo_info is None:
        raise TodoInfoNotFoundError

    return todo_info


# Function to add a new todo info to the database
def create_todo(session: Session, todo_info: CreateAndUpdateTodo) -> TodoInfo:
    # todo_details = session.query(TodoInfo).filter(TodoInfo.item == todo_info.item)
    # if todo_details is not None:
    #     raise TodoInfoAlreadyExistError

    new_todo_info = TodoInfo(**todo_info.dict())
    session.add(new_todo_info)
    session.commit()
    session.refresh(new_todo_info)
    return new_todo_info


# Function to update details of the todo
def update_todo_info(session: Session, _id: int, info_update: CreateAndUpdateTodo) -> TodoInfo:
    todo_info = get_todo_info_by_id(session, _id)

    if todo_info is None:
        raise TodoInfoNotFoundError

    todo_info.item = info_update.item

    session.commit()
    session.refresh(todo_info)

    return todo_info


# Function to delete a todo info from the db
def delete_todo_info(session: Session, _id: int):
    todo_info = get_todo_info_by_id(session, _id)

    if todo_info is None:
        raise TodoInfoNotFoundError

    session.delete(todo_info)
    session.commit()

    return
