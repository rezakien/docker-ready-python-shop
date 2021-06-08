import random
import string

from utils.db.models import Item, Category, Price



async def add_to_database():
    rabbit = await Category.create(name='Корм для кроликов 🐇')
    pet = await Category.create(name='Корм для птиц 🐓')

    rabbit_universal = await Category.create(name='Universal', parent_id=rabbit.id)
    rabbit_premium = await Category.create(name='Premium', parent_id=rabbit.id)

    item = await Item.create(name='Корм для кроликов Universal 🐇', category_id=rabbit_universal.id, photo='rabbit-universal.jpg', price=4600)
    await Price.create(item_id=item.id, min_quantity=100, max_quantity=475, price=4500)
    await Price.create(item_id=item.id, min_quantity=500, max_quantity=975, price=4400)
    await Price.create(item_id=item.id, min_quantity=1000, price=4300)

    item = await Item.create(name='Корм для кроликов Premium 🐇', category_id=rabbit_premium.id, photo='rabbit-premium.jpg', price=5300)
    await Price.create(item_id=item.id, min_quantity=100, max_quantity=475, price=5200)
    await Price.create(item_id=item.id, min_quantity=500, max_quantity=975, price=5100)
    await Price.create(item_id=item.id, min_quantity=1000, price=5000)

    item = await Item.create(name='Корм для домашних птиц 🐓', category_id=pet.id, photo='pets.jpg', price=4000)
    await Price.create(item_id=item.id, min_quantity=100, max_quantity=475, price=3900)
    await Price.create(item_id=item.id, min_quantity=500, max_quantity=975, price=3800)
    await Price.create(item_id=item.id, min_quantity=1000, price=3700)