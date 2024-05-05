from flask import (Flask, render_template, redirect, url_for, request, session)
from sqlalchemy import asc, desc

from create_app import InitApp
from instance.db.initDB import dbCheck
from instance.db.sqlalchemyDB import db
from profile_manager import *
from instance.db.models import *
from forms import *

app = InitApp()
dbCheck()


def addItemToBasketDB(userID, option_id, quantity):
    basket_id = UserBasket.query \
        .filter_by(basket_user_id=userID) \
        .with_entities(UserBasket.basket_id).first()

    basket_item = BasketItem(for_basket_id=basket_id,
                             option_id=option_id,
                             quantity=quantity)

    db.session.add(basket_item)
    db.session.commit()


def getCategoryNames():
    all_categories = ItemClassification.query \
        .with_entities(ItemClassification.category_name) \
        .order_by(asc(ItemClassification.id_identifier)).all()
    all_categories = [category[0] for category in all_categories]

    return all_categories


def getAllItems():
    all_items = ItemListing.query.all()
    return all_items


def getAccountSettings(isAnon):
    account_settings = AccountSettings.query \
        .with_entities(AccountSettings.setting_option) \
        .filter_by(is_anon=int(isAnon)).all()

    return [settings[0] for settings in account_settings]


def checkSessionDefaults():
    if 'isAnon' not in session or 'user_id' not in session:
        app.logger.info("Currently in an anonymous session...")
        session['isAnon'] = True

    if 'basket' not in session:
        app.logger.info("Creating session basket...")
        session['basket'] = []

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


@app.route('/faq')
def faq():
    # return render_template('faq.html', categories=all_categories
    pass


@app.route('/')
def homePage():
    checkSessionDefaults()
    app.logger.info("Account settings: " + str(session['account_settings']))

    try:
        best_sellers = ItemListing.query \
            .order_by(desc(ItemListing.sold)) \
            .limit(4).all()

        new_stock = ItemListing.query \
            .order_by(desc(ItemListing.date_added)) \
            .limit(4).all()

        all_items = getAllItems()[:3]

        return render_template('index.html',
                               sections=[('Best Sellers', best_sellers),
                                         ('New in Stock', new_stock),
                                         ('All Items', all_items)],
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])

    except Exception as e:
        error_text = "The error: " + str(e)
        return error_text


def getDatabaseQuery(filter_by='all', order_by='asc', show_sold=False):
    # process query words and return relevant database query
    pass


@app.route('/<string:category>')
def loadCategory(category):
    if category == "All Items":
        category_items = getAllItems()
    else:
        category_items = ItemListing.query \
            .join(ItemClassification, ItemListing.id_identifier == ItemClassification.id_identifier) \
            .filter_by(category_name=category).all()

    return render_template('loadCategory.html', category_items=category_items,
                           category_name=category,
                           categories=getCategoryNames(),
                           account_settings=session['account_settings'])


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
    if option_default:
        form.option.default = option_default
    else:
        form.option.default = (item_options[0].option_id, item_options[0].option_name)

    if form.validate_on_submit():
        if not session['isAnon']:
            addItemToBasketDB(session['user_id'],
                              form.option.data,
                              form.quantity.data)

        session['basket'] += [{'option_id': form.option.data,
                               'quantity': form.quantity.data}]

        return redirect(url_for('basket'))

    else:
        return render_template('singleItem.html',
                               item=listing,
                               item_options=item_options,
                               form=form,
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])


def clearBasketDB(userID):
    basket_id = UserBasket.query \
        .filter_by(basket_user_id=userID) \
        .with_entities(UserBasket.basket_id).first()

    BasketItem.query \
        .filter_by(for_basket_id=basket_id) \
        .delete()

    db.session.commit()


def updateItemQuantity(userID, option_id, quantity):
    basket_id = UserBasket.query \
        .filter_by(basket_user_id=userID) \
        .with_entities(UserBasket.basket_id).first()

    basket_item = BasketItem.query \
        .filter_by(for_basket_id=basket_id,
                   option_id=option_id).first()

    basket_item.quantity = quantity
    db.session.commit()


def getBasketDB(userID):
    basket_id = UserBasket.query \
        .filter_by(basket_user_id=userID) \
        .with_entities(UserBasket.basket_id).first()

    basket_items = BasketItem.query \
        .filter_by(for_basket_id=basket_id) \
        .with_entities(BasketItem.option_id,
                       BasketItem.quantity).all()

    return basket_items


def getBasketDisplay(isAnon, basketItems):
    basket_display = []

    for item in basketItems:
        if isAnon:
            option_id = item['option_id']
            quantity = item['quantity']
        else:
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

        basket_display += [{'listing_id': option_listing_id[0],
                            'listing_name': listing_info.listing_name,
                            'listing_img': listing_info.thumbnail_img,
                            'option_id': option_id,
                            'option_name': option_info.option_name,
                            'option_price': option_info.option_price,
                            'quantity': quantity}]

    return basket_display


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    app.logger.info("Basket: " + str(session['basket']))

    if session['isAnon']:
        basket_display = getBasketDisplay(session['isAnon'], session['basket'])

    else:
        basket_display = getBasketDisplay(session['isAnon'], getBasketDB(session['user_id']))

    app.logger.info("Basket Display: " + str(basket_display))

    total_price = sum([item['option_price'] for item in basket_display])

    form = ShoppingBasketForm()

    if form.clear.data:
        session['basket'] = []

        if not session['isAnon']:
            clearBasketDB(session['user_id'])

        return redirect(url_for('basket'))

    if form.validate_on_submit():
        return redirect(url_for('checkOut', final_basket=basket_display))
    else:
        return render_template('basket.html',
                               basket=basket_display,
                               total_price=total_price,
                               form=form,
                               categories=getCategoryNames(),
                               account_settings=session['account_settings'])


def getUserPaymentMethods():
    payment_methods = []

    user_payment_methods = UserBillingInfo.query \
        .filter_by(id=session['user_id']) \
        .with_entities(UserBillingInfo.payment_method).all()

    all_user_payment_methods = []

    for payment_method in user_payment_methods:
        all_user_payment_methods += [PaymentMethod.query
                                     .filter_by(details_id=payment_method.payment_method).all()]

    payment_display = []

    for payment_method in all_user_payment_methods:
        if payment_method[0].payment_type == "card":
            payment_display += [f"Card ending in {int(str(payment_method[0].card_num)[-4:])}"]
        elif payment_method[0].payment_type == "online":
            if payment_method[0].paypal_email:
                payment_display += [f"{payment_method[0].merchant_name} account {payment_method[0].email}"]
            else:
                payment_display += [f"{payment_method[0].merchant_name} account {payment_method[0].username}"]

    for i in range(len(payment_display)):
        payment_methods += [(all_user_payment_methods[i], payment_display[i])]

    return payment_methods


@app.route('/checkout/', methods=['GET', 'POST'])
def checkOut():
    if not session['isAnon']:
        session['basket'] = getBasketDB(session['user_id'])
    final_basket = getBasketDisplay(session['isAnon'], session['basket'])

    total_price = sum([item['option_price'] for item in final_basket])
    app.logger.info("Final basket: " + str(final_basket))

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
        payment_methods += getUserPaymentMethods()

    checkout_form.payment_method.choices = payment_methods

    if checkout_form.validate_on_submit():
        return redirect(url_for('invoice'))

    return render_template('checkout.html',
                           final_basket=final_basket,
                           total_price=total_price,
                           form=checkout_form,
                           categories=getCategoryNames(),
                           account_settings=session['account_settings'])


@app.route('/checkout/invoice')
def invoice():

    if 'invoice' not in session:
        if not session['isAnon']:
            create_invoice = Invoices(session['user_id'])
            clearBasketDB(session['user_id'])
        else:
            create_invoice = Invoices()
            session['basket'] = []
        db.session.add(create_invoice)
        db.session.commit()

        session['invoice'] = create_invoice.invoice_id

    app.logger.info("Invoice: " + str(session['invoice']))

    return render_template('invoice.html',
                           invoice_number=session['invoice'],
                           categories=getCategoryNames(),
                           account_settings=session['account_settings'])


if __name__ == '__main__':
    app.run(debug=True)
