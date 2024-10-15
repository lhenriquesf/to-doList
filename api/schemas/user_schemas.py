from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=4)
    confirm_password: str = Field(..., min_length=4)

    @field_validator('confirm_password')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Senhas são diferentes')
        return v

