from fastapi import FastAPI,APIRouter
from services.auth import auth_router
from services.profile import profile_router
from services.orders import order_router
from services.products import product_router
from services.adminpanel import adminpanel_router
import asyncio
import uvicorn
from db.database import AsyncORM

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
    router=order_router,
    prefix="/orders",
    tags=["orders"]
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
    return {"message":"Main page"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
