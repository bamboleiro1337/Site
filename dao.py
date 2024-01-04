from sqlalchemy import delete, insert, select, update

from database import async_session_maker
from models import User


async def create_user(
        name: str,
        second_name: str,
        login: str,
        password: str,
        age: str,
        ip: str,
        city: str,
        country: str,
        region: str,
        is_admin: bool,

):
    
    async with async_session_maker() as session:

        query = insert(User).values(
            name=name,
            second_name=second_name,
            login=login,
            password=password,
            age=age,
            ip=ip,
            city=city,
            country=country,
            region=region,
            is_admin=is_admin,

        ).returning(User.id, User.login, User.name)


        print(query)
        data = await session.execute(query)
        await session.commit()
        
        return tuple(data)[0]



async def fetch_users(skip: int = 0, limit: int = 10):
    
    async with async_session_maker() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)

        return result.scalars().all()



async def get_user_by_id(user_id: int):

    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        print(query)
        result = await session.execute(query)

        return result.scalar_one_or_none()



async def get_user_by_login(user_login: str):

    async with async_session_maker() as session:
        query = select(User).filter_by(login=user_login)
        result = await session.execute(query)
        return result.scalar_one_or_none()



async def update_user(user_id: int):

    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(name='Olik')
        print(query)

        await session.execute(query)
        await session.commit(query)



async def delete_user(user_id: int):
    
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        print(query)

        await session.execute(query)
        await session.commit(query)





