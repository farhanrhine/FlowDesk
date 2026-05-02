from flask import Blueprint

projects = Blueprint('projects', __name__)

from app.projects import routes
