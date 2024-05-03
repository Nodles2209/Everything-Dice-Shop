from flask_wtf import FlaskForm
import wtforms


class OptionsForm(FlaskForm):
    option = wtforms.SelectField('Select option')
    quantity = wtforms.IntegerField('Quantity', default=1, widget=wtforms.widgets.NumberInput(min=1))
    submit = wtforms.SubmitField('Add to basket')


class ToCheckoutForm(FlaskForm):
    changeQuantity = wtforms.IntegerField('Change quantity', widget=wtforms.widgets.NumberInput(min=1))
    delete = wtforms.SubmitField('Delete')
    checkout = wtforms.SubmitField('Checkout')


class CheckoutForm(FlaskForm):
    address1 = wtforms.StringField('Address 1')
    address2 = wtforms.StringField('Address 2')
    address3 = wtforms.StringField('Address 3')
    city = wtforms.StringField('City')
    postcode = wtforms.StringField('Postcode')
    country = wtforms.SelectField('Country')  # add choices from database query
    state = wtforms.StringField('State')
    phone_area_code = wtforms.IntegerField('Phone area code')
    phone_number = wtforms.IntegerField('Phone number')
    payment_type = wtforms.RadioField('Payment type', choices=[('card', 'Card'), ('online', 'Paypal')])
    payment_method = wtforms.SelectField('Payment method')  # add choices from database query or a choice which adds
    # new payment methods via js
    submit = wtforms.SubmitField('Complete payment')


class SortForm(FlaskForm):
    sort_by = wtforms.SelectField('Sort by', choices=[('price', 'Price'),
                                                      ('name', 'Name'),
                                                      ('reviews', 'Review rating'),
                                                      ('footprint', 'Environmental footprint'),
                                                      ('sold', 'Sold')],
                                  default='name')
    order_by = wtforms.RadioField('Order', choices=[('asc', 'Ascending'), ('desc', 'Descending')], default='asc')
    category = wtforms.RadioField('Category', choices=[('all', 'All categories'),
                                                       ('resin_dice', 'Resin dice'),
                                                       ('metal_dice', 'Metal dice'),
                                                       ('dice_making_materials', 'Dice making materials'),
                                                       ('dice_accessories', 'Dice accessories')],
                                  default='all')
    show_sold = wtforms.BooleanField('Show sold out items')
    submit = wtforms.SubmitField('Sort')
