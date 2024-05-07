from wtforms import FormField
from flask_wtf import FlaskForm
import wtforms
from wtforms.form import Form


class OptionsForm(FlaskForm):
    option = wtforms.SelectField('Select option', validators=[wtforms.validators.DataRequired()], coerce=int)
    quantity = wtforms.IntegerField('Quantity', default=1, widget=wtforms.widgets.NumberInput(min=1),
                                    validators=[wtforms.validators.InputRequired()])
    price = wtforms.StringField('Price', render_kw={'readonly': True})
    submit = wtforms.SubmitField('Add to basket')


class BasketItemForm(FlaskForm):
    option = wtforms.StringField('Option selected', render_kw={'readonly': True})
    quantity = wtforms.IntegerField('Quantity', default=1, widget=wtforms.widgets.NumberInput(min=1),
                                    validators=[wtforms.validators.InputRequired()])
    price = wtforms.StringField('Price', render_kw={'readonly': True})
    delete_item = wtforms.SubmitField('Delete item')


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
    payment_type = wtforms.SelectField('Payment type',
                                       choices=[('none', 'Please select a payment option'),
                                                ('card', 'Card'),
                                                ('online', 'Paypal')],
                                       default=('none', 'Please select a payment option'),
                                       validators=[wtforms.validators.InputRequired()])
    payment_method = wtforms.SelectField('Payment method')  # add
    # choices from database query
    # (a concat string containing last 4 digits of the card num) or a choice which adds new payment methods via js
    card_form = FormField(CardForm)  # add card form in a div which stays hidden until payment method is "new" and
    # payment type is card
    online_form = FormField(OnlineForm)  # add online form in a div which stays hidden until payment method is "new"
    # and payment type is online
    submit = wtforms.SubmitField('Complete payment')


class SortForm(FlaskForm):
    sort_by = wtforms.SelectField('Sort by', choices=[('avg_price', 'Price'),
                                                      ('listing_name', 'Name'),
                                                      ('footprint', 'Environmental Footprint'),
                                                      ('sold', 'Sold'),
                                                      ('date_added', 'Date Added')],
                                  default=('name', 'Name'))
    order_by = wtforms.SelectField('Order', choices=[('asc', 'Ascending'), ('desc', 'Descending')],
                                   default=('asc', 'Ascending'))
    category = wtforms.SelectField('Category', choices=[('all', 'All categories'),
                                                        ('Resin dice', 'Resin dice'),
                                                        ('Metal dice', 'Metal dice'),
                                                        ('Dice making materials', 'Dice making materials'),
                                                        ('Dice accessories', 'Dice accessories')],
                                   default=('all', 'All categories'))
    show_sold = wtforms.SelectField('Show sold out items', choices=[(0, 'Yes'), (1, 'No')],
                                    default=(1, 'No'))
    submit = wtforms.SubmitField('Sort')


class CategorySortForm(FlaskForm):
    sort_by = wtforms.SelectField('Sort by', choices=[('avg_price', 'Price'),
                                                      ('listing_name', 'Name'),
                                                      ('footprint', 'Environmental Footprint'),
                                                      ('sold', 'Sold'),
                                                      ('date_added', 'Date Added')],
                                  default=('name', 'Name'))
    order_by = wtforms.SelectField('Order', choices=[('asc', 'Ascending'), ('desc', 'Descending')],
                                   default=('asc', 'Ascending'))
    show_sold = wtforms.SelectField('Show sold out items', choices=[(0, 'Yes'), (1, 'No')],
                                    default=(1, 'No'))
    submit = wtforms.SubmitField('Sort')
