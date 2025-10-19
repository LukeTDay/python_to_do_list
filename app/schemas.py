from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

#This is sent by the client to create an account
class UserCreate(BaseModel):
    username: str = Field(strip_whitespace=True, min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=72)

#This is sent by the server when an account is succsesfully created
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
#This is sent by the client to obtain a login token
class UserLogin(BaseModel):
    username: str
    password: str
#This will be sent by the server after a successful login
class Token(BaseModel):
    access_token: str
    token_type: str

class TodoCreate(BaseModel):
    title: str
    due_by: datetime

class TodoOut(BaseModel):
    id: int
    title: str
    due_by: datetime
    completed: bool

    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    due_by: Optional[datetime] = None
    completed: Optional[bool] = None

class TodoUpdateOut(BaseModel):
    id: int
    title: str
    due_by: datetime
    completed: bool

class TodoDelete(BaseModel):
    id:int

class TodoDeleteOut(BaseModel):
    success: bool