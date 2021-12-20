from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, \
    SelectMultipleField, widgets, FileField
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
                         choices=[('CPSC 571', 'CPSC 571'), ('CPSC 313', 'CPSC 313'),
                                  ('CPSC 441', 'CPSC 441'), ('CPSC 449', 'CPSC 449'),
                                  ('CPSC 530', 'CPSC 530'), ('CPSC 231', 'CPSC 231')],
                         validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    assignmentFile = FileField('assignmentFile')
    submit = SubmitField('Post')


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
