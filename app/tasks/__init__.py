from flask import Blueprint

tasks = Blueprint('tasks', __name__)

from app.tasks import routes
