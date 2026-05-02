from datetime import datetime, date
from flask import render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Project, ProjectMember, Task
from app.tasks import tasks

def get_project_role(project_id):
    member = ProjectMember.query.filter_by(project_id=project_id, user_id=current_user.id).first()
    return member.role if member else None

@tasks.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        flash('Project ID is required to create a task.', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    project = Project.query.get_or_404(project_id)
    role = get_project_role(project_id)
    
    if not role:
        abort(403)
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date')
        assigned_to_id = request.form.get('assigned_to', type=int)
        
        # Validations
        if not title or len(title) < 3 or len(title) > 200:
            flash('Title must be between 3 and 200 characters.', 'danger')
            return render_template('tasks/create.html', project=project, role=role)
            
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if due_date < date.today():
                    flash('Due date cannot be in the past.', 'danger')
                    return render_template('tasks/create.html', project=project, role=role)
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('tasks/create.html', project=project, role=role)
        
        # Assignment logic
        if assigned_to_id:
            # Check if assigned_to is a member of the project
            is_member = ProjectMember.query.filter_by(project_id=project_id, user_id=assigned_to_id).first()
            if not is_member:
                flash('Assigned user must be a member of the project.', 'danger')
                return render_template('tasks/create.html', project=project, role=role)
                
            # RBAC for assignment
            if role != 'admin' and assigned_to_id != current_user.id:
                flash('Members can only assign tasks to themselves.', 'danger')
                return render_template('tasks/create.html', project=project, role=role)
        
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            project_id=project_id,
            created_by=current_user.id,
            assigned_to=assigned_to_id
        )
        db.session.add(new_task)
        db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('projects.detail', id=project_id))
        
    return render_template('tasks/create.html', project=project, role=role)

@tasks.route('/<int:id>')
@login_required
def detail(id):
    task = Task.query.get_or_404(id)
    role = get_project_role(task.project_id)
    
    if not role:
        abort(403)
        
    return render_template('tasks/detail.html', task=task, role=role)

@tasks.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.get_or_404(id)
    project_id = task.project_id
    role = get_project_role(project_id)
    
    if not role:
        abort(403)
        
    # RBAC: Admins can edit anything. Members can edit their own tasks.
    if role != 'admin' and task.created_by != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('tasks.detail', id=id))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        status = request.form.get('status')
        due_date_str = request.form.get('due_date')
        assigned_to_id = request.form.get('assigned_to', type=int)
        
        if not title or len(title) < 3 or len(title) > 200:
            flash('Title must be between 3 and 200 characters.', 'danger')
            return render_template('tasks/edit.html', task=task, role=role)
            
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('tasks/edit.html', task=task, role=role)
        else:
            task.due_date = None
            
        # Assignment logic (Admins only can change assignee)
        if assigned_to_id and assigned_to_id != task.assigned_to:
            if role != 'admin':
                flash('Only admins can change task assignment.', 'danger')
            else:
                is_member = ProjectMember.query.filter_by(project_id=project_id, user_id=assigned_to_id).first()
                if is_member:
                    task.assigned_to = assigned_to_id
                else:
                    flash('Selected user is not a member of the project.', 'danger')

        task.title = title
        task.description = description
        task.priority = priority
        task.status = status
        
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('tasks.detail', id=id))
        
    return render_template('tasks/edit.html', task=task, role=role)

@tasks.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    role = get_project_role(task.project_id)
    
    # Only Admins can delete tasks
    if role != 'admin':
        flash('Only project admins can delete tasks.', 'danger')
        return redirect(url_for('tasks.detail', id=id))
        
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('projects.detail', id=project_id))

@tasks.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    task = Task.query.get_or_404(id)
    role = get_project_role(task.project_id)
    
    if not role:
        return jsonify({'error': 'Access denied'}), 403
        
    # Admins can change status of any task. Members can change status of tasks assigned to them.
    if role != 'admin' and task.assigned_to != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
        
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status in ['todo', 'in_progress', 'done']:
        task.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'new_status': new_status})
    
    return jsonify({'error': 'Invalid status'}), 400
