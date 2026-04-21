from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from services.schemas import User
from db.database import AsyncORM
from services.security import create_jwt_token, get_current_user, get_current_user_from_token
from services.encrypting import encrypt_password, email_validation
from typing import Annotated
from starlette import status

auth_router = APIRouter()

@auth_router.post("/registration")
async def registration(user: User):
    """
    Регистрация пользователя в базе данных с уникальным email
    """
    if user.password != user.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пароли не совпадают"
        )
    hashed_password = encrypt_password(user.password)
    email = email_validation(user.email)
    if email is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильный формат почты"
        )
    try:
        await AsyncORM.register_user(
            user.surname,
            user.name,
            hashed_password,
            user.email,
            user.role_id,
            user.is_active
        )
        return JSONResponse(content="Register successful!", status_code=201)
    except:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Произошла ошибка"
    )

@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_current_user(
        form_data.username, 
        form_data.password
    )
    token = create_jwt_token({
        "sub": str(user.user_id),
        "role": str(user.role_id),
    })
    return {
        "access_token": token,
        "token_type": "bearer",
    }

@auth_router.post("/logout")
async def logout(current_user: Annotated[User, Depends(get_current_user_from_token)]):
    if current_user:
        return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Вы вышли из аккаунта"
    )
    raise HTTPException(
        status_code=401,
        detail='Вы вышли из аккаунта'
    )
