from dataclasses import dataclass
from typing import Optional
from litestar import Litestar, delete, get, post, put
from litestar.exceptions import HTTPException, NotFoundException

@dataclass
class TodoItem:
    title: str
    completed: bool

TODO_LIST: list[TodoItem] = [
    TodoItem(title="Buy Milk", completed=False),
    TodoItem(title="Cook Dinner", completed=True),
    TodoItem(title="Start Project", completed=False),
    TodoItem(title="???", completed=False),
    TodoItem(title="Wash Car", completed=True),
]

@get("/todos")
# The `completed` query parameter is expected to be a string that can be "1" for completed items, "0" for incomplete items, or any other value will result in a 400 Bad Request error.
async def get_list(completed: str) -> list[TodoItem]:
    if completed.strip().lower() == "1":
        return [item for item in TODO_LIST if item.completed] 
    elif completed.strip().lower() == "0":
        return [item for item in TODO_LIST if not item.completed]
    else:
        raise HTTPException(status_code=400, detail=f"Invalid query parameter: {completed}")

# more better way to handle the query parameter is to use a boolean type and let 
# Litestar handle the parsing and validation. Here's how you can modify the code:
# also, make the completed parameter optional. If it's not provided, we can return all TODO items regardless of their completion status.
# if we can to return the not completed items when completed is false, we can use False as the value for the completed query parameter. Litestar will handle the parsing and validation, and we can filter the TODO_LIST accordingly. Here's how you can modify the code:
@get("/mytodos")
async def get_todos(completed: Optional[bool] = False) -> list[TodoItem]:
    if completed is None:
        return TODO_LIST
    return [item for item in TODO_LIST if item.completed == completed]

@post("/mytodos")
async def add_item(data: TodoItem) -> list[TodoItem]:
    TODO_LIST.append(data)
    return TODO_LIST

@put("/mytodos/{item_title:str}")
async def update_item(item_title: str, data: TodoItem) -> list[TodoItem]:
    todo_item = get_todo_item_by_title(item_title)
    todo_item.title = data.title
    todo_item.completed = data.completed
    return TODO_LIST
 
def get_todo_item_by_title(item_title: str) -> TodoItem:
    for item in TODO_LIST:
        if item.title.lower() == item_title.lower():
            return item
    raise NotFoundException(detail=f"TODO item with title '{item_title}' not found")

# delete usually doesn't return any content, so we can set the return type to None. 
# The delete_item function will remove the specified item from the TODO_LIST and 
# return a 204 No Content response if the deletion is successful. 
# If the item is not found, it will raise a NotFoundException.
@delete("/mytodos/{item_title: str}")
async def delete_item(item_title: str) -> None:  
    
    # check if item exists before attempting to delete it
    # if not exists throw a NotFoundException
    item = [item for item in TODO_LIST if item.title.lower() == item_title.lower()]
    if not item:
        raise NotFoundException(detail=f"TODO item with title '{item_title}' not found")

    TODO_LIST[:] = [item for item in TODO_LIST if item.title.lower() != item_title.lower()]

