from flask import Flask
from models import *

def create_db(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        Role.save_role('admin', 'Administrator')
        Role.save_role('estático', 'Somente ver tempo real e histórico')
        Role.save_role('operador', 'alem do estático, consegue mandar comando')
        User.save_user('admin', 'admin', 'admin')