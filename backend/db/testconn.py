import asyncio
from sqlalchemy import text
from base import engine

async def testConnection():
    try:
        async with engine.connect() as conn:
            res = await conn.execute(text("SELECT VERSION();"))
            version = res.scalar()
            print("Connected successfully")
            print(f"Postgres version : {version}")

            res2 = await conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';"))
            has_vec = res2.scalar()
            if has_vec:
                print("Vector extension found")
            else:
                print("Vector not initialised")

    except Exception as e:
        print("An error occured:" , e)


if __name__ == "__main__":
    asyncio.run(testConnection())
    

