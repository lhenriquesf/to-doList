from pydantic import BaseModel, Field, field_validator
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.task_models import Task

GetTask = pydantic_model_creator(Task, name="Task")

class PostTask(BaseModel):
    task:str = Field(...,max_length=100)
    done:bool = Field(default=False)

    @field_validator('task')
    def check_not_empty(task):
        if not task or task.strip() == "":
            raise ValueError("A tarefa não pode estar vazia.")
        return task



class PutTask(BaseModel):
    task:Optional[str] = Field(None, max_length=100)
    done:Optional[bool] = Field(None)

    @field_validator('task')
    def check_not_empty(task):
        if not task or task.strip() == "":
            raise ValueError("A tarefa não pode estar vazia.")
        return task
