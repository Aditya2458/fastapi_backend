from pydantic import BaseModel, EmailStr , field_validator,model_validator
from pydantic import Field 
import re

class UserSignup(BaseModel):
    
    name: str
    age: int
    location: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    confirm_password:str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls,v):
        pattern= r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).+$"
        if not re.match(pattern,v):
            raise ValueError ("Password must contain uppercase, lowercase, number and special character")
        return v

    @model_validator(mode="after")
    def password_match(self):
        if self.password!= self.confirm_password:
            raise ValueError  ("password do not match")
        return self

    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class ForgotPasswordRequest(BaseModel):
    email:EmailStr
    
class ResetPasswordRequest(BaseModel):
    token:str
    new_password: str = Field(min_length=8, max_length=72)