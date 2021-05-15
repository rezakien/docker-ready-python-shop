import asyncio
import asyncpg
import logging

from config import HOST, PG_USER, PG_PASSWORD

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def create_db():
    create_db_command = open("sql/create_db.sql", "r").read()

    logging.info("Connection to db")
    conn: asyncpg.Connection = await asyncpg.connect(
        user=PG_USER,
        password=PG_USER,
        host=HOST
    )
    await conn.execute(create_db_command)
    logging.info("Table has been created")
    await conn.close()


async def create_pool():
    return await asyncpg.create_pool(
        user=PG_USER,
        password=PG_USER,
        host=HOST
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())