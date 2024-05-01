from flask_sqlalchemy import SQLAlchemy
from src.app.shop import app

db = SQLAlchemy(app)


class ItemClassification(db.Model):
    __tablename__ = "item_classification"

    classification_id = db.Column(db.Integer, primary_key=True)

    id_identifier = db.Column(db.Integer, db.ForeignKey("item_listing.id_identifier"))
    identifier = db.relationship("ItemListing", back_populates="classification")

    category_name = db.Column(db.String, index=True)


class ItemListing(db.Model):
    __tablename__ = "item_listing"

    listing_id = db.Column(db.Integer, primary_key=True)
    options = db.relationship("ListingOptions", back_populates="listing")
    reviews = db.relationship("ListingReviews", back_populates="listing")
    billing = db.relationship("ListingBillingInfo", back_populates="listing")

    id_identifier = db.Column(db.Integer, index=True)
    classification = db.relationship("ItemClassification", back_populates="identifier")

    thumbnail_img = db.Column(db.String, index=True)
    listing_name = db.Column(db.String, index=True)
    listing_description = db.Column(db.Text, index=True)
    footprint = db.Column(db.Float, index=True)
    avg_price = db.Column(db.Float, index=True)
    avg_rating = db.Column(db.Float, index=True)
    num_of_reviews = db.Column(db.Integer, index=True)


class ListingOptions(db.Model):
    __tablename__ = "listing_options"

    option_id = db.Column(db.Integer, primary_key=True)
    basket = db.relationship("UserBasket", back_populates="option")

    for_listing_id = db.Column(db.Integer, db.ForeignKey("item_listing.listing_id"))
    listing = db.relationship("ItemListing", back_populates="options")

    option_img = db.Column(db.String, index=True)
    option_name = db.Column(db.String, index=True)
    option_price = db.Column(db.Float, index=True)
    option_stock = db.Column(db.Integer, index=True)
    option_sold = db.Column(db.Integer, index=True)
    option_inStock = db.Column(db.Boolean, index=True)


class ListingReviews(db.Model):
    __tablename__ = "listing_reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    reply = db.relationship("ReviewReplies", back_populates="review")

    listing_id = db.Column(db.Integer, db.ForeignKey("item_listing.listing_id"))
    listing = db.relationship("ItemListing", back_populates="reviews")

    review_user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="review")

    review_title = db.Column(db.String, index=True)
    review_text = db.Column(db.Text, index=True)
    review_rating = db.Column(db.Float, index=True)
    num_of_replies = db.Column(db.Integer, index=True)


class ReviewReplies(db.Model):
    __tablename__ = "review_replies"

    reply_id = db.Column(db.Integer, primary_key=True)

    reply_user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="reply")

    under_review_id = db.Column(db.Integer, db.ForeignKey("listing_reviews.review_id"))
    review = db.relationship("ListingReviews", back_populates="reply")

    reply_text = db.Column(db.Text, index=True)


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    user_id = db.Column(db.Integer, primary_key=True)
    review = db.relationship("ListingReviews", back_populates="user")
    reply = db.relationship("ReviewReplies", back_populates="user")
    basket = db.relationship("UserBasket", back_populates="user")
    billing = db.relationship("UserBillingInfo", back_populates="user")

    username = db.Column(db.String, index=True)
    password = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)


class UserBasket(db.Model):
    __tablename__ = "user_basket"

    basket_id = db.Column(db.Integer, primary_key=True)

    basket_user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="basket")

    item_id = db.Column(db.Integer, db.ForeignKey("listing_options.option_id"))
    option = db.relationship("ListingOptions", back_populates="basket")

    num_of_items = db.Column(db.Integer, index=True)


class CountryList(db.Model):
    __tablename__ = "country_list"

    country_id = db.Column(db.Integer, primary_key=True)
    billing = db.relationship("BillingInfo", back_populates="country")

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
    country = db.relationship("CountryList", back_populates="billing")

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
    listing = db.relationship("ItemListing", back_populates="billing")


class UserBillingInfo(BillingInfo):
    __tablename__ = "user_billing_info"
    __mapper_args__ = {"polymorphic_identity": "user_billing_info"}

    details = db.relationship("PaymentMethod", back_populates="user_billing",
                              primaryjoin="UserBillingInfo.payment_method == PaymentMethod.details_id")

    user_id = db.Column(db.Integer, db.ForeignKey("user_profile.user_id"))
    user = db.relationship("UserProfile", back_populates="billing")


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"

    details_id = db.Column(db.Integer, primary_key=True)
    listing_billing = db.relationship("ListingBillingInfo", back_populates="details")
    user_billing = db.relationship("UserBillingInfo", back_populates="details")

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
