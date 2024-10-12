from fastapi import APIRouter, HTTPException, status
from api.models.task_models import Task
from api.schemas.task_schemas import GetTask, PostTask, PutTask

task_router = APIRouter(prefix="/api", tags=["Task"])

@task_router.get("/")
async def get_task():
    data = Task.all()
    return await GetTask.from_queryset(data)

@task_router.post("/")
async def post_task(body:PostTask):
    row = await Task.create(**body.model_dump(exclude_unset=True))
    return await GetTask.from_tortoise_orm(row)


@task_router.put("/{key}")
async def update_task(key:int, body:PutTask):
    data = body.model_dump(exclude_unset=True)
    exists = await Task.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    await Task.filter(id=key).update(**data)
    return await GetTask.from_queryset_single(Task.get(id=key))


@task_router.delete("/{key}")
async def delete_task(key:int):
    exists = await Task.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    await Task.filter(id=key).delete()
    return "Tarefa deletada com sucesso"
