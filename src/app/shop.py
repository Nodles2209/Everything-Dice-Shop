from create_app import app
from flask import (Flask, render_template, redirect, url_for, request)
from instance.db.initDB import dbCheck
dbCheck()


@app.route('/faq')
def faq():
    # return render_template('faq.html', categories=all_categories
    pass


@app.route('/')
def homePage():
    return render_template('index.html', categories=all_categories, home_display=home_display.items())


def getDatabaseQuery():
    # process query words and return relevant database query
    pass


@app.route('/search', methods=['POST'])
def search(query):
    # return render_template('search.html', query=query)
    pass


@app.route('/<string:category>')
def loadCategory(category):
    return render_template('loadCategory.html', category_items=item_json[category], categories=all_categories,
                           category_name=category)


@app.route('/<int:item_id>')
def loadItem(item_id):
    for item_category, item_list in item_json.items():
        for item in item_list:
            if item['id'] == item_id:
                return render_template('singleItem.html', item=item, categories=all_categories)


@app.route('/reviewThread')
def loadReviewThread():
    # load expanded review thread upon clicking on review link
    # return render_template('reviewThread.html')
    pass


@app.route('/signIn')
def signIn():
    # return render_template('signIn.html')
    pass


@app.route('/forgotPassword')
def forgotPassword():
    # render_template('forgotPassword.html')
    # ask which email the password is for and then send email to user with reset link if email exists
    pass


@app.route('/signUp')
def signUp():
    # return render_template('signUp.html')
    pass


@app.route('/checkout')
def checkOut():
    # return render_template('checkout.html')
    pass


@app.route('/shoppingBasket')
def shoppingBasket():
    # return render_template('shoppingBasket.html')
    pass


@app.route('/addToBasket')
def addToBasket():
    # displays page where you either
    # go to checkout
    # go to basket
    # go to item page
    # go to home page to search more items
    pass


if __name__ == '__main__':
    app.run(debug=True)
