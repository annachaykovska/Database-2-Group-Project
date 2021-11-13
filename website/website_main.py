from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Can change this to be another db
db = SQLAlchemy(app)


# This is the structure of the database table to use
class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseNumber = db.Column(db.String(120), nullable=False)
    courseCode = db.Column(db.String(4), nullable=False)
    prerequisites = db.Column(db.String(200), nullable=True)
    antirequisites = db.Column(db.String(200), nullable=True)


# TODO: This will just make a new database if there isn't one here already, probably will need
#  to remove this
db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
