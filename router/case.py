from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import Case
from websocket_manager import wsok_manager,redis_manager
from schema import PushNotificationInput

router = APIRouter(prefix="/case", tags=["cases"])


@router.get("")
async def get_all_cases(db: AsyncSession = Depends(get_db)):
    stmt = select(Case)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("")
async def create_case(name: str, db: AsyncSession = Depends(get_db)):
    case = Case(name=name)
    db.add(case)
    await db.commit()
    return case


@router.put("/assign_to")
async def assign_case(case_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    assigned = await Case.assign_case(case_id, user_id, db)
    try:
        await wsok_manager.personal_message(
        message=PushNotificationInput(message="Case assigned to you", user_id=user_id)
        )
    except RuntimeError as e:
        await redis_manager.store_message(user_id=user_id,message="Case assigned to you")
    return assigned
