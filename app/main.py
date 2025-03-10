from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db, Base
from .models import Todo
from .schema import Todo as TodoSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/todos/{:todo_id}', response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    result = db.query(Todo).filter(Todo.id == todo_id).first()
    if not result:
        return HTTPException(status=404, detail="No todo found!")
    return result

@app.get('/', response_model=list[TodoSchema])
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.post('/create/', response_model=TodoSchema)
def create_todo(todo: TodoSchema, db: Session = Depends(get_db)):
    db_todo = Todo(
            task=todo.task,
            description=todo.description,
            is_completed=todo.is_completed
            )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put('/edit/{:todo_id}', response_model=TodoSchema)
def edit_todo(todo_id: int, todo: TodoSchema, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return HTTPException(status=404, detail="Todo not found!")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete('/delete/{:todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return HTTPException(status=404, detail="Todo not found!")
    db.delete(db_todo)
    db.commit()
    return {"message": "Task deleted successfully."}

