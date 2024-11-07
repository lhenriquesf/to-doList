"""Módulo que define o modelo de tarefa para o banco de dados.

Este módulo contém a definição do modelo `Task`, que é usado para armazenar
informações sobre as tarefas no sistema. Ele inclui os campos de `id`, 
`task` (descrição da tarefa) e `done` (status de conclusão da tarefa).
"""

from tortoise.models import Model
from tortoise.fields import IntField, BooleanField, CharField

class Task(Model):
    """Modelo que representa uma tarefa no sistema.

    A classe `Task` define os atributos de uma tarefa, incluindo um identificador 
    único `id`, uma descrição da tarefa `task`, e um campo boolean `done` que 
    indica se a tarefa foi concluída. O campo `done` tem um valor padrão de `False`.
    """
    id = IntField(pk=True)
    task = CharField(max_length=100, null=False)
    done = BooleanField(default=False, null=False)
