# Importing necessary modules and classes
from enum import IntEnum  # Importing IntEnum for defining priority levels
from typing import List, Optional  # Importing List and Optional for type hints

from fastapi import FastAPI, HTTPException  # Importing FastAPI and HTTPException
from pydantic import BaseModel, Field  # Importing BaseModel and Field for data validation

# Creating a new FastAPI application
api = FastAPI()

# Defining an enumeration for priority levels
class Priority(IntEnum):
    LOW = 3  # Low priority
    MEDIUM = 2  # Medium priority
    HIGH = 1  # High priority

# Defining a base model for todos
class TodoBase(BaseModel):
    # Todo name with validation (min_length=3, max_length=512)
    todo_name: str = Field(..., min_length=3, max_length=512, description="The name of the todo")
    # Todo description with validation
    todo_description: str = Field(..., description="The description of the todo")
    # Priority with default value (LOW)
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo')

# Defining a model for creating new todos
class TodoCreate(TodoBase):
    pass  # Inheriting all fields from TodoBase

# Defining a model for todos with an additional id field
class Todo(TodoBase):
    # Unique identifier for the todo
    todo_id: int = Field(..., description='Unique Identifier of the Todo')

# Defining a model for updating existing todos
class TodoUpdate(BaseModel):
    # Optional todo name with validation (min_length=3, max_length=512)
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of the todo')
    # Optional todo description
    todo_description: Optional[str] = Field(None, description='Description of the todo')
    # Optional priority
    priority: Optional[Priority] = Field(None, description='Priority of the todo')

# Initializing a list of todos
all_todos = [
    Todo(todo_id=1, todo_name="Buy milk", todo_description="Buy milk from the store", priority=Priority.LOW),
    Todo(todo_id=2, todo_name="Buy eggs", todo_description="Buy eggs from the store", priority=Priority.LOW),
    Todo(todo_id=3, todo_name="Buy bread", todo_description="Buy bread from the store", priority=Priority.MEDIUM),
    Todo(todo_id=4, todo_name="Buy cheese", todo_description="Buy cheese from the store", priority=Priority.LOW),
    Todo(todo_id=5, todo_name="Buy water", todo_description="Buy water from the store", priority=Priority.HIGH),
]

# Defining routes for the API

# GET route for the root URL
@api.get("/")
def index():
    return {"message": "Hello World"}

# GET route for retrieving a todo by id
@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id):
    # Iterate through the list of todos to find the one with the matching id
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    # Raise a 404 error if the todo is not found
    raise HTTPException(status_code=404, detail="Todo not found")

# GET route for retrieving a list of todos
@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int = None):
    # If first_n is provided, return the first n todos
    if first_n:
        return all_todos[:first_n]
    # Otherwise, return all todos
    else:
        return all_todos

# POST route for creating a new todo
@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    # Generate a new todo id by incrementing the maximum id in the list
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    # Create a new todo with the provided data and the generated id
    new_todo = Todo(todo_id=new_todo_id,
                    todo_name=todo.todo_name,
                    todo_description=todo.todo_description,
                    priority=todo.priority)
    # Add the new todo to the list
    all_todos.append(new_todo)
    # Return the new todo
    return new_todo

# PUT route for updating an existing todo
@api.put('todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    # Iterate through the list of todos to find the one with the matching id
    for todo in all_todos:
        if todo.todo_id == todo_id:
            # Update the todo with the provided data, if it exists
            if updated_todo.todo_name is not None:
                # Update the todo name
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                # Update the todo description
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                # Update the todo priority
                todo.priority = updated_todo.priority
            # Return the updated todo
            return todo
    
    # Raise a 404 error if the todo is not found
    raise HTTPException(status_code=404, detail="Todo not found")


# DELETE route for deleting a todo by id
@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    # Iterate through the list of todos to find the one with the matching id
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            # Remove the todo from the list and return it
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    # Raise a 404 error if the todo is not found
    raise HTTPException(status_code=404, detail="Todo not found")