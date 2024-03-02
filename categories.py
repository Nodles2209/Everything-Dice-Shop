from highest_selling import best_seller
from newest_items import new_stock
from init_items import load_items

item_json = load_items()
all_categories = [category for category in item_json.keys()]
all_items = []
for item_list in item_json.values():
    for item in item_list:
        del item['stock']
        del item['sold']
        all_items.append(item)

home_display = {
    'Best sellers': best_seller,
    'New in stock': new_stock,
    'All items': all_items,
}
