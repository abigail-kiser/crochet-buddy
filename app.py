import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from enum import Enum


scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "database.sqlite3")

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class yarnWeightEnum(Enum):
    Lace = 0
    SuperFine = 1
    Fine = 2
    Light = 3
    Medium = 4
    Bulky = 5
    SuperBulky = 6
    Jumbo = 7


# -------------------------------------- Database Initialization ----------------------------------


"""
Database Models for Yarn
    id: Int, Primary Key, AutoIncremented
    lengthYards: Int, Length of yarn in yards (optional)
    numSkeins: Int, Number of skeins (optional)
    weight: Enum, Weight category of yarn (required)
    color: String(50), Color of the yarn (required)
    brand: String(50), Brand of the yarn (optional)
    specialAttr: String(100), Special attributes (ex. sparkly, scrubby) (optional)
    material: String(100), Material(s) composition (ex. 100% wool, 80% cotton 20% polyester) (optional)
    thumbnail: String(200), Path to thumbnail image (optional)


    Note: can't have both lengthYards and numSkeins
        if don't have lengthYards, won't be affected by use with pattern + won't count towards stats

    note: todo: thumbnail will be implemented later. it'll still be optional once implemented
    
    """
class Yarn(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    lengthYards = db.Column(db.Integer) 
    numSkeins = db.Column(db.Integer)
    weight = db.Column(db.Enum(yarnWeightEnum), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50))
    specialAttr = db.Column(db.String(100))
    material = db.Column(db.String(100))
    thumbnail = db.Column(db.String(200))  # Path to thumbnail image

    def __str__(self):
        return f"Yarn(ID: {self.id}, Color: {self.color}, Weight: {self.weight.name})"

    def __repr__(self):
        return f"Yarn({self.id})"

# """Database Models for PatrnIngredients"""
# class PatrnIngredients(db.Model):

#     __abstract__ = True

#     id = db.Column(db.Integer, primary_key=True)
#     # pattern_id = db.Column(db.Integer, db.ForeignKey('pattern.id'), nullable=False)
#     yarn_id = db.Column(db.Integer, db.ForeignKey('yarn.id'), nullable=False)


# """
# Database Models for Pattern

# """
# class Pattern(db.Model, PatrnIngredients):

#     id = db.Column(db.Integer, primary_key=True)
    

with app.app_context():
    # db.drop_all()
    db.create_all()

    #example yarns
    multipleYarns = [
        Yarn(lengthYards=200, weight=yarnWeightEnum.Medium, color="Red", brand="YarnCo", material="100% Wool"), 
        Yarn(numSkeins=3, weight=yarnWeightEnum.Bulky, color="Blue", brand="KnitStuff", specialAttr="Sparkly", material="80% Acrylic 20% Nylon")
    ]
    
    # Add example yarns to the database if they don't already exist
    # (ignoring length being added when duplicates for now. that'll be a different function,
    # prompted by when the user enters a new yarn)
    for yarn in multipleYarns:
        possYarn = Yarn.query.filter_by(color=yarn.color, weight=yarn.weight).first()
        if possYarn is not None:
            db.session.merge(possYarn)
        else:
            print(f"Adding yarn: {yarn.color}, Weight: {yarn.weight.name}")
            db.session.add(yarn)


    db.session.commit()



# --------------------------------------- Route Definitions ----------------------------------

@app.route('/')
def library():
    yarnsInDB = Yarn.query.all()
    # for yarn in yarnsInDB:
    #     print(f"Yarn ID: {yarn.id}, Color: {yarn.color}, Weight: {yarn.weight.name}")
    return render_template("library.html", yarns=yarnsInDB)


@app.route('/discover/')
def discover():
    return render_template("discover.html")


@app.route('/settings/')
def settings():
    return render_template("settings.html")






# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()