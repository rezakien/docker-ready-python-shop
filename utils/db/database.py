from gino import Gino
from gino.schema import GinoSchemaVisitor
from config import PG_USER, PG_PASSWORD, PG_HOST, PG_CONTAINER_PORT, DATABASE

db = Gino()


async def connect_db():
    uri = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_CONTAINER_PORT}/{DATABASE}"
    await db.set_bind(uri)
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()
    await create_mocks()


async def create_mocks():
    from utils.db.mocks.add_to_database import add_to_database
    await add_to_database()
