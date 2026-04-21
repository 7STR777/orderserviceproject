from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    user_id: int
    surname: str
    name: str
    email: str
    password: str
    repeat_password: str
    role_id: int = 1
    is_active: bool = True

class UserLogin(BaseModel):
    email: str
    password: str
    
class ChangePassword(BaseModel):
    password: str
    new_password: str

class ChangeEmail(BaseModel):
    new_email: str

class ChangeCredentials(BaseModel):
    new_surname: Optional[str] = None
    new_name: Optional[str] = None

class DeleteUser(BaseModel):
    password: str
    repeat_password: str

class CreateProduct(BaseModel):
    product_name: str
    price: int
    amount: int

class UpdateFieldsOfProduct(BaseModel):
    new_product_name: Optional[str] = None
    new_price: Optional[int] = None
    new_amount: Optional[int] = None

class UpdateProduct(BaseModel):
    new_product_name: str
    new_amount: int
    new_price: int

class UpdateFieldOfPermission(BaseModel):
    role_id: Optional[int]
    business_element_id: Optional[int]
    read_permission: Optional[bool] = None
    read_all_permission: Optional[bool] = None
    create_permission: Optional[bool] = None
    update_permission: Optional[bool] = None
    update_all_permission: Optional[bool] = None
    delete_permission: Optional[bool] = None
    delete_all_permission: Optional[bool] = None
