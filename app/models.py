
from flask_login import UserMixin 
from settings import db,app


class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.id)
    
    def show(self):
        return {'id': self.id, 'username': self.username}
    
class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age=db.Column(db.Integer, nullable=False)
    standard= db.Column(db.String(40), nullable=False)
    rollnumber= db.Column(db.Integer, nullable=False)
    

    def show(self):
        return {'id': self.id, 'name': self.name, 'age': self.age, 'standard': self.standard,'rollnumber': self.rollnumber}

with app.app_context():
    db.create_all()