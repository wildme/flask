import os
import click
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Departments
from app.models import Outbox

app = create_app('default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Departments=Departments, Outbox=Outbox)
