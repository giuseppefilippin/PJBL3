from models.db import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def save_role(name, description):
        role = Role(name = name, description = description)
        db.session.add(role)
        db.session.commit()
        
    def get_single_role(name):
        role = Role.query.filter(Role.name == name).first()
        return role
    
    def get_roles():
        roles = Role.query.all()
        return roles