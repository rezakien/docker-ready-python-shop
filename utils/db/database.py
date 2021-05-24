from gino import Gino
from gino.schema import GinoSchemaVisitor
from config import POSTGRES_URI

db = Gino()


async def connect_db():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()
    await create_mocks()


async def create_mocks():
    from utils.db.mocks.add_categories import add_categories
    from utils.db.mocks.add_items import add_items
    await add_categories()
    await add_items()
