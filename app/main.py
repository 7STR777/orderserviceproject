from fastapi import FastAPI,APIRouter
from services.auth import auth_router
from services.profile import profile_router
from services.products import product_router
from services.adminpanel import adminpanel_router
import asyncio
import uvicorn
from db.database import AsyncORM, StaticData

app = FastAPI()
app.include_router(
    router=auth_router,
    prefix="/auth",
    tags=['auth']
)

app.include_router(
    router=profile_router,
    prefix="/profile",
    tags=["profile"]
)

app.include_router(
    router=product_router,
    prefix="/content",
    tags=['products']
)

app.include_router(
    router=adminpanel_router,
    prefix="/adminpanel",
    tags=["adminpanel"]
)

@app.get("/refreshdb", tags=['database'])
async def main():
    await AsyncORM.init_db()
    await StaticData.add_test_roles()
    await StaticData.add_business_elements()
    await StaticData.add_test_users()
    await StaticData.add_test_products()
    await StaticData.add_access_roles_rules()
    return {"message":"Database refreshed!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
