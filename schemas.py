from pydantic import BaseModel, Field

class UserSignup(BaseModel):
    name: str
    age: int
    location: str
    email: str
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    email:str
    password:str
