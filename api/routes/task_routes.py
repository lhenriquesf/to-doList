from api.schemas.task_schemas import GetTask, PostTask, PutTask
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from api.redis_config import redis_client
from api.models.task_models import Task
from api.auth import get_current_user
import json

task_router = APIRouter(prefix="/api", tags=["Task"])

@task_router.get("/")
async def get_task():
    cached_tasks = redis_client.get("tasks")
    if cached_tasks:
        return json.loads(cached_tasks)
    
    tasks = await GetTask.from_queryset(Task.all())
    tasks_json = jsonable_encoder(tasks)
    redis_client.set("tasks", json.dumps(tasks_json))
    return tasks


@task_router.post("/",dependencies = [Depends(dependency=get_current_user)], status_code=201)
async def post_task(body: PostTask):
    print("Entrou na rota post_task")
    data = body.model_dump(exclude_unset=True)
    new_task = await Task.create(**data)
    
    updated_tasks = await GetTask.from_queryset(Task.all())
    updated_tasks_json = jsonable_encoder(updated_tasks)
    redis_client.set("tasks", json.dumps(updated_tasks_json))
    
    return await GetTask.from_tortoise_orm(new_task)


@task_router.put("/{key}", dependencies=[Depends(dependency=get_current_user)])
async def update_task(key: int, body: PutTask):
    data = body.model_dump(exclude_unset=True)
    exists_task = await Task.filter(id=key).exists()
    
    if not exists_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    
    await Task.filter(id=key).update(**data)

    updated_tasks = await GetTask.from_queryset(Task.all())
    updated_tasks_json = jsonable_encoder(updated_tasks)
    redis_client.set("tasks", json.dumps(updated_tasks_json))
    
    return await GetTask.from_queryset_single(Task.get(id=key))


@task_router.delete("/{key}", dependencies = [Depends(dependency=get_current_user)])
async def delete_task(key: int):
    exists_task = await Task.filter(id=key).exists()
    
    if not exists_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
 
    await Task.filter(id=key).delete()

    updated_tasks = await GetTask.from_queryset(Task.all())
    updated_tasks_json = jsonable_encoder(updated_tasks)
    redis_client.set("tasks", json.dumps(updated_tasks_json))
    
    return {"message": "Tarefa deletada com sucesso"}
