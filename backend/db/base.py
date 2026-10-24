from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import DeclarativeBase


DB_URL = os.environ["POSTGRESQL_URL"]

engine = create_async_engine(DB_URL , pool_size = 5 , max_overflow = 10 , pool_pre_ping = True , echo = False)

asyncsession = async_sessionmaker(engine , class_= AsyncSession , expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with asyncsession() as session:
        yield session

