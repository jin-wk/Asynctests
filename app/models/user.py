from pydantic import BaseModel, EmailStr, SecretStr


class UserBase(BaseModel):
    email: EmailStr
    password: SecretStr


class UserRegister(UserBase):
    password_confirm: SecretStr
    name: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
