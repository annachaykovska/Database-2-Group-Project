from flask import render_template, flash, redirect, url_for
from website import app
from website.models import Courses, PreReq, AntiReq
from website.forms import RegistrationForm, LoginForm


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


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