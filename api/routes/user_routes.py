from api.auth import create_access_token, authenticate_user, Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas.user_schemas import UserCreate
from passlib.context import CryptContext
from api.models.user_models import User
from datetime import timedelta
from typing import Annotated

user_router = APIRouter(prefix="/auth", tags=["User"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


@user_router.post("/register", status_code=201)
async def register(user_data: UserCreate):
    user_exists = await User.filter(username=user_data.username).exists()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe",
        )

    hashed_password = get_password_hash(user_data.password)
    await User.create(username=user_data.username, password=hashed_password)
    
    return {"message": "Usuário registrado com sucesso"}


@user_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer")
