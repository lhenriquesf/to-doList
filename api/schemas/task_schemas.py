from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.task_models import Task

GetTask = pydantic_model_creator(Task, name="Task")

class PostTask(BaseModel):
    task:str = Field(...,max_length=100)
    done:bool

class PutTask(BaseModel):
    task:Optional[str] = Field(None, max_length=100)
    done:Optional[bool]