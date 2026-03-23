from pydantic import BaseModel, EmailStr , field_validator,model_validator
from pydantic import Field 
import re
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserSignup(BaseModel):
    
    name: str
    age: int
    location: str
    email: EmailStr
    role: UserRole 
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

class CreateClass(BaseModel):
    name: str
    section:str

class SubjectCreate(BaseModel):
    name: str
    code : str

class SubjectResponse(BaseModel):
    name: str
    code: str
    

class MarkCreate(BaseModel):
    student_id: int
    subject_id: int
    exam_type: str
    marks: int

class TeacherSubjectCreate(BaseModel):
    teacher_id: int
    subject_id: int