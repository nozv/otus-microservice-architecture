import re
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User


class SUser(BaseModel):
    username: str = Field(...,min_length=1,max_length=50)
    firstname: str = Field()
    lastname: str = Field()
    email: EmailStr = Field()
    phone: str = Field()

    @validator("phone")
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError
        return value

class SUserGet(SUser):
    id: int = Field(default = None)

class SUserUpd(SUser):
    username: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

class UserDAO:
    model = User

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        try:
            users = await session.execute(select(cls.model))
            return users.scalars().all()
        except Exception as e:
            raise e
        
    @classmethod
    async def find_user_by_id(cls, user_id: int, session: AsyncSession):
        try:
            user = await session.get(cls.model, user_id)
            if user:
                return user
            else:
                raise IndexError
        except Exception as e:
            raise e
        
    @classmethod
    async def create_user(cls, user: SUser, session: AsyncSession):
        new_user = cls.model(username = user.username,
                            firstname = user.firstname,
                            lastname = user.lastname,
                            email = user.email,
                            phone = user.phone)
        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user.id
        except Exception as e:
            await session.rollback()
            raise e
            
    @classmethod
    async def update_user(cls, user_id: int, user: SUserUpd, session: AsyncSession):
        try:
            updated_user = await session.get(cls.model, user_id)
            if updated_user:
                for field,value in user.dict(exclude_unset = True, exclude={"id"}).items():
                    setattr(updated_user, field, value)
                await session.commit()
                return updated_user
            else:
                raise IndexError
        except Exception as e:
            await session.rollback()
            raise e
            
    @classmethod
    async def delete_user(cls, user_id: int, session: AsyncSession):
        try:
            user_to_del = await session.get(cls.model, user_id)
            if not user_to_del:
                raise IndexError
            await session.delete(user_to_del)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
