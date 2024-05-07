import datetime
import os
import random

from flask import json

from paths import jsonPath
from instance.db.models import *
from instance.db.sqlalchemyDB import db
from instance.db import getDBLocation
from src.app.create_app import InitApp

app = InitApp()


def createAppDB():
    with app.app_context():
        db.create_all()


def initLookupTables():
    lookup_file = os.path.join(jsonPath, 'reference_tables.json')
    lookup_data = json.load(open(lookup_file, encoding='utf-8'))

    for classification in lookup_data["Item classifications"]:
        newCategory = ItemClassification(id_identifier=classification["id_identifier"],
                                         category_name=classification["category_name"])
        db.session.add(newCategory)

    for country in lookup_data["Country list"]:
        newCountry = CountryList(country_name=country["country_name"],
                                 area_code=country["area_code"])
        db.session.add(newCountry)

    for vendor in lookup_data["Card classification"]:
        newVendor = CardClassification(card_identifier=vendor["card_identifier"],
                                       card_type=vendor["card_type"])
        db.session.add(newVendor)

    for setting in lookup_data["Account settings"]:
        for option in setting["setting_options"]:
            newOption = AccountSettings(setting_option=option,
                                        is_anon=setting["is_anon"])
            db.session.add(newOption)


def initInvoices():
    invoice_start_id = random.randint(100000, 200000)
    invoice_nums = random.randint(0, 200)

    new_invoice = Invoices(invoice_id=invoice_start_id)
    db.session.add(new_invoice)

    for i in range(invoice_nums):
        new_invoice = Invoices()
        db.session.add(new_invoice)


def initOptions(item, table_for, newListing):
    for index in range(len(table_for["option_id"])):
        newOption = ListingOptions(for_listing_id=item["listing_id"],
                                   option_img=table_for["option_img"][index],
                                   option_name=table_for["option_name"][index],
                                   option_price=table_for["option_price"][index],
                                   option_stock=table_for["option_stock"][index],
                                   option_sold=table_for["option_sold"][index],
                                   option_inStock=table_for["option_inStock"][index])
        newListing.options.append(newOption)


def initReviewsAndReplies(item, table_for, newListing):
    for index in range(len(table_for["review_id"])):
        newReview = ListingReviews(review_id=table_for["review_id"][index],
                                   listing_id=item["listing_id"],
                                   review_user_id=table_for["review_user_id"][index],
                                   review_title=table_for["review_title"][index],
                                   review_text=table_for["review_text"][index],
                                   review_rating=table_for["review_rating"][index],
                                   num_of_replies=table_for["num_of_replies"][index])

    table_for = item["replies"]
    for index in range(len(table_for["reply_id"])):
        newReply = ReviewReplies(reply_id=table_for["reply_id"][index],
                                 reply_user_id=table_for["reply_user_id"][index],
                                 under_review_id=table_for["review_id"][index],
                                 reply_text=table_for["reply_text"][index])
        newReview.replies.append(newReply)
        newListing.reviews.append(newReview)
        db.session.add(newReply)
        db.session.add(newReview)


def initBillingAndPayment(item, table_for, newListing):
    for index in range(len(table_for["billing_id"])):
        newBilling = ListingBillingInfo(address_1=table_for["address_1"][index],
                                        address_2=table_for["address_2"][index],
                                        address_3=table_for["address_3"][index],
                                        city=table_for["city"][index],
                                        postcode=table_for["postcode"][index],
                                        country_id=table_for["country_id"][index],
                                        state=table_for["state"][index],
                                        phone_area_code=table_for["phone_area_code"][
                                            index],
                                        phone_num=table_for["phone_num"][index],
                                        payment_method=table_for["payment_method"][index],
                                        billing_type="listing",
                                        listing_id=item["listing_id"])

    table_for = item["payment_method"]
    for index in range(len(table_for["payment_method"])):
        newPaymentMethod = CreditCardDetails(payment_type=table_for["transaction_type"][
            index],
                                             identifier=table_for["card_identifier"][
                                                 index],
                                             card_num=table_for["card_num"][index],
                                             expiry_date=datetime.datetime.fromisoformat(
                                                 table_for["expiry_date"][index]),
                                             cardholder=table_for["cardholder"][index])

        newPaymentMethod.classification = CardClassification.query.filter_by(
            card_identifier=table_for["card_identifier"][index]).first()

        newListing.billing = [newBilling]
        db.session.add(newPaymentMethod)
        db.session.add(newBilling)


def initListings():
    items_file = os.path.join(jsonPath, 'all_items.json')
    item_data = json.load(open(items_file, encoding='utf-8'))

    for category in item_data:
        for item in item_data[category]:
            newListing = ItemListing(id_identifier=str(item["listing_id"])[0],
                                     thumbnail_img=item["thumbnail_img"],
                                     listing_name=item["listing_name"],
                                     listing_description=item["listing_description"],
                                     avg_price=item["avg_price"],
                                     avg_rating=item["avg_rating"],
                                     num_of_reviews=item["num_of_reviews"],
                                     footprint=item["footprint"],
                                     sold=item["sold"],
                                     in_stock=item["in_stock"],
                                     date_added=datetime.datetime.fromisoformat(item["date_added"]))

            initOptions(item, item["options"], newListing)
            initReviewsAndReplies(item, item["reviews"], newListing)
            initBillingAndPayment(item, item["billing"], newListing)

            db.session.add(newListing)


def initAppDB():
    with app.app_context():
        initLookupTables()
        initListings()
        initInvoices()
        db.session.commit()
        db.session.close()


@app.before_request
def dbCheck():
    if getDBLocation().is_file():
        createAppDB()
    else:
        createAppDB()
        initAppDB()
