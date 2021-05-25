import random
import string

from utils.db.models import Item
from utils.db.models import Category


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_integer_price(length):
    result_str = str(random.randint(1, 9)) + ''.join(str(random.randint(0, length - 1)) for i in range(length))
    return int(result_str)


async def add_items():
    categories = await Category.all_parents()
    if len(categories) > 0:
        for i in range(50):
            random_name = "Товар №" + str(i+1)
            random_category_id = categories[random.randint(0, len(categories) - 1)].id
            random_price = get_integer_price(3)
            await Item.create_item(name=random_name, price=random_price, category_id=random_category_id)

