from instance.db.models import *
from instance.db.db import db
from src.app.create_app import InitApp, cur_path, parent
import os
from flask import json
import datetime
from pathlib import Path

app = InitApp()


def createAppDB():
    with app.app_context():
        db.create_all()


def initLookupTables():
    lookup_file = os.path.join(cur_path, 'static', 'json', 'reference_tables.json')
    lookup_data = json.load(open(lookup_file, encoding='utf-8'))

    for classification in lookup_data["Item classifications"]:
        newCategory = ItemClassification(id_identifier=classification["id_identifier"],
                                         category_name=classification["category_name"])
        db.session.add(newCategory)

    for country in lookup_data["Country list"]:
        newCountry = CountryList(country_name=country["country_name"])
        db.session.add(newCountry)

    for vendor in lookup_data["Card classification"]:
        newVendor = CardClassification(card_identifier=vendor["card_identifier"],
                                       card_type=vendor["card_type"])
        db.session.add(newVendor)


def initListings():
    items_file = os.path.join(cur_path, 'static', 'json', 'all_items.json')
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
                                     in_stock=item["in_stock"])

            creating_table_for = item["options"]
            for index in range(len(creating_table_for["option_id"])):
                newOption = ListingOptions(for_listing_id=item["listing_id"],
                                           option_img=creating_table_for["option_img"][index],
                                           option_name=creating_table_for["option_name"][index],
                                           option_price=creating_table_for["option_price"][index],
                                           option_stock=creating_table_for["option_stock"][index],
                                           option_sold=creating_table_for["option_sold"][index],
                                           option_inStock=creating_table_for["option_inStock"][index])
                newListing.options.append(newOption)

            creating_table_for = item["reviews"]
            for index in range(len(creating_table_for["review_id"])):
                newReview = ListingReviews(review_id=creating_table_for["review_id"][index],
                                           listing_id=item["listing_id"],
                                           review_user_id=creating_table_for["review_user_id"][index],
                                           review_title=creating_table_for["review_title"][index],
                                           review_text=creating_table_for["review_text"][index],
                                           review_rating=creating_table_for["review_rating"][index],
                                           num_of_replies=creating_table_for["num_of_replies"][index])

            creating_table_for = item["replies"]
            for index in range(len(creating_table_for["reply_id"])):
                newReply = ReviewReplies(reply_id=creating_table_for["reply_id"][index],
                                         reply_user_id=creating_table_for["reply_user_id"][index],
                                         under_review_id=creating_table_for["review_id"][index],
                                         reply_text=creating_table_for["reply_text"][index])
                newReview.replies.append(newReply)
                newListing.reviews.append(newReview)
                db.session.add(newReply)
                db.session.add(newReview)

            creating_table_for = item["billing"]
            for index in range(len(creating_table_for["billing_id"])):
                newBilling = ListingBillingInfo(address_1=creating_table_for["address_1"][index],
                                                address_2=creating_table_for["address_2"][index],
                                                address_3=creating_table_for["address_3"][index],
                                                city=creating_table_for["city"][index],
                                                postcode=creating_table_for["postcode"][index],
                                                country_id=creating_table_for["country_id"][index],
                                                state=creating_table_for["state"][index],
                                                phone_area_code=creating_table_for["phone_area_code"][
                                                    index],
                                                phone_num=creating_table_for["phone_num"][index],
                                                payment_method=creating_table_for["payment_method"][index],
                                                billing_type="listing",
                                                listing_id=item["listing_id"])

            creating_table_for = item["payment_method"]
            for index in range(len(creating_table_for["payment_method"])):
                newPaymentMethod = CreditCardDetails(payment_type=creating_table_for["transaction_type"][
                    index],
                                                     identifier=creating_table_for["card_identifier"][
                                                         index],
                                                     card_num=creating_table_for["card_num"][index],
                                                     expiry_date=datetime.datetime.fromisoformat(
                                                         creating_table_for["expiry_date"][index]),
                                                     cardholder=creating_table_for["cardholder"][index])

                newPaymentMethod.classification = CardClassification.query.filter_by(
                    card_identifier=creating_table_for["card_identifier"][index]).first()

                newListing.billing = [newBilling]
                db.session.add(newPaymentMethod)
                db.session.add(newBilling)

            db.session.add(newListing)


def initAppDB():
    with app.app_context():
        initLookupTables()
        initListings()
        db.session.commit()
        db.session.close()


@app.before_request
def dbCheck():
    myDB = Path(os.path.join(parent, 'instance', 'app.db'))
    if myDB.is_file():
        createAppDB()
    else:
        createAppDB()
        initAppDB()


dbCheck()
