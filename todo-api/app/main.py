from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import SessionLocal, engine, Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#Creates a table if necessary
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = auth.create_access_token(data={"sub", user.username})
    return {"acccess_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model="Out")
def register(user: UserCreate, db: Session = Depends(get_db)):
    pass
