from fastapi import FastAPI
from api.routes.task_routes import task_router
from api.routes.user_routes import user_router

from tortoise.contrib.fastapi import register_tortoise

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)

register_tortoise(
    app=app,
    db_url="sqlite://task.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models":["api.models.task_models", "api.models.user_models"]}
)


@app.get("/")
async def ler_root():
    return {"message": "Hello World"}
