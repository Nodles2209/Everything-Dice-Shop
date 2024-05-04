from flask_login import LoginManager
from create_app import InitApp
import instance.db.models as models
from flask import (Flask, render_template, redirect, url_for, request)

app = InitApp()
login_manager = LoginManager(app)
login_manager.session_protection = "strong"


@login_manager.user_loader
def loadUser(user_id):
    """
    Returns a user object from the database based on the user_id provided
    :param int user_id: id (primary key) field from user model
    :return: user model
    """""
    return models.UserProfile.get(user_id, None)


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
