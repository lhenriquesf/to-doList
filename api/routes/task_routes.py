"""Módulo das rotas de tarefas (Task).

Este módulo define as rotas para operações CRUD na entidade Task,
incluindo a criação, leitura, atualização e exclusão de tarefas.
As rotas são protegidas e requerem autenticação do usuário.
"""

from api.schemas.task_schemas import GetTask, PostTask, PutTask
from api.models.task_models import Task
from api.auth import get_current_user
from fastapi import APIRouter, HTTPException, Depends

task_router = APIRouter(prefix="/api", tags=["Task"])


@task_router.get("/")
async def get_task():
    """
    Rota para listar todas as tarefas.

    Retorna todas as tarefas disponíveis no banco de dados.

    Returns:
        List[GetTask]: Lista de objetos de tarefas.
    """
    tasks = await GetTask.from_queryset(Task.all())
    return tasks


@task_router.post("/", dependencies=[Depends(dependency=get_current_user)], status_code=201)
async def post_task(body: PostTask):
    """
    Rota para criar uma nova tarefa.

    Recebe os dados de uma nova tarefa e a salva no banco de dados.

    Args:
        body (PostTask): Dados da nova tarefa.

    Returns:
        GetTask: Objeto da tarefa recém-criada.
    """
    print("Entrou na rota post_task")
    data = body.model_dump(exclude_unset=True)
    new_task = await Task.create(**data)
    return await GetTask.from_tortoise_orm(new_task)


@task_router.put("/{key}", dependencies=[Depends(dependency=get_current_user)])
async def update_task(key: int, body: PutTask):
    """
    Rota para atualizar uma tarefa existente.

    Verifica se a tarefa existe e, caso afirmativo, atualiza os dados fornecidos.

    Args:
        key (int): ID da tarefa a ser atualizada.
        body (PutTask): Dados para atualizar na tarefa.

    Returns:
        GetTask: Objeto da tarefa atualizada.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    data = body.model_dump(exclude_unset=True)
    exists_task = await Task.filter(id=key).exists()

    if not exists_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    await Task.filter(id=key).update(**data)
    return await GetTask.from_queryset_single(Task.get(id=key))


@task_router.delete("/{key}", dependencies=[Depends(dependency=get_current_user)])
async def delete_task(key: int):
    """
    Rota para deletar uma tarefa existente.

    Verifica se a tarefa existe e, caso afirmativo, a remove do banco de dados.

    Args:
        key (int): ID da tarefa a ser deletada.

    Returns:
        dict: Mensagem de confirmação da exclusão.

    Raises:
        HTTPException: Se a tarefa não for encontrada.
    """
    exists_task = await Task.filter(id=key).exists()

    if not exists_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    await Task.filter(id=key).delete()
    return {"message": "Tarefa deletada com sucesso"}
