from pydantic import BaseModel, EmailStr

class SignupModel(BaseModel):
    name: str
    email: EmailStr
    gender: str
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str
