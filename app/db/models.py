from db.base import Base
from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import TIMESTAMP, ForeignKey, Column, Table, Integer


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.role_id'))
    is_active: Mapped[bool] = mapped_column(default=True)
    
    role: Mapped["Roles"] = relationship(back_populates="users")

class Roles(Base):
    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(unique=True)
    
    users: Mapped[List["Users"]] = relationship(back_populates="role")
    access_roles_rules: Mapped[List["AccessRolesRules"]] = relationship(back_populates="role")

class BusinessElements(Base):
    __tablename__ = 'business_elements'

    business_element_id: Mapped[int] = mapped_column(primary_key=True)
    business_element: Mapped[str] = mapped_column()

    access_roles_rules: Mapped[List["AccessRolesRules"]] = relationship(back_populates="business_element")

class AccessRolesRules(Base):
    __tablename__ = 'access_roles_rules'

    access_roles_rules_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.role_id'))
    business_element_id: Mapped[int] = mapped_column(ForeignKey('business_elements.business_element_id'))
    read_permission: Mapped[bool] = mapped_column()
    read_all_permission: Mapped[bool] = mapped_column()
    create_permission: Mapped[bool] = mapped_column()
    update_permission: Mapped[bool] = mapped_column()
    update_all_permission: Mapped[bool] = mapped_column()
    delete_permission: Mapped[bool] = mapped_column()
    delete_all_permission: Mapped[bool] = mapped_column()

    role: Mapped["Roles"] = relationship(back_populates="access_roles_rules")
    business_element: Mapped["BusinessElements"] = relationship(back_populates="access_roles_rules")
    

class OrderProductAssociation(Base):
    __tablename__ = 'order_product_association'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.order_id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=1)
    
    order: Mapped["Orders"] = relationship(back_populates="product_associations")
    product: Mapped["Products"] = relationship(back_populates="order_associations")


class Orders(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(primary_key=True)
    order_name: Mapped[str] = mapped_column(unique=True)
    
    product_associations: Mapped[List["OrderProductAssociation"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    @property
    def products(self):
        return [assoc.product for assoc in self.product_associations]


class Products(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(unique=True)
    price: Mapped[int] = mapped_column()
    amount: Mapped[int] = mapped_column()
    
    order_associations: Mapped[List["OrderProductAssociation"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )