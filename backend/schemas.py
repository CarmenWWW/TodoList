# schemas.py
from pydantic import BaseModel
from typing import Optional, List


# TO support creation and update APIs
class CreateAndUpdateTodo(BaseModel):
    item: str



# TO support list and get APIs
class Todo(CreateAndUpdateTodo):
    id: int

    class Config:
        orm_mode = True


# To support list cars API
class PaginatedTodoInfo(BaseModel):
    data: List[Todo]