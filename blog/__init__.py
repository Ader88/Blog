from flask import Flask, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from blog import routes, models

@app.shell_context_processor
def make_shell_context():
    return {
        "app": app,
        "db": db,
        "Entry": models.Entry
    }

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Aby uzyskać dostęp do tej strony, musisz się zalogować.', 'warning')
    return redirect(url_for('login'))

login_manager.login_view = 'login'
