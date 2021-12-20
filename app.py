from flask import Flask, redirect, render_template, request, session, flash, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Course, Planner
from forms import RegisterUser, AddCourse, EditCourse, AddPlanner 
from sqlalchemy.exc import IntegrityError
import os 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///university'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = "curr_user"

connect_db(app)

####################################################################
# User signup/login/logout 


@app.before_request 
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None 

def do_login(user):
    """Login user."""
    session[CURR_USER_KEY] = user.id 

def do_logout():
    """Logout user."""
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def redirect_to_register():
    """Show homepage to logged in users; otherwise redirects to Register Page"""
    if g.user:
        # Get all courses for specific user 
        user = User.query.get(session[CURR_USER_KEY])
        courses = user.courses
        
        # Get the number of credits 
        creditsCount = 0
        
        for course in courses:
            creditsCount = creditsCount + course.num_credits
        # Get the number of courses 
        courseCount = len(courses)
        
        return render_template("home.html", user=user, courses=courses, courseCount=courseCount, creditsCount=creditsCount)
    else:
        return redirect('/register')
    
@app.route('/register', methods=["GET", "POST"])
def get_register_page():
    """Gets the Register Page"""
    form = RegisterUser()
    
    if form.validate_on_submit():
        try:
            # Create user instance 
            user = User.register(
                username=form.username.data, 
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data
            )
            
            # Save instance to database session 
            db.session.commit()
            
        except IntegrityError:
            flash("Username or Email already taken", "danger")
            return render_template("register.html", form=form)
            
        do_login(user)
        
        return redirect("/")
        
    else: 
        return render_template("register.html", form=form)        

@app.route("/logout")
def logout_user():
    """Handle logout of user"""
    do_logout()
    flash("Successfully logged out.")
    return redirect('/')
    
#################################################### Course Routes */
@app.route("/<userId>/add-course", methods=["GET", "POST"])
def add_course_page(userId):
    """Gets the add course page and handles form submits"""
    
    if g.user:
        form = AddCourse()
    
        if form.validate_on_submit():
            course = Course(name=form.name.data, num_credits=form.num_credits.data, class_id=form.class_id.data, user_id=session[CURR_USER_KEY])
        
            db.session.add(course)
            db.session.commit()
        
            return redirect('/')
        else:
            return render_template("add-course.html", form=form)
    else:
        return redirect('/')

@app.route("/<userId>/<courseId>/edit-course", methods=["GET", "POST"])
def edit_course_page(userId, courseId):
    """Gets the edit course page and handles form submits"""
    if g.user:
        course = Course.query.get(courseId)
    
        form = EditCourse(obj=course)
    
        if form.validate_on_submit():
            course.name = form.name.data 
            course.num_credits = form.num_credits.data
            course.class_id = form.num_credits.data
            course.finished = form.finished.data
        
            db.session.add(course)
            db.session.commit()
        
            return redirect('/')
        else:
            return render_template("edit-course.html", form=form)
    else:
        return redirect('/')

@app.route("/<userId>/<courseId>/delete-course")
def delete_course(userId, courseId):
    """Deletes a course"""
    if g.user:
        Course.query.filter_by(id=courseId).delete()
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
        
######################################################### Planner Routes 
@app.route('/<userId>/planner')
def display_planner_page(userId):
    """Displays the planner page"""
    if g.user:
        plans = Planner.query.all()
        return render_template("planner.html", userId=userId, plans=plans)
    else:
        return redirect("/")

@app.route('/<userId>/planner/create-new-planner', methods=["GET", "POST"])
def create_new_planner(userId):
    """Handles Creating a new planner"""
    if g.user:
        form = AddPlanner()
        
        if form.validate_on_submit():
            name = form.name.data 
            newPlanner = Planner(name=name, user_id=userId)
            db.session.add(newPlanner)
            db.session.commit()
            
            return redirect(f"/{userId}/planner")
        else:
            return render_template("add-planner.html", form=form)
    else:
        return redirect('/')

@app.route('/<userId>/planner/<plannerId>')
def display_planner_individual_page(userId, plannerId):
    """Displays a planner individual page"""
    if g.user:
        plan = Planner.query.get(plannerId)
        return render_template("planner-individual.html", plan=plan, userId=userId)
    else:
        return redirect('/')
        
@app.route('/<userId>/planner/<plannerId>/create-new-semester')
def create_new_semester(userId, plannerId):
    """Create New Semester"""
    if g.user:
        plan = Planner.query.get(plannerId)
        return render_template("add-semester.html", plan=plan, userId=userId)
    else:
        return redirect('/')
        
##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
        
        
        