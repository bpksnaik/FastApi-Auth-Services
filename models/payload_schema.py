from pydantic import BaseModel, EmailStr, Field


class Userdetails(BaseModel):
    name: str = Field(description="name of the user")
    email_id: EmailStr = Field(description="User's Email_id")
    password: str = Field(description="user's password")


class UserCredentials(BaseModel):
    email_id: EmailStr = Field(description="User's Email_id")
    password: str = Field(description="User's password")
