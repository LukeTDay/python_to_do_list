from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from . import models, schemas, auth
from .database import get_db, engine
from .schemas import UserCreate, UserOut
from .auth import get_current_user

#Creates a table if necessary
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=schemas.UserOut)
def register(user: UserCreate,
             db: Session = Depends(get_db)):
    desired_username = db.query(models.User).filter(models.User.username == user.username).first()
    if desired_username != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use"
        )
    print(user.password)
    hashed_pw = auth.hash_password(user.password)

    new_user = models.User(
        username = user.username,
        hashed_password = hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/todos", response_model=List[schemas.TodoOut])
def read_todos(current_user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db),
                ):
    
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return todos

@app.post("/todos", response_model=schemas.TodoOut)
def create_todo(
    todo: schemas.TodoCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    new_todo = models.Todo(
        user_id = current_user.id,
        title = todo.title,
        due_by = todo.due_by
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

#Updates an existing todo list item
@app.post("/todos/update", response_model=schemas.TodoUpdateOut)
def update_todo(
    requested_update: schemas.TodoUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    requested_todo_update = db.query(models.Todo).filter((models.Todo.user_id == current_user.id) & (models.Todo.id == requested_update.id)).first()

    if not requested_todo_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if requested_update.title is not None:
        requested_todo_update.title = requested_update.title
    if requested_update.due_by is not None:
        requested_todo_update.due_by = requested_update.due_by
    if requested_update.completed is not None:
        requested_todo_update.completed = requested_update.completed

    db.commit()
    db.refresh(requested_todo_update)
    return requested_todo_update

#What is the purpose of the response model if I have to send my own JSON?
# These automatically sanitize your response so that only data you have
# designated in your schemas will be sent.
# In this i send a "password" but on the client side all i see is 
# success : True
#Deletes an existing todo list item by its index
@app.post("/todos/delete",
          response_model=schemas.TodoDeleteOut)
def delete_todo(
    requested_deletions: schemas.TodoDelete,
    current_user: models.User = Depends(get_current_user),  
    db: Session = Depends(get_db)
    ):
    requested_todo_deletion = db.query(models.Todo).filter((models.Todo.user_id == current_user.id) & (models.Todo.id == requested_deletions.id)).first()

    if not requested_todo_deletion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found during requested deletion"
        )
    db.delete(requested_todo_deletion)
    db.commit()
    return {"success" : True,
            "realpw" : "password"}