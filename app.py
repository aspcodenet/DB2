from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
import barnum



app = Flask("__name__")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hejsan123@localhost/demo'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
with app.app_context():
    upgrade()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    cards = db.relationship('Card', backref='person', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80), unique=False, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)
    # glömde
    typ = db.Column(db.String(80), unique=False, nullable=False)

if __name__  == "__main__":
    while True:
        print("1. Skapa")
        sel = input("Val:")
        if sel == "1":
            person = Person()
            n = barnum.create_name()
            person.namn = n[0] + " " + n[1]
            person.city = barnum.create_city_state_zip()[1]
            n = barnum.create_cc_number()
            c = Card()
            c.number = n[1][0]
            c.typ = n[0]
            person.cards.append(c)
            n = barnum.create_cc_number()
            c = Card()
            c.number = n[1][0]
            c.typ = n[0]
            person.cards.append(c)
            db.session.add(person)
            db.session.commit()



