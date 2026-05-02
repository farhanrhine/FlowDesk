from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, Project, ProjectMember, Task
from app.projects import projects

def get_project_role(project_id):
    """Helper to get the current user's role in a project."""
    member = ProjectMember.query.filter_by(project_id=project_id, user_id=current_user.id).first()
    return member.role if member else None

@projects.route('/')
@login_required
def list_projects():
    # Get all projects the user is a member of
    memberships = ProjectMember.query.filter_by(user_id=current_user.id).all()
    user_projects = [m.project for m in memberships]
    return render_template('projects/list.html', projects=user_projects)

@projects.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name or len(name) < 3 or len(name) > 120:
            flash('Project name must be between 3 and 120 characters.', 'danger')
            return render_template('projects/create.html')
            
        new_project = Project(name=name, description=description, owner_id=current_user.id)
        db.session.add(new_project)
        db.session.flush() # Get the ID before committing
        
        # Add creator as admin member
        admin_member = ProjectMember(project_id=new_project.id, user_id=current_user.id, role='admin')
        db.session.add(admin_member)
        db.session.commit()
        
        flash(f'Project "{name}" created successfully!', 'success')
        return redirect(url_for('projects.detail', id=new_project.id))
        
    return render_template('projects/create.html')

@projects.route('/<int:id>')
@login_required
def detail(id):
    project = Project.query.get_or_404(id)
    role = get_project_role(id)
    
    if not role:
        abort(403) # User is not a member of this project
        
    return render_template('projects/detail.html', project=project, role=role)

@projects.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    project = Project.query.get_or_404(id)
    role = get_project_role(id)
    
    if role != 'admin':
        flash('Only project admins can edit project details.', 'danger')
        return redirect(url_for('projects.detail', id=id))
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name or len(name) < 3 or len(name) > 120:
            flash('Project name must be between 3 and 120 characters.', 'danger')
            return render_template('projects/edit.html', project=project)
            
        project.name = name
        project.description = description
        db.session.commit()
        
        flash('Project updated successfully.', 'success')
        return redirect(url_for('projects.detail', id=id))
        
    return render_template('projects/edit.html', project=project)

@projects.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    project = Project.query.get_or_404(id)
    role = get_project_role(id)
    
    if role != 'admin':
        flash('Only project admins can delete projects.', 'danger')
        return redirect(url_for('projects.detail', id=id))
        
    # Check for tasks
    if project.tasks:
        confirm = request.form.get('confirm_delete_tasks')
        if not confirm:
            flash('Cannot delete project with existing tasks. Please confirm deletion of all associated tasks.', 'warning')
            return redirect(url_for('projects.detail', id=id))
            
    db.session.delete(project)
    db.session.commit()
    flash('Project and all associated data deleted.', 'success')
    return redirect(url_for('projects.list_projects'))

@projects.route('/<int:id>/add-member', methods=['POST'])
@login_required
def add_member(id):
    project = Project.query.get_or_404(id)
    role = get_project_role(id)
    
    if role != 'admin':
        flash('Only project admins can manage members.', 'danger')
        return redirect(url_for('projects.detail', id=id))
        
    email = request.form.get('email')
    new_member_role = request.form.get('role', 'member')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(f'No user found with email {email}.', 'danger')
        return redirect(url_for('projects.detail', id=id))
        
    # Check if already a member
    existing = ProjectMember.query.filter_by(project_id=id, user_id=user.id).first()
    if existing:
        flash(f'{user.username} is already a member of this project.', 'info')
        return redirect(url_for('projects.detail', id=id))
        
    new_member = ProjectMember(project_id=id, user_id=user.id, role=new_member_role)
    db.session.add(new_member)
    db.session.commit()
    
    flash(f'{user.username} added to project as {new_member_role}.', 'success')
    return redirect(url_for('projects.detail', id=id))

@projects.route('/<int:id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(id, user_id):
    project = Project.query.get_or_404(id)
    role = get_project_role(id)
    
    if role != 'admin':
        flash('Only project admins can manage members.', 'danger')
        return redirect(url_for('projects.detail', id=id))
        
    # Check if removing self
    if user_id == current_user.id:
        # Check if last admin
        admin_count = ProjectMember.query.filter_by(project_id=id, role='admin').count()
        if admin_count <= 1:
            flash('Cannot remove yourself as you are the last admin. Appoint another admin first.', 'danger')
            return redirect(url_for('projects.detail', id=id))
            
    member = ProjectMember.query.filter_by(project_id=id, user_id=user_id).first_or_404()
    db.session.delete(member)
    db.session.commit()
    
    flash('Member removed from project.', 'success')
    return redirect(url_for('projects.detail', id=id))
