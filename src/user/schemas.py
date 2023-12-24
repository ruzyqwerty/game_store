from pydantic import BaseModel


class NewUser(BaseModel):
    login_user: str
    bill: int
    password: str

class UserInfo(BaseModel):
    login_user: str
    password: str

class AuthResponse(BaseModel):
    status: str
    data: str
