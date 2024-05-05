from wtforms import FormField
from flask_wtf import FlaskForm
import wtforms
from wtforms.form import Form


class OptionsForm(FlaskForm):
    option = wtforms.SelectField('Select option', validators=[wtforms.validators.DataRequired()])
    quantity = wtforms.IntegerField('Quantity', default=1, widget=wtforms.widgets.NumberInput(min=1),
                                    validators=[wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField('Add to basket')


class ShoppingBasketForm(FlaskForm):
    clear = wtforms.SubmitField('Clear basket')
    checkout = wtforms.SubmitField('Checkout')


class CardForm(Form):
    card_holder = wtforms.StringField('Cardholder name',
                                      validators=[wtforms.validators.DataRequired(),
                                                  wtforms.validators.InputRequired()])
    card_num = wtforms.StringField('Card number',
                                   validators=[wtforms.validators.DataRequired(), wtforms.validators.InputRequired()])
    expiry_date = wtforms.DateField('Expiry Date', format='%Y-%m-%d')
    cvc = wtforms.StringField('CVC', validators=[wtforms.validators.DataRequired()])


class OnlineForm(Form):
    name_or_email = wtforms.StringField('Username or Email', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])


class CheckoutForm(FlaskForm):
    address1 = wtforms.StringField('Address 1', validators=[wtforms.validators.DataRequired()])
    address2 = wtforms.StringField('Address 2')
    address3 = wtforms.StringField('Address 3')
    city = wtforms.StringField('City', validators=[wtforms.validators.DataRequired()])
    postcode = wtforms.StringField('Postcode')
    country = wtforms.SelectField('Country', coerce=int)  # add choices from
    # database query
    state = wtforms.StringField('State')
    phone_area_code = wtforms.SelectField('Phone area code', coerce=int)
    phone_number = wtforms.IntegerField('Phone number', validators=[wtforms.validators.DataRequired()])
    payment_type = wtforms.RadioField('Payment type', choices=[('card', 'Card'), ('online', 'Paypal')],
                                      default=('card', 'Card'), validators=[wtforms.validators.DataRequired()])
    payment_method = wtforms.SelectField('Payment method')  # add
    # choices from database query
    # (a concat string containing last 4 digits of the card num) or a choice which adds new payment methods via js
    card_form = FormField(CardForm)  # add card form in a div which stays hidden until payment method is "new" and
    # payment type is card
    online_form = FormField(OnlineForm)  # add online form in a div which stays hidden until payment method is "new"
    # and payment type is online
    submit = wtforms.SubmitField('Complete payment')


class SortForm(FlaskForm):
    sort_by = wtforms.SelectField('Sort by', choices=[('price', 'Price'),
                                                      ('name', 'Name'),
                                                      ('avg_rating', 'Average Ratings'),
                                                      ('footprint', 'Environmental Footprint'),
                                                      ('sold', 'Sold'),
                                                      ('date_added', 'Date Added')],
                                  default=('name', 'Name'))
    order_by = wtforms.RadioField('Order', choices=[('asc', 'Ascending'), ('desc', 'Descending')], default='asc')
    category = wtforms.RadioField('Category', choices=[('all', 'All categories'),
                                                       ('resin_dice', 'Resin dice'),
                                                       ('metal_dice', 'Metal dice'),
                                                       ('dice_making_materials', 'Dice making materials'),
                                                       ('dice_accessories', 'Dice accessories')],
                                  default=('all', 'All categories'))
    show_sold = wtforms.BooleanField('Show sold out items')
    submit = wtforms.SubmitField('Sort')
