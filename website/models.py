from website import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # 0 = Student, 1 = Teacher, 2 = Admin
    role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    course = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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
    AntiReq9 = db.Column(db.String(50), nullable=True)

## TODO: This will just make a new database if there isn't one here already, probably will need
##  to remove this
db.create_all()

