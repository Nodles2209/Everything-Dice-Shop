from flask import (Flask, render_template, redirect, url_for, request)
from sqlalchemy import asc, desc
import wtforms
from flask_wtf import FlaskForm

from create_app import InitApp
from instance.db.initDB import dbCheck
from instance.db.models import *
from forms import *

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
        all_items = ItemListing.query.all()

        return render_template('index.html', categories=getCategoryNames(), all_items=all_items)

    except Exception as e:
        error_text = "The error: " + str(e)
        return error_text


def getDatabaseQuery():
    # process query words and return relevant database query
    pass


@app.route('/all', methods=['POST'])
def search(query):
    # return render_template('allItems.html', query=query)
    pass


@app.route('/<string:category>')
def loadCategory(category):
    category_items = ItemListing.query \
        .join(ItemClassification, ItemListing.id_identifier == ItemClassification.id_identifier) \
        .filter_by(category_name=category).all()
    return render_template('loadCategory.html', category_items=category_items,
                           categories=getCategoryNames(),
                           category_name=category)


@app.route('/<int:item_id>', methods=['GET', 'POST'])
def loadItem(item_id):
    listing = ItemListing.query \
        .filter_by(listing_id=item_id) \
        .with_entities(ItemListing.listing_name,
                       ItemListing.listing_description,
                       ItemListing.thumbnail_img,
                       ItemListing.in_stock,
                       ItemListing.footprint,
                       ItemListing.num_of_reviews).first()

    item_options = ListingOptions.query \
        .filter_by(for_listing_id=item_id) \
        .with_entities(ListingOptions.option_name,
                       ListingOptions.option_price,
                       ListingOptions.option_img,
                       ListingOptions.option_inStock).all()

    form = OptionsForm()
    form.option.choices = [(option.option_name, option.option_name) for option in item_options]
    form.option.default = item_options[0].option_name

    if form.validate_on_submit():
        return redirect(url_for('homePage'))
    else:
        return render_template('singleItem.html',
                               item=listing,
                               categories=getCategoryNames(),
                               item_options=item_options,
                               form=form)


@app.route('/checkout')
def checkOut():
    # return render_template('checkout.html')
    pass


@app.route('/shoppingBasket')
def shoppingBasket():
    # return render_template('shoppingBasket.html')
    pass


if __name__ == '__main__':
    app.run(debug=True)
