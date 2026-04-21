from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated

from services.schemas import User, UpdateFieldOfPermission
from db.database import AdminPanel
from services.security import get_current_user_from_token, admin_required


adminpanel_router = APIRouter()

@adminpanel_router.get("/showallpermissions")
@admin_required
async def get_all_permissions(current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Показывает все разрешения для пользователей
    """
    permissions = await AdminPanel.get_all_permissions()
    if permissions[0].read_all_permission == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа"
        )
    return permissions

@adminpanel_router.patch("/updatepermission")
@admin_required
async def update_field_of_permission(access_roles_rules_id: int, updateper: UpdateFieldOfPermission, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Обновляет поля разрешений
    """
    update_data = updateper.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для обновления"
        )
    await AdminPanel.update_fields_of_permission(access_roles_rules_id, update_data)
    return {"message": "Данные были успешно сохранены!"}

@adminpanel_router.delete("/deletepermission/{access_roles_rules_id}")
@admin_required
async def delete_permission(access_roles_rules_id: int, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """Удаляет разрешение"""
    try:
        await AdminPanel.delete_permission(access_roles_rules_id)
    except:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Произошла ошибка при удалении"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Разрешение было удалено"
    )