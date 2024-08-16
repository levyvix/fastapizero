from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPulic(BaseModel):
    username: str
    email: EmailStr


class UserDB(UserSchema):
    id: int


class UserPublicId(UserPulic):
    id: int


class UserListWithId(BaseModel):
    users: list[UserPublicId]
