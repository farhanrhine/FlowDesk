from datetime import date
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_
from app.models import Task, Project
from app.dashboard import dashboard

@dashboard.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@dashboard.route('/dashboard')
@login_required
def index():
    today = date.today()
    
    # My Tasks Today: Assigned to user, due_date = today
    tasks_today = Task.query.filter(
        and_(Task.assigned_to == current_user.id, Task.due_date == today, Task.status != 'done')
    ).all()
    
    # In Progress: Count of user's tasks with status = in_progress
    in_progress_count = Task.query.filter(
        and_(Task.assigned_to == current_user.id, Task.status == 'in_progress')
    ).count()
    
    # Overdue: Tasks where due_date < today AND status != 'done'
    overdue_tasks = Task.query.filter(
        and_(Task.assigned_to == current_user.id, Task.due_date < today, Task.status != 'done')
    ).all()
    
    # 4. Team Tasks: All tasks in projects the user is a member of
    user_project_ids = [m.project_id for m in current_user.project_memberships]
    team_tasks = Task.query.filter(Task.project_id.in_(user_project_ids)).order_by(Task.due_date.asc().nullslast()).all()
    
    return render_template(
        'dashboard/index.html',
        tasks_today=tasks_today,
        in_progress_count=in_progress_count,
        overdue_tasks=overdue_tasks,
        all_my_tasks=team_tasks
    )
