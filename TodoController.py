from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException

from dataclasses import dataclass

from BaseObject import TodoObject
from data_list import TodoItem


# Logic to retrieve a specific to-do item by its ID
# session is an instance of AsyncSession that is provided by the provide_transaction function,
# allowing for database interactions within this function.
async def get_todo_item(todo_id: int, session: AsyncSession) -> TodoObject:
    query = select(TodoObject).where(TodoObject.id == todo_id)
    result = await session.execute(query)
    try:
        # scalar_one() is used to retrieve a single scalar result from the query execution.
        return result.scalar_one()
    except NoResultFound as e:
        raise NotFoundException(detail=f"Todo item with ID '{todo_id}' not found") from e


# Logic to retrieve the list of to-do items, with an optional filter for completion status
# session is an instance of AsyncSession that is provided by the provide_transaction function, 
# allowing for database interactions within this function.
async def get_todo_list(completed: Optional[bool], session: AsyncSession) -> list[TodoObject]:
    # Logic to retrieve the list of to-do items
    query = select(TodoObject)
    if completed is not None:
        query = query.where(TodoObject.completed.is_(completed))
    
    # execute the query and return the results as a list of TodoObject instances
    # scalars() is used to extract the scalar values (in this case, the TodoObject instances) 
    # from the result of the query execution, and all() retrieves all of those instances as a list.
    result = await session.execute(query)
    return list(result.scalars().all())


class TodoController(Controller):
    path = "/todo-items"
    
    # All non-default parameters must come BEFORE default parameters in the function signature
    @get("/")
    async def get_list(self, transaction: AsyncSession, completed: Optional[bool] = None) -> list[TodoObject]:
        return await get_todo_list(completed, transaction)
    
    
    @get("/{task_id:int}")
    async def get_task(self, task_id: int, transaction: AsyncSession) -> TodoObject:
        # Logic to retrieve a specific task by ID
            
        return await get_todo_item(task_id, session=transaction)
        
    
    @post("/")
    async def create_task(self, data: TodoObject, transaction: AsyncSession) -> TodoObject:
        # Logic to create a new task
        transaction.add(data)
        return data
    
    
    @put("/{task_id:int}")
    async def update_task(self, task_id: int, data: TodoObject, transaction: AsyncSession) -> TodoObject:
        # Logic to update an existing task by ID
        todo_item = await get_todo_item(task_id, session=transaction)
        todo_item.title = data.title
        todo_item.completed = data.completed
        return todo_item
    
    
    @delete("/{task_id:int}")
    async def delete_task(self, task_id: int, transaction: AsyncSession) -> None:
        # Logic to delete a task by ID
        task = await get_todo_item(task_id, session=transaction)
        await transaction.delete(task)
        