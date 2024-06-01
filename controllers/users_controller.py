from flask import Blueprint, render_template, request
from models.Users.users import User

user = Blueprint('user', __name__, template_folder='views')
        
@user.route('/users')
def users():
    users = User.get_users()
    return render_template('user.html', users=users)
        
@user.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        role = request.form['role']
        User.save_user(role, user, password)
        users = User.get_users()

        return render_template('user.html', users=users)

@user.route('/del_user', methods=['GET'])
def del_user():
    id = request.args.get('id', None)
    users = User.delete_user(id)

    return render_template('user.html', users=users)