from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated

from services.schemas import User, UpdateProduct, CreateProduct, UpdateFieldsOfProduct
from db.database import OrderData, AsyncORM, ProductData
from services.security import get_current_user_from_token


product_router = APIRouter()

@product_router.get("/products")
async def show_all_products(current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Показывает все продукты.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )
    permissions = await AsyncORM.get_permissions_by_role_id(current_user.role_id, 'products')
    if permissions[0].read_all_permission == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа"
        )
    products = await ProductData.show_all_products()
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Список пуст'
        )
    return permissions

@product_router.post("/products")
async def create_product(crpr: CreateProduct, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Создает продукт
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )
    permissions = await AsyncORM.get_permissions_by_role_id(current_user.role_id, 'products')
    if permissions[0].create_permission == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа"
        )
    try:
        await ProductData.create_product(crpr.product_name, crpr.price, crpr.amount)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось добавить товар"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=f"Товар {crpr.product_name} был успешно добавлен!"
    )

@product_router.get("/products/{product_id}")
async def show_product(product_id: int, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Показывает карточку продукта.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )
    product = await ProductData.show_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Список пуст'
        )
    return product


@product_router.patch("/products/{product_id}")
async def update_fields_product(product_id: int,updatepr: UpdateFieldsOfProduct, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Обновляет поля продукта
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )
    permissions = await AsyncORM.get_permissions_by_role_id(current_user.role_id, 'products')
    if permissions[0].update_permission == False and permissions[0].update_all_permission == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа"
        )
    update_data = updatepr.model_dump(exclude_none=True)
    field_mapping = {
    "new_product_name": "product_name",
    "new_amount": "amount",
    "new_price":"price"
    }
    raw_data = updatepr.model_dump(exclude_none=True)
    update_data = {
        field_mapping[key]: value
        for key, value in raw_data.items()
    }
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для обновления"
        )
    await ProductData.update_fields_of_product(product_id, update_data)
    return {"message": "Данные были успешно сохранены!"}


@product_router.put("/products/{product_id}")
async def update_product(product_id: int, updatepr: UpdateProduct, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Обновление продукта целиком
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )
    permissions = await AsyncORM.get_permissions_by_role_id(current_user.role_id, 'products')
    if permissions[0].update_permission == False and permissions[0].update_all_permission == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа"
        )
    await ProductData.update_product(product_id, updatepr.new_product_name, updatepr.new_amount, updatepr.new_price)
    return {"message": "Данные были успешно сохранены!"}


@product_router.delete("/products/{product_id}")
async def delete_product(product_id: int, current_user: Annotated[User, Depends(get_current_user_from_token)]):
    """
    Удаляет продукт по product_id
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )
    permissions = await AsyncORM.get_permissions_by_role_id(current_user.role_id, 'products')
    if permissions[0].delete_permission == False and permissions[0].delete_all_permission == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа"
        )
    await ProductData.delete_product(product_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Продукт был удален"
    )
    
