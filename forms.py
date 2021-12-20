from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email 

class RegisterUser(FlaskForm):
    """Form for registering new users"""
    
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])

class LoginUser(FlaskForm):
    """Form for logging in returning users"""
    
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class AddCourse(FlaskForm):
    """Form for adding courses"""
    
    name = StringField("Name", validators=[InputRequired()])
    num_credits = IntegerField("Number of Credits", validators=[InputRequired()])
    class_id = StringField("Class ID", validators=[InputRequired()])

class EditCourse(FlaskForm):
    """Form for editing courses"""
    
    name = StringField("Name", validators=[InputRequired()])
    num_credits = IntegerField("Number of Credits", validators=[InputRequired()])
    class_id = StringField("Class ID", validators=[InputRequired()])
    finished = BooleanField("Finished")

class AddPlanner(FlaskForm):
    """Form for creating a new plan"""
    
    name = StringField("Name", validators=[InputRequired()])