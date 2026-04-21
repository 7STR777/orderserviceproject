from db.models import Users, Roles, AccessRolesRules, BusinessElements, Products
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from db.config import settings
from db.base import Base
from services.encrypting import encrypt_password

async_engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=False)

async_session = async_sessionmaker(async_engine)

class ProductData():
    @staticmethod
    async def show_all_products():
        """
        Показывает все продукты
        """
        async with async_session() as session:
            stmt = select(Products)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return products
    
    @staticmethod
    async def show_product(product_id: int):
        """
        Показывает данные продукта
        """
        async with async_session() as session:
            stmt = select(Products).where(Products.product_id==product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()
            return product
        
    @staticmethod
    async def create_product(product_name: str, price: int, amount: int):
        async with async_session() as session:
            new_product = Products(
                product_name=product_name,
                price=price,
                amount=amount
            )
            session.add(new_product)
            await session.commit()
            print('[LOGS]: Product created!')

    @staticmethod
    async def update_fields_of_product(product_id: int, update_data: dict):
        async with async_session() as session:
            stmt = update(Products).where(Products.product_id==product_id).values(
                **update_data
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Fields of product updated!')

    @staticmethod
    async def update_product(product_id: int, product_name: str, amount: int, price: int):
        async with async_session() as session:
            stmt = update(Products).where(Products.product_id==product_id).values(
                product_name=product_name,
                amount=amount,
                price=price
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Product updated!')

    @staticmethod
    async def delete_product(product_id: int):
        async with async_session() as session:
            stmt = delete(Products).where(Products.product_id==product_id)
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Product deleted!')


class StaticData():
    @staticmethod
    async def add_test_roles():
        """
        Добавляет роли в БД
        """
        async with async_session() as session:
            stmt = insert(Roles).values(
                [
                    {"role_name":"user"},
                    {"role_name":"admin"},
                    {"role_name":"manager"},
                    {"role_name":"guest"},
                ]
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_test_users():
        """Добавляет тестовых пользователей с разными ролями"""
        async with async_session() as session:

            roles = await session.execute(select(Roles))
            roles = {r.role_name: r.role_id for r in roles.scalars()}

            data = [
                {
                    "surname": "Ivanov",
                    "name": "Ivan",
                    "email": "ivan@mail.com",
                    "password": encrypt_password("123"),
                    "role_id": roles["user"],
                    "is_active": True
                },
                {
                    "surname": "Petrov",
                    "name": "Petr",
                    "email": "admin@mail.com",
                    "password": encrypt_password("admin"),
                    "role_id": roles["admin"],
                    "is_active": True
                },
                {
                    "surname": "Sidorov",
                    "name": "Sergey",
                    "email": "manager@mail.com",
                    "password": encrypt_password("manager"),
                    "role_id": roles["manager"],
                    "is_active": True
                },
                {
                    "surname": "Guest",
                    "name": "Guest",
                    "email": "guest@mail.com",
                    "password": encrypt_password("guest"),
                    "role_id": roles["guest"],
                    "is_active": True
                },
            ]

            stmt = insert(Users).values(data)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_test_products():
        """Добавляет тестовые продукты"""
        async with async_session() as session:

            data = [
                {
                    "product_name": "Футболка",
                    "price": 3999,
                    "amount": 20
                },
                {
                    "product_name": "Штаны",
                    "price": 2499,
                    "amount": 45
                },
                {
                    "product_name": "Кроссовки",
                    "price": 7999,
                    "amount": 10
                },
                {
                    "product_name": "Кепка",
                    "price": 999,
                    "amount": 100
                },
            ]

            stmt = insert(Products).values(data)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_business_elements():
        """
        Добавляет бизнес-сущности
        """
        async with async_session() as session:
            stmt = insert(BusinessElements).values([
                {"business_element": "products"}
            ])
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_access_roles_rules():
        """Добавляет правила доступа"""
        async with async_session() as session:

            roles = await session.execute(select(Roles))
            roles = {r.role_name: r.role_id for r in roles.scalars()}

            elements = await session.execute(
                select(BusinessElements).where(BusinessElements.business_element == "products")
            )
            product_element = elements.scalar_one_or_none()

            if not product_element:
                raise Exception("Business element 'products' not found")

            data = [
                {
                    "role_id": roles["admin"],
                    "business_element_id": product_element.business_element_id,
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                },

                {
                    "role_id": roles["user"],
                    "business_element_id": product_element.business_element_id,
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": False,
                    "update_permission": False,
                    "update_all_permission": False,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },

                {
                    "role_id": roles["manager"],
                    "business_element_id": product_element.business_element_id,
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },

                {
                    "role_id": roles["guest"],
                    "business_element_id": product_element.business_element_id,
                    "read_permission": True,
                    "read_all_permission": False,
                    "create_permission": False,
                    "update_permission": False,
                    "update_all_permission": False,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },
            ]

            stmt = insert(AccessRolesRules).values(data)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_test_business_element():
        async with async_session() as session:
            stmt = insert(BusinessElements).values(
                {
                    "business_element":"orders"
                }
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_test_access_levels():
        async with async_session() as session:
            select_role = select(Roles.role_id).where(Roles.role_name=='user')
            result = await session.execute(select_role)
            role_id = result.scalar_one_or_none()

            select_business_element = select(BusinessElements.business_element_id).where(BusinessElements.business_element=='orders')
            result = await session.execute(select_business_element)
            business_element_id = result.scalar_one_or_none()

            stmt = insert(AccessRolesRules).values(
                [
                    {
                        "role_id":role_id,
                        "business_element_id": business_element_id,
                        "read_permission":True,
                        "read_all_permission":True,
                        "create_permission":False,
                        "update_permission":False,
                        "update_all_permission":False,
                        "delete_permission":False,
                        "delete_all_permission":False
                    }
                ]
            )
            await session.execute(stmt)
            await session.commit()

class AsyncORM():
    @staticmethod
    async def init_db():
        """
        Инициализирует БД в проекте
        """
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def register_user(surname: str, name: str, password:str, email: str, role_id: int, is_active: bool = True):
        """
        Регистрирует пользователя в базе данных.
        """
        async with async_session() as session:
            stmt_for_role_id = select(Roles.role_id).where(Roles.role_name=='user')
            result = await session.execute(stmt_for_role_id)
            role_id = result.scalar_one()

            stmt = insert(Users).values(
                surname = surname,
                name = name,
                password = password,
                email = email,
                role_id = role_id,
                is_active = is_active
            )
            await session.execute(stmt)
            await session.commit()
            print("[LOGS]:User was created!")

    @staticmethod
    async def get_user_from_email(email: str):
        async with async_session() as session:
            stmt = select(Users).where(Users.email==email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user != None:
                print(f"[LOGS]:User: {user} was found")
                return user
            return None

    @staticmethod
    async def get_user_by_id(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Users).where(Users.user_id == user_id)
            )
            user = result.scalar_one_or_none()
            return user

    @staticmethod
    async def update_user_password(user_id: int, new_password: str):
        async with async_session() as session:
            stmt = update(Users).where(Users.user_id==user_id).values(
                password=new_password
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Password updated!')

    @staticmethod
    async def update_user_email(user_id: int, new_email: str):
        async with async_session() as session:
            stmt = update(Users).where(Users.user_id==user_id).values(
                email=new_email
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Email updated!')

    @staticmethod
    async def update_user_credentials(user_id: int, update_data: dict):
        async with async_session() as session:
            stmt = update(Users).where(Users.user_id==user_id).values(
                **update_data
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Creds updated!')

    @staticmethod
    async def soft_delete_user(user_id: int):
        async with async_session() as session:
            stmt = update(Users).where(Users.user_id==user_id).values(
                is_active=False
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: User was soft deleted\n[LOGS]:Logout..')

    @staticmethod
    async def get_permissions_by_role_id(role_id: int, business_element: str):
        async with async_session() as session:
            stmt_for_elem = select(BusinessElements).where(
                BusinessElements.business_element == business_element
            )
            result = await session.execute(stmt_for_elem)
            element = result.scalar_one_or_none()
            
            if not element:
                return []  
            
            stmt = (
                select(AccessRolesRules)
                .where(
                    AccessRolesRules.role_id == role_id,
                    AccessRolesRules.business_element_id == element.business_element_id
                )
            )

            result = await session.execute(stmt)
            permissions = result.scalars().all()
            return permissions
    
    @staticmethod
    async def get_role_by_id(role_id: int):
        async with async_session() as session:
            stmt = select(Roles.role_name).where(Roles.role_id==role_id)
            result = await session.execute(stmt)
            role = result.scalar_one_or_none()
            return role
        
class AdminPanel():
    @staticmethod
    async def get_all_permissions():
        async with async_session() as session:
            stmt = select(AccessRolesRules)
            result = await session.execute(stmt)
            permissions = result.scalars().all()
            return permissions
        
    @staticmethod
    async def update_fields_of_permission(access_roles_rules_id: int, update_data: dict):
        async with async_session() as session:
            stmt = update(AccessRolesRules).where(AccessRolesRules.access_roles_rules_id==access_roles_rules_id).values(
                **update_data
            )
            await session.execute(stmt)
            await session.commit()
            print('[LOGS]: Fields of permission updated!')
        
    @staticmethod
    async def delete_permission(access_roles_rules_id: int):
        async with async_session() as session:
            stmt = delete(AccessRolesRules).where(AccessRolesRules.access_roles_rules_id==access_roles_rules_id)
            await session.execute(stmt)
            await session.commit()

