from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    db.app = app 
    db.init_app(app)
    
class User(db.Model):
    """Defines a user instance"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    
    courses = db.relationship('Course', backref="users", cascade="all")
    
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user w/hashed password & return user."""
        
        hashed = bcrypt.generate_password_hash(password)
        
        # turn bytestring into normal (unicode utf8) string 
        hashed_utf8 = hashed.decode("utf8")
        
        # Create instance of user 
        user = User(username=username, email=email, password=hashed_utf8, first_name=first_name, last_name=last_name)
        
        db.session.add(user)
        
        # return instance of user w/username and hashed password 
        return user
        
    @classmethod 
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct."""
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user 
        else:
            return False 

class Course(db.Model):
    """Defines a course instance"""
    
    __tablename__ = "courses"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    num_credits = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.String(30), nullable=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    semesters = db.relationship('Semester', secondary='semesterCourse', back_populates='courses')
    
class Semester(db.Model):
    """Defines a semester instance"""
    
    __tablename__ = "semesters"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    planner_id = db.Column(db.Integer, db.ForeignKey('planners.id', ondelete='CASCADE'), nullable=False)
    
    courses = db.relationship('Course', secondary='semesterCourse', back_populates='semesters')
    
class Planner(db.Model):
    """Defines a planner instance"""
    
    __tablename__ = "planners"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    semesters = db.relationship("Semester", backref="planners")
    
semester_course_table = db.Table('semesterCourse',
    db.Column('semester_id', db.ForeignKey('semesters.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    db.Column('course_id', db.ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True, nullable=False))

    