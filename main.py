from fastapi import FastAPI

api = FastAPI()


all_todos = [
    { 'todo_id': 1, 'todo_name': 'Sports', 'todo_description': 'Go to the gym'},
    { 'todo_id': 2, 'todo_name': 'Groceries', 'todo_description': 'Buy groceries'},
    { 'todo_id': 3, 'todo_name': 'Home', 'todo_description': 'Clean the house'},
    { 'todo_id': 4, 'todo_name': 'Work', 'todo_description': 'Work out'},
    { 'todo_id': 5, 'todo_name': 'Study', 'todo_description': 'Study for exams'},
]



#GET, POST, PUT, DELETE routes
@api.get("/")
def index():
    return {"message": "Hello World"}


@api.get('/todos/{todo_id}')
def get_todo(todo_id):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result': todo}



@api.get('/todos')
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
     return all_todos



@api.post('/todos')
def create_todo(todo:dict):
    new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1
    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }
    all_todos.append(new_todo)
    return  new_todo
    