from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await User.get_all(db=db)
    return users


@router.post("")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    user = await User.add_user(name=name, email=email, db=db)
    return user
