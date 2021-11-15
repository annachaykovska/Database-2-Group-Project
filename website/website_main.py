from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CourseDB.db'  # Can change this to be another db
db = SQLAlchemy(app)

# This is the structure of the database table to use
class Courses(db.Model):
    __tablename__ = "CPSCcourses"
    Department = db.Column(db.String(4), nullable=False)
    Course = db.Column(db.Integer, nullable=False)
    CourseCode = db.Column(db.String(7), primary_key=True)
    AntireqID = db.Column(db.Integer, nullable=False)
    PreReqID = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(150), nullable=False)

class PreReq(db.Model):
    __tablename__ = "CoursePreReq"
    PreReqID = db.Column(db.Integer, primary_key=True)
    Prereq1 = db.Column(db.String(100), nullable=True)
    Prereq2 = db.Column(db.String(100), nullable=True)
    Prereq3 = db.Column(db.String(100), nullable=True)
    Prereq4 = db.Column(db.String(100), nullable=True)

class AntiReq(db.Model):
    __tablename__ = "CourseAntiReq"
    PreReqID = db.Column(db.Integer, primary_key=True)
    AntiReq1 = db.Column(db.String(50), nullable=True)
    AntiReq2 = db.Column(db.String(50), nullable=True)
    AntiReq3 = db.Column(db.String(50), nullable=True)
    AntiReq4 = db.Column(db.String(50), nullable=True)
    AntiReq5 = db.Column(db.String(50), nullable=True)
    AntiReq6 = db.Column(db.String(50), nullable=True)
    AntiReq7 = db.Column(db.String(50), nullable=True)
    AntiReq8 = db.Column(db.String(50), nullable=True)
    AntiReq8 = db.Column(db.String(50), nullable=True)
## TODO: This will just make a new database if there isn't one here already, probably will need
##  to remove this
db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/courses")
def courses():
    return render_template('courses.html')

@app.route("/students")
def students():
    return render_template('students.html')

@app.route("/instructors")
def instructors():
    return render_template('instructors.html')

if __name__ == '__main__':
    app.run(debug=True)
