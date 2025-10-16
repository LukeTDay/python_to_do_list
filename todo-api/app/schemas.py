from pydantic import BaseModel, Field

#This is sent by the client to create an account
class UserCreate(BaseModel):
    username: str = Field(strip_whitespace=True, min_length=3, max_length=50)
    password: str = Field(min_length=6)

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