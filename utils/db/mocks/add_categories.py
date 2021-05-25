import random
import string

from utils.db.models import Category

# sub_cats_2 = [
#     {
#         "name": "Universal-qush",
#     }, {
#         "name": "Premium-popugai",
#     }
# ]
# sub_cats_1 = [
#     {
#         "name": "Universal",
#         "sub_cats": sub_cats_2
#     }, {
#         "name": "Premium",
#     }
# ]
# categories = [
#     {
#         "name": "Корм для кроликов",
#         "sub_cats": sub_cats_1
#     }, {
#         "name": "Корм для домашних птиц"
#     }
# ]
#
#
# async def add_categories():
#     for cat in categories:
#         category = await Category.create_category(name=cat["name"])
#         if "sub_cats" in cat:
#             for sub_cat in cat["sub_cats"]:
#                 sub_category = await Category.create_category(name=sub_cat["name"], parent_id=category.id)
#                 if "sub_cats" in sub_cat:
#                     for sub_cat_2 in sub_cat["sub_cats"]:
#                         sub_sub_category = await Category.create_category(name=sub_cat_2["name"], parent_id=sub_category.id)
#
#


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


async def add_categories():
    for i in range(4):
        random_name = "Категория №" + str(i+1)
        await Category.create_category(name=random_name)