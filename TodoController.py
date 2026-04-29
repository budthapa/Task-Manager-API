from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from dataclasses import dataclass

@dataclass
class TodoObject:
    title: str
    completed: bool 
    id: int
    
TODO_DATA_LIST: list[TodoObject]=[
    TodoObject(title="Buy Milk", completed=False, id=1),
    TodoObject(title="Cook Dinner", completed=True, id=2),
    TodoObject(title="Start Project", completed=False, id=3),
    TodoObject(title="Watch movie", completed=False, id=4),
    TodoObject(title="Wash Car", completed=True, id=5),
]

class TodoController(Controller):
    path = "/todo-items"
    
    @get("/")
    async def get_tasks(self) -> list[TodoObject]:
        # Logic to retrieve tasks
        return TODO_DATA_LIST
    
    @get("/{task_id:int}")
    async def get_task(self, task_id: int) -> TodoObject:
        # Logic to retrieve a specific task by ID
        # next() is used to find the first task in the TODO_DATA_LIST that matches the provided task_id. 
        # If no matching task is found, it returns None.
        task = next((task for task in TODO_DATA_LIST if task.id == task_id), None)
         
        if task is None:
            raise NotFoundException(detail=f"Task with ID {task_id} not found")    
        return task
    
    @post("/")
    async def create_task(self, data: TodoObject) -> TodoObject:
        # Logic to create a new task
        data.id = len(TODO_DATA_LIST) + 1
        TODO_DATA_LIST.append(data)
        return data
    
    @put("/{task_id:int}")
    async def update_task(self, task_id: int, data: TodoObject) -> TodoObject:
        # Logic to update an existing task by ID
        task = next((task for task in TODO_DATA_LIST if task.id == task_id), None)
        if task is None:
            raise NotFoundException(detail=f"Task with ID {task_id} not found")
        task.title = data.title
        task.completed = data.completed
        
        return task
    
    
    @delete("/{task_id:int}")
    async def delete_task(self, task_id: int) -> None:
        # Logic to delete a task by ID
        task = next((task for task in TODO_DATA_LIST if task.id == task_id), None)
        if task is None:
            raise NotFoundException(detail=f"Task with ID {task_id} not found")
        
        TODO_DATA_LIST.remove(task)
    
    
