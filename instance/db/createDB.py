from flask_sqlalchemy import SQLAlchemy
from src.app.create_app import app

db = SQLAlchemy(app)


class ItemClassification(db.Model):
    __tablename__ = "item_classification"

    classification_id = db.Column(db.Integer, primary_key=True)

    id_identifier = db.Column(db.Integer, db.ForeignKey("item_listing.id_identifier"))
    identifier = db.relationship("ItemListing", back_populates="classification",
                                 primaryjoin="ItemClassification.id_identifier == ItemListing.id_identifier")

    category_name = db.Column(db.String, index=True)


class ItemListing(db.Model):
    __tablename__ = "item_listing"

    listing_id = db.Column(db.Integer, primary_key=True)
    options = db.relationship("ListingOptions", back_populates="listing",
                              primaryjoin="ItemListing.listing_id == ListingOptions.for_listing_id")
    reviews = db.relationship("ListingReviews", back_populates="listing",
                              primaryjoin="ItemListing.listing_id == ListingReviews.listing_id")
    billing = db.relationship("ListingBillingInfo", back_populates="listing",
                              primaryjoin="ItemListing.listing_id == ListingBillingInfo.listing_id")

    id_identifier = db.Column(db.Integer, index=True)
    classification = db.relationship("ItemClassification", back_populates="identifier",
                                     primaryjoin="ItemListing.id_identifier == ItemClassification.id_identifier")

    thumbnail_img = db.Column(db.String, index=True)
    listing_name = db.Column(db.String, index=True)
    listing_description = db.Column(db.Text, index=True)
    footprint = db.Column(db.Float, index=True)
    avg_price = db.Column(db.Float, index=True)
    avg_rating = db.Column(db.Float, index=True)
    num_of_reviews = db.Column(db.Integer, index=True)
    sold = db.Column(db.Integer, index=True)


class ListingOptions(db.Model):
    __tablename__ = "listing_options"

    option_id = db.Column(db.Integer, primary_key=True)
    basket = db.relationship("BasketItem", back_populates="option",
                             primaryjoin="ListingOptions.option_id == BasketItem.for_item_id")

    for_listing_id = db.Column(db.Integer, db.ForeignKey("item_listing.listing_id"))
    listing = db.relationship("ItemListing", back_populates="options",
                              primaryjoin="ListingOptions.for_listing_id == ItemListing.listing_id")

    option_img = db.Column(db.String, index=True)
    option_name = db.Column(db.String, index=True)
    option_price = db.Column(db.Float, index=True)
    option_stock = db.Column(db.Integer, index=True)
    option_sold = db.Column(db.Integer, index=True)
    option_inStock = db.Column(db.Boolean, index=True)


class ListingReviews(db.Model):
    __tablename__ = "listing_reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    reply = db.relationship("ReviewReplies", back_populates="review",
                            primaryjoin="ListingReviews.review_id == ReviewReplies.under_review_id")

    listing_id = db.Column(db.Integer, db.ForeignKey("item_listing.listing_id"))
    listing = db.relationship("ItemListing", back_populates="reviews",
                              primaryjoin="ListingReviews.listing_id == ItemListing.listing_id")

    review_user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="review",
                           primaryjoin="ListingReviews.review_user_id == UserProfile.user_id")

    review_title = db.Column(db.String, index=True)
    review_text = db.Column(db.Text, index=True)
    review_rating = db.Column(db.Float, index=True)
    num_of_replies = db.Column(db.Integer, index=True)


class ReviewReplies(db.Model):
    __tablename__ = "review_replies"

    reply_id = db.Column(db.Integer, primary_key=True)

    reply_user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="reply",
                           primaryjoin="ReviewReplies.reply_user_id == UserProfile.user_id")

    under_review_id = db.Column(db.Integer, db.ForeignKey("listing_reviews.review_id"))
    review = db.relationship("ListingReviews", back_populates="reply",
                             primaryjoin="ReviewReplies.under_review_id == ListingReviews.review_id")

    reply_text = db.Column(db.Text, index=True)


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    user_id = db.Column(db.Integer, primary_key=True)
    review = db.relationship("ListingReviews", back_populates="user",
                             primaryjoin="UserProfile.user_id == ListingReviews.review_user_id")
    reply = db.relationship("ReviewReplies", back_populates="user",
                            primaryjoin="UserProfile.user_id == ReviewReplies.reply_user_id")
    basket = db.relationship("UserBasket", back_populates="user",
                             primaryjoin="UserProfile.user_id == UserBasket.basket_user_id")
    billing = db.relationship("UserBillingInfo", back_populates="user",
                              primaryjoin="UserProfile.user_id == UserBillingInfo.user_id")

    username = db.Column(db.String, index=True)
    password = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)


class UserBasket(db.Model):
    __tablename__ = "user_basket"

    basket_id = db.Column(db.Integer, primary_key=True)
    basket_item = db.relationship("BasketItem", back_populates="basket",
                                  primaryjoin="UserBasket.basket_id == BasketItem.for_basket_id")

    basket_user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="basket",
                           primaryjoin="UserBasket.basket_user_id == UserProfile.user_id")

    session_id = db.Column(db.String, index=True)


class BasketItem(db.Model):
    __tablename__ = "basket_item"

    basket_item_num = db.Column(db.Integer, primary_key=True)

    for_basket_id = db.Column(db.Integer, db.ForeignKey("user_basket.basket_id"))
    basket = db.relationship("UserBasket", back_populates="basket_item",
                             primaryjoin="BasketItem.for_basket_id == UserBasket.basket_id")

    for_item_id = db.Column(db.Integer, db.ForeignKey("listing_options.option_id"))
    option = db.relationship("ListingOptions", back_populates="basket",
                             primaryjoin="BasketItem.for_item_id == ListingOptions.option_id")

    num_of_items = db.Column(db.Integer, index=True)


class CountryList(db.Model):
    __tablename__ = "country_list"

    country_id = db.Column(db.Integer, primary_key=True)
    billing = db.relationship("BillingInfo", back_populates="country",
                              primaryjoin="CountryList.country_id == BillingInfo.country_id")

    country_name = db.Column(db.String, index=True)


class BillingInfo(db.Model):
    __tablename__ = "billing_info"

    billing_id = db.Column(db.Integer, primary_key=True)

    address_1 = db.Column(db.String, index=True)
    address_2 = db.Column(db.String, index=True)
    address_3 = db.Column(db.String, index=True)
    city = db.Column(db.String, index=True)
    postcode = db.Column(db.String, index=True)

    country_id = db.Column(db.Integer, db.ForeignKey("country_list.country_id"))
    country = db.relationship("CountryList", back_populates="billing",
                              primaryjoin="BillingInfo.country_id == CountryList.country_id")

    state = db.Column(db.String, index=True)
    phone_area_code = db.Column(db.Integer, index=True)
    phone_num = db.Column(db.Integer, index=True)

    payment_method = db.Column(db.Integer, db.ForeignKey("payment_method.details_id"))
    billing_type = db.Column(db.String, index=True)

    __mapper_args__ = {"polymorphic_identity": "billing_info",
                       "polymorphic_on": 'billing_type'}


class ListingBillingInfo(BillingInfo):
    __tablename__ = "listing_billing_info"
    __mapper_args__ = {"polymorphic_identity": "listing_billing_info"}

    details = db.relationship("PaymentMethod", back_populates="listing_billing",
                              primaryjoin="ListingBillingInfo.payment_method == PaymentMethod.details_id")

    listing_id = db.Column(db.Integer, db.ForeignKey("item_listing.listing_id"))
    listing = db.relationship("ItemListing", back_populates="billing",
                              primaryjoin="ListingBillingInfo.listing_id == ItemListing.listing_id")


class UserBillingInfo(BillingInfo):
    __tablename__ = "user_billing_info"
    __mapper_args__ = {"polymorphic_identity": "user_billing_info"}

    details = db.relationship("PaymentMethod", back_populates="user_billing",
                              primaryjoin="UserBillingInfo.payment_method == PaymentMethod.details_id")

    user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="billing",
                           primaryjoin="UserBillingInfo.user_id == UserProfile.user_id")


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"

    details_id = db.Column(db.Integer, primary_key=True)
    listing_billing = db.relationship("ListingBillingInfo", back_populates="details",
                                      primaryjoin="PaymentMethod.details_id == ListingBillingInfo.payment_method")
    user_billing = db.relationship("UserBillingInfo", back_populates="details",
                                   primaryjoin="PaymentMethod.details_id == UserBillingInfo.payment_method")

    payment_type = db.Column(db.String, index=True)
    __mapper_args__ = {"polymorphic_identity": "payment_method",
                       "polymorphic_on": 'payment_type'}


class CreditCardDetails(PaymentMethod):
    __tablename__ = "credit_card_details"
    __mapper_args__ = {"polymorphic_identity": "credit_card_details"}
    __schema__ = "credit_card_details"

    identifier = db.Column(db.Integer, db.ForeignKey("card_classification.card_identifier"))
    classification = db.relationship("CardClassification", back_populates="identifier",
                                     primaryjoin="CreditCardDetails.identifier == CardClassification.card_identifier")

    card_num = db.Column(db.Integer, index=True)
    expiry_date = db.Column(db.Date, index=True)

    cardholder = db.Column(db.String, index=True)


class CardClassification(db.Model):
    __tablename__ = "card_classification"

    classification_id = db.Column(db.Integer, primary_key=True)

    card_identifier = db.Column(db.Integer, index=True)
    identifier = db.relationship("CreditCardDetails", back_populates="classification",
                                 primaryjoin="CardClassification.card_identifier == CreditCardDetails.identifier")

    card_type = db.Column(db.String, index=True)


class OnlineBanking(PaymentMethod):
    __tablename__ = "online_banking"
    __mapper_args__ = {"polymorphic_identity": "online_banking"}
    __schema__ = "online_banking"

    merchant_name = db.Column(db.String, index=True)
    username = db.Column(db.String, index=True)
    password = db.Column(db.String, index=True)
