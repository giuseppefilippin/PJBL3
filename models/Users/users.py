from models.db import db
from models.Users.roles import Role
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))

    def save_user(role, username, password):
        role = Role.get_single_role(role)
        user = User(role_id = role.id, username = username, password = password)

        db.session.add(user)
        db.session.commit()

    def get_users():
        users = User.query.join(Role, Role.id == User.role_id)\
            .add_columns(User.id, User.username, Role.name).all()
        print(users)
        return users
    
    def update_user(id, username, role):
        user = User.query.filter(User.id == id).first()
        role = Role.query.filter(Role.user_id == id).first()
        if user is not None:
            user.username = username
            user.role = role

        db.session.commit()

        return User.get_users()
    
    def delete_user(id):
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()

        return User.get_users()
    
    def validate_user(username, password):
        user = User.query.filter(User.username == username).first()
        if user is not None and user.password == password:
            return user
        else:
            return None
