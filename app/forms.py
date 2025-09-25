from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    submit = SubmitField('Add Task')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[Optional(), Length(max=120)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    avatar = StringField('Avatar URL', validators=[Optional(), Length(max=255)])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    submit = SubmitField('Save Changes')

class AdminUserEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[Optional(), Length(max=120)])
    new_password = PasswordField('Reset Password', validators=[Optional(), Length(min=6)])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Update User')
