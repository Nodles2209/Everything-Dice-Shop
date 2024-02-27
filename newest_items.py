from init_items import load_items

all_items = load_items()
new_stock = []

for category, item_list in all_items.items():
    most_recent = item_list[-1]
    del most_recent['stock']
    del most_recent['sold']
    new_stock.append(most_recent)
