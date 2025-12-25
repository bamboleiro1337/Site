import asyncio
import asyncpg

async def test_conn():
    try:
        conn = await asyncpg.connect(
            user='your_user',
            password='your_password',
            database='your_db',
            host='127.0.0.1',  # замість localhost
            port=5432
        )
        print("Connected!")
        await conn.close()
    except Exception as e:
        print("Connection failed:", e)

asyncio.run(test_conn())
