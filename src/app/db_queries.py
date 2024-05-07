from instance.db.sqlalchemyDB import db
from sqlalchemy import asc, desc

from instance.db.models import *


def getBasketIDFromUserID(userID):
    return UserBasket.query \
        .filter_by(basket_user_id=userID) \
        .with_entities(UserBasket.basket_id).first()


def addItemToBasketDB(userID, option_id, quantity):
    basket_id = getBasketIDFromUserID(userID)

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


def getDatabaseQuery(category, filter_by, order_by, show_sold):

    print(category, filter_by, order_by, show_sold)

    if category == "all":
        if order_by == 'asc':
            if show_sold:
                query_items = ItemListing.query \
                    .order_by(asc(filter_by)).all()
            else:
                query_items = ItemListing.query \
                    .filter_by(in_stock=int(show_sold)) \
                    .order_by(asc(filter_by)).all()
        else:
            if show_sold:
                query_items = ItemListing.query \
                    .order_by(desc(filter_by)).all()
            else:
                query_items = ItemListing.query \
                    .filter_by(in_stock=int(show_sold)) \
                    .order_by(desc(filter_by)).all()
    else:
        id_identifier = ItemClassification.query \
            .with_entities(ItemClassification.id_identifier) \
            .filter_by(category_name=category).first()

        if order_by == 'asc':
            if show_sold:
                query_items = ItemListing.query \
                    .filter_by(id_identifier=id_identifier[0]) \
                    .order_by(asc(filter_by)).all()
            else:
                query_items = ItemListing.query \
                    .filter_by(id_identifier=id_identifier[0], in_stock=int(show_sold)) \
                    .order_by(asc(filter_by)).all()
        else:
            if show_sold:
                query_items = ItemListing.query \
                    .filter_by(id_identifier=id_identifier[0]) \
                    .order_by(desc(filter_by)).all()
            else:
                query_items = ItemListing.query \
                    .filter_by(id_identifier=id_identifier[0], in_stock=int(show_sold)) \
                    .order_by(desc(filter_by)).all()

    return query_items


def deleteItemFromBasketDB(user_id, data):
    basket_id = getBasketIDFromUserID(user_id)

    BasketItem.query \
        .filter_by(for_basket_id=basket_id,
                   option_id=data).delete()

    db.session.commit()


def clearBasketDB(userID):
    basket_id = getBasketIDFromUserID(userID)

    BasketItem.query \
        .filter_by(for_basket_id=basket_id) \
        .delete()

    db.session.commit()


def updateItemQuantity(userID, option_id, quantity):
    basket_id = getBasketIDFromUserID(userID)

    basket_item = BasketItem.query \
        .filter_by(for_basket_id=basket_id,
                   option_id=option_id).first()

    basket_item.quantity = quantity
    db.session.commit()


def getBasketDB(userID):
    basket_id = getBasketIDFromUserID(userID)

    basket_items = BasketItem.query \
        .filter_by(for_basket_id=basket_id) \
        .with_entities(BasketItem.option_id,
                       BasketItem.quantity).all()

    return basket_items


def getUserPaymentMethods(user_id):
    payment_methods = []

    user_payment_methods = UserBillingInfo.query \
        .filter_by(id=user_id) \
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


def get_price_by_option_id(option_id):
    price = ListingOptions.query \
        .filter_by(option_id=option_id) \
        .with_entities(ListingOptions.option_price).first()

    return price[0]
