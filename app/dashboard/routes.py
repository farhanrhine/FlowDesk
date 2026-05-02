from flask import render_template
from flask_login import login_required
from app.dashboard import dashboard

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def index():
    return "<h1>Welcome to your Dashboard (Coming in Phase 5)</h1><p><a href='/auth/logout'>Logout</a></p>"
