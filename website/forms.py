from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, \
    SelectMultipleField, widgets, FileField, HiddenField, DecimalField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Choose Role', choices=[(0, 'Student'), (1, 'Teacher'), (2, 'Admin')],
                       validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # TODO: Use user courses as the choice list
    course = SelectField('Course',
                         choices=[('CPSC571', 'CPSC 571'), ('CPSC313', 'CPSC 313'),
                                  ('CPSC441', 'CPSC 441'), ('CPSC449', 'CPSC 449'),
                                  ('CPSC530', 'CPSC 530'), ('CPSC231', 'CPSC 231')],
                         validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    gradingScale = TextAreaField('Grading Scale')
    assignmentFile = FileField('assignmentFile')
    submit = SubmitField('Post')

class RateForm(FlaskForm):

    CourseCode = StringField("CourseCode"),
    Prof = StringField("Prof"),
    Term = StringField("Term"),
    Section = StringField("Section"),
    content = TextAreaField('Content')
    rating = SelectField('Rating',
                         choices=[('1', '1'), ('1.5', '1.5'),
                                  ('2', '2'), ('2.5', '2.5'),
                                  ('3', '3'), ('3.5', '3.5'),
                                  ('4', '4'), ('4.5', '4.5'),
                                  ('5', '5')],
                         validators=[DataRequired()])
    submit = SubmitField('Rate')


class SubmitAssignmentForm(FlaskForm):
    submissionFile = FileField('submissionFile')
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')


class GradeSubmissionForm(FlaskForm):
    comments = TextAreaField('Grading Comments', validators=[DataRequired()])
    grade = DecimalField('Grade (out of 100%)', default=0.0, places=2, validators=[DataRequired()])
    submit = SubmitField('Submit Grade')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    courseChoices = MultiCheckboxField('Courses', coerce=str)
    otherCourseChoices = MultiCheckboxField('OtherCourses', coerce=str)
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
