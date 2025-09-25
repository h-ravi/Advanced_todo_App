from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .forms import TaskForm
from .models import Task
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    form = TaskForm()
    status = request.args.get('status')  # 'active' | 'completed' | None
    q = Task.query.filter_by(user_id=current_user.id)
    if status == 'active':
        q = q.filter_by(completed=False)
    elif status == 'completed':
        q = q.filter_by(completed=True)
    tasks = q.order_by(Task.created_at.desc()).all()
    return render_template('index.html', form=form, tasks=tasks, status=status)

@main_bp.route('/task/add', methods=['POST'])
@login_required
def add_task():
    form = TaskForm()
    wants_json = request.headers.get('Accept', '').startswith('application/json') or \
        request.headers.get('X-Requested-With') == 'fetch'
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        if wants_json:
            html = render_template('_task_item.html', task=task)
            total = Task.query.filter_by(user_id=current_user.id).count()
            completed = Task.query.filter_by(user_id=current_user.id, completed=True).count()
            return jsonify({
                'status': 'ok',
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'created_at': task.created_at.strftime('%Y-%m-%d %H:%M'),
                    'completed': task.completed
                },
                'html': html,
                'counts': {
                    'total': total,
                    'completed': completed,
                    'active': total - completed
                }
            }), 201
        flash('Task added', 'success')
        return redirect(url_for('main.index'))
    else:
        if wants_json:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        flash('Error adding task', 'danger')
        return redirect(url_for('main.index'))

@main_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'status': 'ok', 'completed': task.completed})

@main_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted', 'info')
    return redirect(url_for('main.index'))
