from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(...)
    email: str = Field()


class UserInDb(User):
    hs_password: str = Field(...)


class TokenModel(BaseModel):
    token: str = Field(...)