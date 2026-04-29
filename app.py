from typing import Union
from warnings import deprecated
from litestar import Litestar, get

from litestar.plugins.sqlalchemy import (
    SQLAlchemyInitPlugin,
    SQLAlchemySerializationPlugin,
)

from DBConnection import get_db_config, provide_transaction
from TodoController import TodoController

from data_list import add_item, delete_item, get_list, get_todos, update_item

# using typing.Union to allow for both string and boolean values in the TODO_LIST
# values can be strings or booleans, so we use Union to specify that in the type hint
# list contains dictionaries with "title" as a string and "completed" as a boolean
TODO_LIST: list[dict[str, Union[str, bool]]] = [
    {"title": "Buy groceries", "completed": False},
    {"title": "Clean the house", "completed": True},
    {"title": "Finish project", "completed": False},
    {"title": "???", "completed": False},
]   

# same approach using dataclasses to define the structure of the TODO items in data_list.py class

@get("/")
async def get_todo_list() -> list[dict[str, Union[str, bool]]]:
    return TODO_LIST


app = Litestar(
    [get_todo_list, get_list, get_todos, add_item, update_item, delete_item, TodoController],
    dependencies={"transaction": provide_transaction},
    plugins=[
        SQLAlchemySerializationPlugin(),
        SQLAlchemyInitPlugin(get_db_config()),
    ],
    
)