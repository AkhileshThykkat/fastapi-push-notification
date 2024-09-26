from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

    @classmethod
    async def get_by_email(cls, email: str, db: AsyncSession):
        stmt = select(cls).where(cls.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_by_id(cls, user_id: int, db: AsyncSession):
        stmt = select(cls).where(cls.id == user_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def add_user(cls, name: str, email: str, db: AsyncSession):
        user = cls(name=name, email=email)
        db.add(user)
        await db.commit()
        return user

    @classmethod
    async def get_all(cls, db: AsyncSession):
        stmt = select(cls)
        result = await db.execute(stmt)
        users = result.scalars().all()
        return users


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<Case(id={self.id}, name={self.name}, user_id={self.user_id})>"

    @classmethod
    async def get_by_id(cls, case_id: int, db: AsyncSession):
        stmt = select(cls).where(cls.id == case_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def add_case(cls, name: str, user_id: int, db: AsyncSession):
        case = cls(name=name, user_id=user_id)
        db.add(case)
        await db.commit()
        return case

    @classmethod
    async def assign_case(cls, case_id: int, user_id: int, db: AsyncSession):
        case = await cls.get_by_id(case_id, db)
        case.assigned_to = user_id
        await db.commit()
        return case
