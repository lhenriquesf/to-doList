from fastapi import FastAPI
from api.routes.task_routes import task_router
from api.routes.user_routes import user_router
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "https://frontend-todo-list-chi.vercel.app",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

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
