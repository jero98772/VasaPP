from os import environ
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from typing import AsyncGenerator

conn_string = environ["CONNECTION_STRING"]
engine = create_async_engine(conn_string, echo=True)
MyAsyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# this is to be used as a FastAPI dependency. You can sub it out for testing purposes!
async def get_session() -> AsyncGenerator:
    async with MyAsyncSession() as session:
        try:
            yield session
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise ex
        finally:
            await session.close()