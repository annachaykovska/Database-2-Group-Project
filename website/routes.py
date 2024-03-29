from datetime import datetime
from io import BytesIO
from website.defaultDatabaseEntries import courseList, antireqList, prereqList, otherCoursesList
from website.Predictor import Predictor
from flask import render_template, flash, redirect, url_for, request, abort, send_file
from website import app, db, bcrypt
from website.models import Courses, PreReq, AntiReq, User, Post, OtherCourses, offeredCourses, Submission, \
    professorRatings, enrolledCourses
from website.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, SubmitAssignmentForm, RateForm, \
    GradeSubmissionForm, AssignProfForm, courseEnrollForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = []
    if current_user.is_authenticated:
        posts = Post.query.filter(((Post.course == current_user.current_course_1) |
                                   (Post.course == current_user.current_course_2) |
                                   (Post.course == current_user.current_course_3) |
                                   (Post.course == current_user.current_course_4) |
                                   (Post.course == current_user.current_course_5) |
                                   (Post.course == current_user.current_course_6))
                                  & Post.assignment_flag == 0).all()
    # posts = Post.query.all()
    return render_template('home.html', posts=posts, addSubmissionButton=False)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # TODO: stop hard coding this
        course1 = 'CPSC571'
        course2 = 'CPSC441'
        course3 = 'CPSC530'
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    current_course_1=course1,
                    current_course_2=course2,
                    current_course_3=course3,
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


@app.route("/IO")
def IO():
    if current_user.is_authenticated:
        previousClasses = current_user.pastCpscCourses.split(", ")
        cl = Predictor.predict(previousClasses)
        if len(cl) == 0:
            cl = ["With the given selection of courses no recommendations were possible. Please try again or change your previous courses under the account settings"]
        return render_template('IO.html', addedClasses=cl)
    return render_template('IO.html')


@app.route("/AssignProf", methods=['GET', 'POST'])
def AssignProf():
    form = AssignProfForm()
    teachingProfs = offeredCourses.query.all()
    if form.validate_on_submit():
        teachingAssignment = offeredCourses(CourseCode  = form.CourseCode.data,
                                            Prof        = form.Prof.data,
                                            Term        = form.Term.data,
                                            Section     = form.Section.data
                                            )
        db.session.add(teachingAssignment)
        db.session.commit()
        if current_user.current_course_1 is None:
            current_user.current_course_1 = teachingAssignment.CourseCode
        elif current_user.current_course_2 is None:
            current_user.current_course_2 = teachingAssignment.CourseCode
        elif current_user.current_course_3 is None:
            current_user.current_course_3 = teachingAssignment.CourseCode
        elif current_user.current_course_4 is None:
            current_user.current_course_4 = teachingAssignment.CourseCode
        elif current_user.current_course_5 is None:
            current_user.current_course_5 = teachingAssignment.CourseCode
        elif current_user.current_course_6 is None:
            current_user.current_course_6 = teachingAssignment.CourseCode
        db.session.commit()
    return render_template('AssignProf.html', form=form)


@app.route("/CourseEnrollment", methods=['GET', 'POST'])
def CourseEnrollment():
    offerdCourses = offeredCourses.query.all()
    form = courseEnrollForm()
    if form.validate_on_submit():
        enrollCourse = enrolledCourses(
                                    id          = current_user.id,
                                    username    = current_user.username,
                                    CourseCode  = request.form["CourseCode"],
                                    Prof        = request.form["Prof"],
                                    Term        = request.form["Term"],
                                    Section     = request.form["Section"]
                                    )
        db.session.add(enrollCourse)
        db.session.commit()

    return render_template('CourseEnrollment.html', offerdCourses = offerdCourses, form = form)


@app.route("/RateProfessors", methods=['GET', 'POST'])
def RateProfessors():
    teachingProfs = offeredCourses.query.all()
    form = RateForm(request.form)
    if form.validate_on_submit():
        studentRate = professorRatings(CourseCode=request.form["CourseCode"],
                                       Prof=request.form["Prof"],
                                       Term=request.form["Term"],
                                       Section=request.form["Section"],
                                       Rating=form.rating.data,
                                       Comments=form.content.data,
                                       rater_id=current_user.id)
        db.session.add(studentRate)
        db.session.commit()
        flash(f'Your rating for {studentRate.Prof} for {studentRate.CourseCode} {studentRate.Section} has been successful!', 'success')
    return render_template('RateProfessors.html', teachingProfs=teachingProfs, form=form)


class ProfRatings:
    prof = ''
    courses = []
    # terms = []
    # section = []
    averageRating = None

    def __init__(self, prof, courses):
        self.prof = prof
        self.courses = courses
        self.ratings = [[], []]
        return

    def calcAverageRating(self):
        ratingList = []
        num = 0
        for r in self.ratings:
            if len(r) > 0:
                ratingList.append(sum(r) / len(r))
                num += 1
        if num != 0:
            self.averageRating = sum(ratingList) / num
        return


@app.route("/view_professor_ratings", methods=['GET', 'POST'])
def view_professor_ratings():
    oc = offeredCourses.query.all()
    ratings = professorRatings.query.all()
    students = User.query.filter(User.role == 0).all()

    allRatings = []
    for o in oc:
        prof = None
        for a in allRatings:
            if a.prof == o.Prof:
                prof = a

        if prof is None:
            prof = ProfRatings(prof=o.Prof,
                               courses=[o.CourseCode])
            allRatings.append(prof)
        else:
            if o.CourseCode not in prof.courses:
                prof.courses.append(o.CourseCode)

    for r in ratings:
        for b in allRatings:
            if b.prof == r.Prof:
                print(f'PROF: {b.prof}\n')
                b.ratings[b.courses.index(r.CourseCode)].append(r.Rating)
                print(b.ratings)

    for a in allRatings:
        print(a.prof)
        print(a.courses)
        print(a.ratings)
        a.calcAverageRating()
        print(a.averageRating)
    # submissions = Submission.query.all()
    # grades = []
    # for s in students:
    #     # for
    #     temp = {'id': s.id, 'grade': 0.0, 'num': 0}
    #     grades.append(temp)
    #
    # for sub in submissions:
    #     for g in grades:
    #         if sub.submitter_id == g['id']:
    #             g['grade'] += sub.grade
    #             g['num'] += 1

    print(allRatings)
    return render_template('view_professor_ratings.html', ratings=allRatings)


@app.route("/assignments/current", methods=['GET', 'POST'])
@login_required
def view_assignments():
    posts = Post.query.filter(((Post.course == current_user.current_course_1) |
                              (Post.course == current_user.current_course_2) |
                              (Post.course == current_user.current_course_3) |
                              (Post.course == current_user.current_course_4) |
                              (Post.course == current_user.current_course_5) |
                              (Post.course == current_user.current_course_6))
                              & Post.assignment_flag == 1).all()
    return render_template('home.html', posts=posts, addSubmissionButton=True)


@app.route("/assignments/submit/<int:post_id>", methods=['GET', 'POST'])
@login_required
def submit_assignment(post_id):
    post = Post.query.get_or_404(post_id)
    form = SubmitAssignmentForm()
    if post.due_date:
        # now = pytz.utc.localize(datetime.now())
        # TODO: unhardcode this heh
        now = datetime(2021, 12, 21, 1, 1, 1)
        if now > post.due_date:
            flash('Past Due Date', 'danger')
            return redirect(url_for('view_assignments'))
    if form.validate_on_submit():
        submission = Submission(post_id=post_id,
                                submitter_id=current_user.id,
                                submission_notes=form.content.data,
                                assignment_title=post.title,
                                course=post.course)
        file_data = request.files.get(form.submissionFile.name)
        if file_data:
            submission.file_name = file_data.filename
            submission.file_data = file_data.read()
        db.session.add(submission)
        db.session.commit()
        flash('Your submission has been successful!', 'success')
        return redirect(url_for('view_assignments'))
    return render_template('new_submission.html', form=form, post=post)


@app.route("/assignments/view_submissions/", methods=['GET', 'POST'])
@login_required
def view_submissions():
    submissions = Submission.query.filter((Submission.course == current_user.current_course_1) |
                                          (Submission.course == current_user.current_course_2) |
                                          (Submission.course == current_user.current_course_3) |
                                          (Submission.course == current_user.current_course_4) |
                                          (Submission.course == current_user.current_course_5) |
                                          (Submission.course == current_user.current_course_6)).all()
    return render_template('view_submissions.html', submissions=submissions)


@app.route("/assignments/grade_submissions/<int:submission_id>", methods=['GET', 'POST'])
@login_required
def grade_submissions(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    form = GradeSubmissionForm()
    if form.validate_on_submit():
        # Update the submission
        submission.grading_notes = form.comments.data
        submission.grade = form.grade.data
        submission.grader_id = current_user.id
        submission.graded_flag = True
        db.session.commit()
        flash('Assignment has been graded successfully!', 'success')
        return redirect(url_for('view_submissions'))
    return render_template('grade_submissions.html', form=form, submission=submission)


@app.route("/view_grades", methods=['GET', 'POST'])
@login_required
def view_grades():
    if current_user.role == 0:
        submissions = Submission.query.filter(Submission.submitter_id == current_user.id)
    else:
        submissions = Submission.query.filter(Submission.grader_id == current_user.id)
    return render_template('view_grades.html', submissions=submissions)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    # courses = offeredCourses.query.with_entities(offeredCourses.CourseCode).filter_by(Prof=current_user.username).all()
    # courseList = []
    # for c in courses:
    #     courseList.append((c.CourseCode,c.CourseCode))
    courseList = set([current_user.current_course_1, current_user.current_course_2,
                      current_user.current_course_3, current_user.current_course_4,
                      current_user.current_course_5, current_user.current_course_6])
    courseList.discard(None)
    form = PostForm()

    form.course.choices = list(courseList)
    if form.validate_on_submit():
        file_data = request.files.get(form.assignmentFile.name)
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    course=form.course.data,
                    assignment_flag=False)
        if file_data:
            post.file_name = file_data.filename
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
    # courses = offeredCourses.query.with_entities(offeredCourses.CourseCode).filter_by(Prof=current_user.username).all()
    # courseList = []
    # for c in courses:
    #     courseList.append((c.CourseCode,c.CourseCode))
    courseList = set([current_user.current_course_1, current_user.current_course_2,
                      current_user.current_course_3, current_user.current_course_4,
                      current_user.current_course_5, current_user.current_course_6])
    courseList.discard(None)
    print(courseList)
    form = PostForm()
    form.course.choices = list(courseList)
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
            post.file_name = file_data.filename
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
