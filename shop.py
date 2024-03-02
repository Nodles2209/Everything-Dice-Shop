from flask import (Flask, render_template, redirect, url_for,
                   json, request)
from categories import item_json, home_display, all_categories

app = Flask(__name__)


@app.route('/')
def galleryPage():
    return render_template('index.html', categories=all_categories, home_display=home_display.items())


@app.route('/<string:category>')
def loadCategory(category):
    return render_template('loadCategory.html', category_items=item_json[category], categories=all_categories,
                           category_name=category)


@app.route('/<int:item_id>')
def loadItem(item_id):
    for item_category, item_list in item_json.items():
        for item in item_list:
            if item['id'] == item_id:
                return render_template('singleItem.html', item=item, categories=all_categories)
            # Include error handling


if __name__ == '__main__':
    app.run(debug=True)
