from flask import (Flask, render_template, redirect, url_for, request)
from sqlalchemy import asc, desc
from create_app import InitApp
from instance.db.models import *
from instance.db.initDB import dbCheck

app = InitApp()
dbCheck()


def getCategoryNames():
    all_categories = ItemClassification.query \
        .with_entities(ItemClassification.category_name) \
        .order_by(asc(ItemClassification.id_identifier)).all()
    all_categories = [category[0] for category in all_categories]

    return all_categories


@app.route('/faq')
def faq():
    # return render_template('faq.html', categories=all_categories
    pass


@app.route('/')
def homePage():
    try:
        all_items = ItemListing.query \
            .with_entities(ItemListing.listing_id,
                           ItemListing.listing_name,
                           ItemListing.avg_price,
                           ItemListing.thumbnail_img,
                           ItemListing.in_stock).all()

        return render_template('index.html', categories=getCategoryNames(), all_items=all_items)

    except Exception as e:
        error_text = "The error: " + str(e)
        return error_text


def getDatabaseQuery():
    # process query words and return relevant database query
    pass


@app.route('/search', methods=['POST'])
def search(query):
    # return render_template('search.html', query=query)
    pass


@app.route('/<string:category>')
def loadCategory(category):
    category_items = ItemListing.query \
        .join(ItemClassification, ItemListing.id_identifier == ItemClassification.id_identifier) \
        .filter_by(category_name=category).all()
    return render_template('loadCategory.html', category_items=category_items,
                           categories=getCategoryNames(),
                           category_name=category)


@app.route('/<int:item_id>')
def loadItem(item_id):
    # for item_category, item_list in item_json.items():
    #     for item in item_list:
    #        if item['id'] == item_id:
    #             return render_template('singleItem.html', item=item, categories=all_categories)
    pass


@app.route('/reviewThread')
def loadReviewThread():
    # load expanded review thread upon clicking on review link
    # return render_template('reviewThread.html')
    pass


@app.route('/checkout')
def checkOut():
    # return render_template('checkout.html')
    pass


@app.route('/shoppingBasket')
def shoppingBasket():
    # return render_template('shoppingBasket.html')
    pass


@app.route('/addToBasket')
def addToBasket():
    # displays page where you either
    # go to checkout
    # go to basket
    # go to item page
    # go to home page to search more items
    pass


if __name__ == '__main__':
    app.run(debug=True)
