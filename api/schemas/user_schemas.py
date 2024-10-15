from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8)
