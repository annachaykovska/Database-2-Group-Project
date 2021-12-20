from flask_login import UserMixin
from datetime import datetime, timezone

from website import db, login_manager
from website.defaultDatabaseEntries import courseList, antireqList, prereqList, otherCoursesList


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
    pastCpscCourses = db.Column(db.String(1000), nullable=True)
    pastOtherCourses = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    course = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_flag = db.Column(db.Boolean, default=False)
    file_name = db.Column(db.String(100), nullable=True)
    file_data = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# This is the structure of the database table to use
class Courses(db.Model):
    __tablename__ = "CPSCcourses"
    Department = db.Column(db.String(4), nullable=False)
    Course = db.Column(db.Integer, nullable=False)
    CourseCode = db.Column(db.String(7), primary_key=True)
    AntireqID = db.Column(db.Integer, nullable=False)
    PrereqID = db.Column(db.Integer, nullable=False)
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
    AntiReqID = db.Column(db.Integer, primary_key=True)
    AntiReq1 = db.Column(db.String(50), nullable=True)
    AntiReq2 = db.Column(db.String(50), nullable=True)
    AntiReq3 = db.Column(db.String(50), nullable=True)
    AntiReq4 = db.Column(db.String(50), nullable=True)
    AntiReq5 = db.Column(db.String(50), nullable=True)
    AntiReq6 = db.Column(db.String(50), nullable=True)
    AntiReq7 = db.Column(db.String(50), nullable=True)
    AntiReq8 = db.Column(db.String(50), nullable=True)
    AntiReq9 = db.Column(db.String(50), nullable=True)


class courses_taken(db.Model):
    __tablename__ = "courses_taken"
    #__table_args__ = (
    #    PrimaryKeyConstraint('CompoundPrimaryKey', 'identifier,Term,Course'),
    #)
    identifier = db.Column(db.Integer, primary_key=True)
    Term = db.Column(db.Integer, primary_key=True)
    Course = db.Column(db.String(15), primary_key=True)


class cpsc_random_sample(db.Model):
    __tablename__ = "cpsc_random_sample"
    Admit_Term = db.Column(db.Integer, nullable=False)
    Degree = db.Column(db.String(10), nullable=True)
    Primary_Plan_Description = db.Column(db.String(30), nullable=True)
    Concentration_Desc = db.Column(db.String(40), nullable=True)
    Identifier = db.Column(db.Integer, primary_key=True)


class OtherCourses(db.Model):
    __tablename__ = "OtherCourses"
    Department = db.Column(db.String(4), nullable=False)
    Course = db.Column(db.Integer, nullable=False)
    CourseCode = db.Column(db.String(7), primary_key=True)
    Name = db.Column(db.String(150), nullable=False)


# TODO: Comment this out if you don't need to make a new database
# db.create_all()
# for c in courseList:
#     db.session.add(Courses(**c))
# for a in antireqList:
#     db.session.add(AntiReq(**a))
# for p in prereqList:
#     db.session.add(PreReq(**p))
# for o in otherCoursesList:
#     db.session.add(OtherCourses(**o))
# db.session.commit()
