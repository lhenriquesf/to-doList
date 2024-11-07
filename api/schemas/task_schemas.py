"""Módulo que define os esquemas Pydantic para as tarefas.

Este módulo contém os esquemas Pydantic usados para validar e serializar os
dados das tarefas, incluindo a criação e atualização de tarefas. Ele também
contém validadores para garantir que os dados atendam a certos critérios.
"""

from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field, field_validator
from api.models.task_models import Task


GetTask = pydantic_model_creator(Task, name="Task")

class PostTask(BaseModel):
    """Esquema para criar uma nova tarefa.

    Este esquema é usado para validar os dados ao criar uma nova tarefa. Ele
    garante que o campo `task` não esteja vazio e define um valor padrão de 
    `False` para o campo `done`.

    Attributes:
        task (str): A descrição da tarefa.
        done (bool): O status da tarefa (padrão: `False`).
    """
    task:str = Field(...,max_length=100)
    done:bool = Field(default=False)

    @field_validator('task')
    def check_not_empty(v):
        """
        Args:
            v (str): Valor do campo `task`.

        Raises:
            ValueError: Se o campo `task` estiver vazio ou contiver apenas espaços.

        Returns:
            str: O valor validado do campo `task`.
        """
        if not v or v.strip() == "":
            raise ValueError("A tarefa não pode estar vazia.")
        return v



class PutTask(BaseModel):
    """Esquema para atualizar uma tarefa existente.

    Este esquema é usado para validar os dados ao atualizar uma tarefa. Ele
    permite que os campos `task` e `done` sejam opcionais para atualização.

    Attributes:
        task (Optional[str]): A descrição da tarefa (opcional).
        done (Optional[bool]): O status da tarefa (opcional).
    """
    task:Optional[str] = Field(None, max_length=100)
    done:Optional[bool] = Field(None)

    @field_validator('task')
    def check_not_empty(v):
        """
        Args:
            v (Optional[str]): Valor do campo `task`.

        Raises:
            ValueError: Se o campo `task` estiver vazio ou contiver apenas espaços.

        Returns:
            Optional[str]: O valor validado do campo `task`, ou `None` se não fornecido.
        """
        if not v or v.strip() == "":
            raise ValueError("A tarefa não pode estar vazia.")
        return v
