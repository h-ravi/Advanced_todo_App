from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from .models import User, Task
from .forms import AdminUserEditForm
from . import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    users = User.query.order_by(User.created_at.desc()).all()
    # Build per-user recent tasks (limit 5 each) for display
    user_tasks = {u.id: Task.query.filter_by(user_id=u.id).order_by(Task.created_at.desc()).limit(5).all() for u in users}
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(completed=True).count()
    return render_template('admin_dashboard.html', users=users, user_tasks=user_tasks,
                           total_tasks=total_tasks, completed_tasks=completed_tasks)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if current_user.id == user_id:
        flash('You cannot delete yourself', 'warning')
        return redirect(url_for('admin.dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/user/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    wants_json = request.headers.get('Accept', '').startswith('application/json') or request.is_json
    data = request.get_json() if request.is_json else request.form
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    is_admin = data.get('is_admin') in ('true', 'on', True, '1')
    if not email or '@' not in email:
        msg = 'Valid email required'
        if wants_json:
            return jsonify({'status': 'error', 'message': msg}), 400
        flash(msg, 'danger')
        return redirect(url_for('admin.dashboard'))
    if User.query.filter_by(email=email).first():
        msg = 'Email already exists'
        if wants_json:
            return jsonify({'status': 'error', 'message': msg}), 400
        flash(msg, 'warning')
        return redirect(url_for('admin.dashboard'))
    user = User(email=email, is_admin=is_admin)
    if password:
        user.set_password(password)
    db.session.add(user)
    db.session.commit()
    if wants_json:
        return jsonify({'status': 'ok', 'user': {
            'id': user.id,
            'email': user.email,
            'is_admin': user.is_admin,
            'tasks': 0
        }})
    flash('User created', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm(obj=user)
    if form.validate_on_submit():
        # Email uniqueness check
        existing = User.query.filter(User.email == form.email.data.lower(), User.id != user.id).first()
        if existing:
            flash('Email already in use', 'danger')
            return render_template('admin_user_edit.html', form=form, user=user)
        user.email = form.email.data.lower()
        user.name = form.name.data
        user.is_admin = form.is_admin.data
        if form.new_password.data:
            user.set_password(form.new_password.data)
        db.session.commit()
        flash('User updated', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin_user_edit.html', form=form, user=user)
