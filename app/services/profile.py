from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from typing import Annotated
from app.services.security import get_current_user_from_token
from app.services.encrypting import email_validation, encrypt_password
from app.services.schemas import ChangePassword, User, ChangeEmail, ChangeCredentials, DeleteUser
from app.db.database import AsyncORM
import bcrypt

profile_router = APIRouter()


@profile_router.get("/me")
async def profile(user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Профиль пользователя
    """
    return user

@profile_router.patch("/password")
async def change_password(chpass: ChangePassword, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    if bcrypt.checkpw(chpass.password.encode('utf-8'), current_user.password.encode('utf-8')) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный пароль"
        )
    try:
        await AsyncORM.update_user_password(current_user.user_id, encrypt_password(chpass.new_password))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный пароль"
        )
    return {"message":"Password updated!"}

@profile_router.patch("/email")
async def change_email(chemail: ChangeEmail, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    if chemail.new_email == current_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Почта уже используется"
        )
    if email_validation(chemail.new_email) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильный формат почты"
        )
    await AsyncORM.update_user_email(current_user.user_id, chemail.new_email)
    return {"message":"Email updated!"}


@profile_router.patch("/credentials")
async def change_creds(creds: ChangeCredentials, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    update_data = creds.model_dump(exclude_none=True)
    field_mapping = {
    "new_name": "name",
    "new_surname": "surname"
    }
    raw_data = creds.model_dump(exclude_none=True)
    update_data = {
        field_mapping[key]: value
        for key, value in raw_data.items()
    }
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для обновления"
        )
    await AsyncORM.update_user_credentials(current_user.user_id, update_data)
    return {"message": "Данные были успешно сохранены!"}

@profile_router.delete("/delete")
async def soft_delete_user(deluser: DeleteUser, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    if deluser.password != deluser.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильный пароль"
        )
    await AsyncORM.soft_delete_user(current_user.user_id)
    return {"message":"Пользователь был удален"}