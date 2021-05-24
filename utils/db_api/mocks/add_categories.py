from utils.db_api.models import Category

sub_cats_2 = [
    {
        "name": "Universal-qush",
    }, {
        "name": "Premium-popugai",
    }
]
sub_cats_1 = [
    {
        "name": "Universal",
        "sub_cats": sub_cats_2
    }, {
        "name": "Premium",
    }
]
categories = [
    {
        "name": "Корм для кроликов",
        "sub_cats": sub_cats_1
    }, {
        "name": "Корм для домашних птиц"
    }
]


async def add_categories():
    for cat in categories:
        category = await Category.create_category(name=cat["name"])
        if "sub_cats" in cat:
            for sub_cat in cat["sub_cats"]:
                sub_category = await Category.create_category(name=sub_cat["name"], parent_id=category.id)
                if "sub_cats" in sub_cat:
                    for sub_cat_2 in sub_cat["sub_cats"]:
                        sub_sub_category = await Category.create_category(name=sub_cat_2["name"], parent_id=sub_category.id)
