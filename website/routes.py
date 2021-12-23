from datetime import datetime
from io import BytesIO
import re
from flask import render_template, flash, redirect, url_for, request, abort, send_file, jsonify
from website import app, db, bcrypt
from website.models import Courses, PreReq, AntiReq, User, Post, OtherCourses
from website.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from website.defaultDatabaseEntries import courseList, antireqList, prereqList, otherCoursesList
import json
import website.Jaccard
from website.Predictor import Predictor

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # https://github.com/PrettyPrinted/youtube_video_code/blob/master/2019/06/21/Get%20Form%20Checkbox%20Data%20in%20Flask%20With%20.getlist/checkbox_data/templates/index.html
    form = UpdateAccountForm()
    choices = []
    otherChoices = []
    allCpscCourses = db.session.query(Courses).all()
    for c in allCpscCourses:
        choices.append((c.CourseCode, c.CourseCode))
    allOtherCourses = db.session.query(OtherCourses).all()
    for c in allOtherCourses:
        otherChoices.append((c.CourseCode, c.CourseCode))

    form.courseChoices.choices = choices
    form.otherCourseChoices.choices = otherChoices
    pastCpscCourses = "No Saved Courses"
    pastOtherCourses = "No Saved Courses"
    if current_user.pastCpscCourses:
        pastCpscCourses = current_user.pastCpscCourses.split(", ")
    if current_user.pastOtherCourses:
        pastOtherCourses = current_user.pastOtherCourses.split(", ")

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        pastCpscCourses = ""
        for c in form.courseChoices.data:
            if not pastCpscCourses:
                pastCpscCourses = c
            else:
                pastCpscCourses += f", {c}"
        current_user.pastCpscCourses = pastCpscCourses

        pastOtherCourses = ""
        for c in form.otherCourseChoices.data:
            if not pastOtherCourses:
                pastOtherCourses = c
            else:
                pastOtherCourses += f", {c}"
        current_user.pastOtherCourses = pastOtherCourses

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',
                           title='Account',
                           form=form,
                           pastCpscCourses=pastCpscCourses,
                           pastOtherCourses=pastOtherCourses)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/courses")
def courses():
    return render_template('courses.html')


@app.route("/IO",)
def IO():
    previousClasses = current_user.pastCpscCourses.split(", ")
    cl = Predictor.predict(previousClasses)
    if len(cl) == 0:
        cl = ["With the given selection of courses no recommendations were possible. Please try again or change your previous courses under the account settings"]
    return render_template('IO.html',addedClasses=cl)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        file_data = request.files.get(form.assignmentFile.name)
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    course=form.course.data,
                    assignment_flag=False)
        if file_data:
            post.file_name = form.assignmentFile.name
            post.file_data = file_data.read()
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post', assignment=False)


@app.route("/assignment/new", methods=['GET', 'POST'])
@login_required
def new_assignment():
    form = PostForm()
    if form.validate_on_submit():
        file_data = request.files.get(form.assignmentFile.name)
        dueString = request.form.get('duetime')
        if dueString:
            # Todo: Validate that the input is later than right now if you feel like it
            due_date = datetime.strptime(dueString, '%Y-%m-%dT%H:%M')
        else:
            due_date = None
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    course=form.course.data,
                    grading_scale=form.gradingScale.data,
                    due_date=due_date,
                    assignment_flag=True)
        if file_data:
            post.file_name = file_data.filename
            post.file_data = file_data.read()

        db.session.add(post)
        db.session.commit()
        flash('Your new assignment has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Assignment',
                           form=form, legend='New Assignment', assignment=True)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, course=post.course, post=post)


@app.route("/post/<int:post_id>/view", methods=['GET', 'POST'])
def post_file(post_id):
    post = Post.query.get_or_404(post_id)
    return send_file(BytesIO(post.file_data), attachment_filename=post.file_name, as_attachment=True)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    assignmentFlag = post.assignment_flag
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.course = form.course.data
        file_data = request.files.get(form.assignmentFile.name)
        dueString = request.form.get('duetime')
        if dueString:
            # Todo: Validate that the input is later than right now if you feel like it
            post.due_date = datetime.strptime(dueString, '%Y-%m-%dT%H:%M')
        else:
            post.due_date = None
        if file_data:
            post.file_name = form.assignmentFile.name
            post.file_data = file_data.read()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.course.data = post.course
        if assignmentFlag:
            form.gradingScale.data = post.grading_scale

    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post', assignment=assignmentFlag)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


# @app.route("/teacher-assignments")
# @login_required
# def view_assignments():
#     return render_template('assignments.html', title='Assignments')
