from flask import Blueprint, render_template, request, flash
import flask_login
from flask_login import LoginManager, logout_user
from models.Users.users import User

login = Blueprint('login', __name__, template_folder='views')

@login.route('/validate_user', methods=['POST'])
def validate_user():
    username = request.form['username']
    password = request.form['password']
    user = User.validate_user(username, password)
    if (user == None):
        flash('Invalid username or password')
        return render_template('login.html')
    else:
        flask_login.login_user(user)
        return render_template('home.html')
    
@login.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')