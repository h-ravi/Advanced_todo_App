from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, ProfileForm
from . import db, oauth
from .models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully', 'success')
            return redirect(url_for('main.index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('Email already registered', 'warning')
        else:
            user = User(email=form.email.data.lower())
            user.set_password(form.password.data)
            # Auto create admin user if matches provided admin email
            if user.email == 'admin@admin.com':
                user.is_admin = True
            db.session.add(user)
            db.session.commit()
            flash('Registration successful, please login', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))

# OAuth routes
@auth_bp.route('/login/<provider>')
def oauth_login(provider):
    client = oauth.create_client(provider)
    if not client:
        flash('Unsupported provider', 'danger')
        return redirect(url_for('auth.login'))
    redirect_uri = url_for('auth.oauth_callback', provider=provider, _external=True)
    return client.authorize_redirect(redirect_uri)

@auth_bp.route('/callback/<provider>')
def oauth_callback(provider):
    client = oauth.create_client(provider)
    if not client:
        flash('Unsupported provider', 'danger')
        return redirect(url_for('auth.login'))
    token = client.authorize_access_token()
    user_info = None
    email = None
    sub = None
    if provider == 'google':
        user_info = client.parse_id_token(token)
        email = user_info.get('email')
        sub = user_info.get('sub')
    elif provider == 'github':
        resp = client.get('user', token=token)
        gh_user = resp.json()
        email = gh_user.get('email')
        if not email:
            # fetch primary email
            emails_resp = client.get('user/emails', token=token)
            for e in emails_resp.json():
                if e.get('primary'):
                    email = e.get('email')
                    break
        sub = str(gh_user.get('id'))
    elif provider == 'facebook':
        resp = client.get('me?fields=id,name,email', token=token)
        fb_user = resp.json()
        email = fb_user.get('email')
        sub = fb_user.get('id')

    if not email:
        flash('Unable to retrieve email from provider', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email.lower()).first()
    if not user:
        user = User(email=email.lower(), oauth_provider=provider, oauth_sub=sub)
        if email.lower() == 'admin@admin.com':
            user.is_admin = True
        db.session.add(user)
    else:
        user.oauth_provider = provider
        user.oauth_sub = sub
    db.session.commit()
    login_user(user)
    flash('Logged in via ' + provider, 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Password change (if both provided)
        if form.new_password.data:
            if not current_user.check_password(form.current_password.data or ''):
                flash('Current password incorrect', 'danger')
                return render_template('profile.html', form=form)
            current_user.set_password(form.new_password.data)
            flash('Password updated', 'success')
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.avatar = form.avatar.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html', form=form)
