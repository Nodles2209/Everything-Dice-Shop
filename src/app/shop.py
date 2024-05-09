from flask import (Flask, render_template, redirect, url_for, request, session)

from create_app import InitApp, csrf
from instance.db.initDB import dbCheck
from instance.db.sqlalchemyDB import db
from profile_manager import *
from forms import *
from db_queries import *

app = InitApp()
dbCheck()


def checkSessionDefaults():
    if 'isAnon' not in session or 'user_id' not in session:
        app.logger.info("Currently in an anonymous session...")
        session['isAnon'] = True

    if 'basket' not in session:
        app.logger.info("Creating session basket...")
        session['basket'] = []
        session['basket_item_num'] = 1

    if not session['isAnon'] and 'user_id' in session:
        basket_exists = UserBasket.query \
            .filter_by(basket_user_id=session['user_id']).exists()

        if not basket_exists:
            app.logger.info("Creating user basket...")
            newBasket = UserBasket(basket_user_id=session['user_id'])
            db.session.add(newBasket)
            db.session.commit()

        if session['basket']:
            app.logger.info("Setting basket...")
            for item in session['basket']:
                addItemToBasketDB(session['user_id'], item['option_id'], item['quantity'])

    if 'account_settings' not in session or session['account_settings'] == []:
        app.logger.info("Setting account settings...")
        session['account_settings'] = getAccountSettings(session['isAnon'])


@app.route('/get_price/<int:option_id>', methods=['GET'])
def get_price(option_id):
    price = get_price_by_option_id(option_id)

    return str(price)


@app.route('/')
def homePage():
    checkSessionDefaults()
    app.logger.info("Account settings: " + str(session['account_settings']))

    best_sellers = ItemListing.query \
        .order_by(desc(ItemListing.sold)) \
        .limit(4).all()

    new_stock = ItemListing.query \
        .order_by(desc(ItemListing.date_added)) \
        .limit(4).all()

    all_items = getAllItems()[:4]

    return render_template('index.html',
                           sections=[('Best Sellers', best_sellers),
                                     ('New in Stock', new_stock),
                                     ('All Items', all_items)],
                           categories=getCategoryNames(),
                           account_settings=session['account_settings'])


@app.route('/<string:category>', methods=['GET', 'POST'])
def loadCategory(category):
    if category == "All Items":
        category_items = getAllItems()
        sort_form = SortForm()
    else:
        category_items = ItemListing.query \
            .join(ItemClassification, ItemListing.id_identifier == ItemClassification.id_identifier) \
            .filter_by(category_name=category).all()
        sort_form = CategorySortForm()

    if request.method == "POST":
        if category == "All Items":
            category_items = getDatabaseQuery(sort_form.category.data,
                                              sort_form.sort_by.data,
                                              sort_form.order_by.data,
                                              sort_form.show_sold.data)
        else:
            category_items = getDatabaseQuery(category,
                                              sort_form.sort_by.data,
                                              sort_form.order_by.data,
                                              sort_form.show_sold.data)

        return render_template('loadCategory.html',
                               category_items=category_items,
                               category_name=category,
                               form=sort_form,
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])
    else:
        return render_template('loadCategory.html',
                               category_items=category_items,
                               category_name=category,
                               form=sort_form,
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])


def getFreeBasketID():
    free_basket_item_num = session['basket_item_num']
    session['basket_item_num'] += 1
    return free_basket_item_num


@app.route('/<int:item_id>', methods=['GET', 'POST'])
def loadItem(item_id, option_default=None):
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
        .with_entities(ListingOptions.option_id,
                       ListingOptions.option_name,
                       ListingOptions.option_price,
                       ListingOptions.option_img,
                       ListingOptions.option_inStock).all()

    form = OptionsForm()
    form.option.choices = [(option.option_id, option.option_name) for option in item_options]
    form.price.default = item_options[0].option_price

    if option_default:
        form.option.default = option_default
    else:
        form.option.default = (item_options[0].option_id, item_options[0].option_name)

    if request.method == "POST":
        if not session['isAnon']:
            addItemToBasketDB(session['user_id'],
                              form.option.data,
                              form.quantity.data)

        session['basket'] += [{'basket_item_num': getFreeBasketID(),
                               'option_id': form.option.data,
                               'quantity': form.quantity.data}]

        return redirect(url_for('basket'))

    else:
        return render_template('singleItem.html',
                               item=listing,
                               item_options=item_options,
                               form=form,
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])


def getBasketDisplay(isAnon, basketItems):
    basket_display = []

    for item in basketItems:
        if isAnon:
            basket_item_num = item['basket_item_num']
            option_id = item['option_id']
            quantity = item['quantity']
        else:
            basket_item_num = item.basket_item_num
            option_id = item.option_id
            quantity = item.quantity

        option_listing_id = ListingOptions.query \
            .filter_by(option_id=option_id) \
            .with_entities(ListingOptions.for_listing_id).first()

        listing_info = ItemListing.query \
            .filter_by(listing_id=option_listing_id.for_listing_id) \
            .with_entities(ItemListing.listing_name,
                           ItemListing.thumbnail_img).first()

        option_info = ListingOptions.query \
            .filter_by(option_id=option_id) \
            .with_entities(ListingOptions.option_name,
                           ListingOptions.option_price).first()

        basket_display += [{'basket_item_num': basket_item_num,
                            'listing_id': option_listing_id[0],
                            'listing_name': listing_info.listing_name,
                            'listing_img': listing_info.thumbnail_img,
                            'option_id': option_id,
                            'option_name': option_info.option_name,
                            'option_price': option_info.option_price,
                            'quantity': quantity}]

    return basket_display


@app.route('/basket/update/<int:option_id>', methods=['GET', 'POST'])
@csrf.exempt
def updateItemInBasket(option_id):
    quantity = request.form.get('quantity')
    basket_item_num = request.form.get('basket_item_num')

    if not session['isAnon']:
        updateItemQuantity(session['user_id'], option_id, quantity)
    else:
        for index, item in enumerate(session['basket']):
            if item['option_id'] == option_id and item['basket_item_num'] == basket_item_num:
                item['quantity'] = quantity
                session.modified = True

    print(session['basket'], flush=True)

    return 'ok'


@app.route('/basket/delete/<int:basket_item_num>', methods=['GET', 'POST'])
def deleteItemFromBasket(basket_item_num):
    if not session['isAnon']:
        deleteItemFromBasketDB(session['user_id'], basket_item_num)
    else:
        session['basket'] = [item for item in session['basket'] if item['basket_item_num'] != basket_item_num]

    return redirect(url_for('basket'))


@app.route('/basket', methods=['GET', 'POST'])
def basket():

    if 'invoice' in session or 'invoice_items' in session:
        session.pop('invoice')
        session.pop('invoice_items')

    print(session['basket'])
    if session['isAnon']:
        basket_display = getBasketDisplay(session['isAnon'], session['basket'])

    else:
        basket_display = getBasketDisplay(session['isAnon'], getBasketDB(session['user_id']))

    app.logger.info("Basket Display: " + str(basket_display))

    total_price = sum([(item['option_price'] * item['quantity']) for item in basket_display])

    update_item_form = BasketItemForm()
    form = ShoppingBasketForm()

    if form.clear.data:
        session['basket'] = []
        session['basket_item_num'] = 0

        if not session['isAnon']:
            clearBasketDB(session['user_id'])

        return redirect(url_for('basket'))

    if request.method == "POST":
        return redirect(url_for('checkOut'))
    else:
        return render_template('basket.html',
                               basket=basket_display,
                               total_price=total_price,
                               item_form=update_item_form,
                               form=form,
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])


@app.route('/checkout/', methods=['GET', 'POST'])
def checkOut():
    country_choices = CountryList.query.all()
    country_names = [(country.country_id, country.country_name) for country in country_choices]

    display_area_codes = [(country.area_code, f"{country.country_name} +{country.area_code}") for country in
                          country_choices]

    checkout_form = CheckoutForm()
    checkout_form.country.choices = country_names
    checkout_form.phone_area_code.choices = display_area_codes
    checkout_form.country.default = (1, "United Kingdom")
    checkout_form.phone_area_code.default = (44, "United Kingdom +44")

    payment_methods = [(0, "Add new payment method")]

    if not session['isAnon']:
        payment_methods += getUserPaymentMethods(session['user_id'])

    checkout_form.payment_method.choices = payment_methods

    if request.method == "POST":
        return redirect(url_for('invoice'))

    return render_template('checkout.html',
                           form=checkout_form,
                           categories=getCategoryNames(),
                           account_settings=session['account_settings'])


@app.route('/checkout/invoice')
def invoice():
    if 'invoice' not in session:
        if not session['isAnon']:
            create_invoice = Invoices(session['user_id'])

            # edit the number of items in listing_stock
            # potentially add carousel for image gallery for single items

            clearBasketDB(session['user_id'])
        else:
            create_invoice = Invoices()

        db.session.add(create_invoice)
        db.session.commit()
        session['invoice'] = create_invoice.invoice_id

        session['invoice_items'] = session['basket']

    invoice_items = getBasketDisplay(session['isAnon'], session['invoice_items'])
    total_price = sum([(item['option_price'] * item['quantity']) for item in invoice_items])

    session['basket'] = []
    session['basket_item_num'] = 0

    app.logger.info("Invoice: " + str(session['invoice']))
    app.logger.info("Invoice items: " + str(invoice_items))

    return render_template('invoice.html',
                           invoice_number=session['invoice'],
                           basket=invoice_items,
                           total_price=total_price,
                           categories=getCategoryNames(),
                           account_settings=session['account_settings'])


if __name__ == '__main__':
    app.run(debug=True, port=5050)
