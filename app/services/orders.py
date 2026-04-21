from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated

from services.schemas import User 
from db.database import OrderData, AsyncORM
from services.security import get_current_user_from_token


order_router = APIRouter()

