from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import SessionLocal, engine, Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserCreate

#Creates a table if necessary
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = auth.create_access_token(data={"sub", user.username})
    return {"acccess_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=schemas.userOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    desired_username = db.query(models.User).filter(models.User.username == user.username).first()
    if desired_username != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use"
        )
    
    hashed_pw = auth.hash_password(user.password)

    new_user = models.User(
        username = user.username,
        hashed_password = hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user