from init_items import load_items

all_items = load_items()
best_seller = []

for category, item_list in all_items.items():
    max_sold = 0
    max_item = item_list[0]
    for item in item_list:
        if item['sold'] > max_sold:
            max_sold = item['sold']
            max_item = item
    del max_item['stock']
    del max_item['sold']
    best_seller.append(max_item)
