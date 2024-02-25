from flask import render_template, request, flash, redirect, url_for, session
from blog import app
from blog.models import Entry, db, User
from blog.forms import EntryForm, LoginForm
from utils import generate_entries
from flask_login import login_required, current_user, logout_user, login_user
from config import Config

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/generate_entries")
def generate_blog_entries():
    generate_entries(10)
    return "Wpisy zostały wygenerowane."

def save_entry(form, entry=None):
    if entry is None:
        entry = Entry()
    form.populate_obj(entry)
    entry.author = current_user  # Dodajemy informację o autorze wpisu
    db.session.add(entry)
    db.session.commit()
    flash('Wpis został zaktualizowany pomyślnie!', 'success' if entry.id else 'success')
    return entry

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def new_post():
    form = EntryForm()
    if form.validate_on_submit():
        entry = save_entry(form)
        return redirect(url_for('index'))
    return render_template("entry_form.html", form=form)
    
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_post(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    form = EntryForm(obj=entry)
    
    # Dodaj warunek sprawdzający czy użytkownik jest autorem wpisu
    if entry.author != current_user:
        flash("You are not authorized to edit this post", "error")
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        save_entry(form, entry)
        return redirect(url_for('index'))
    return render_template("entry_form.html", form=form, entry_id=entry_id)
    
@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Sprawdzenie czy podane dane logowania są zgodne z danymi w pliku konfiguracyjnym
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            user = User.query.filter_by(username=username).first()
            if user:
                login_user(user)
                flash('You are now logged in.', 'success')
                return redirect(url_for('index'))
            else:
                flash('User not found.', 'error')
        else:
            flash('Invalid username or password', 'error')
    return render_template("login_form.html", form=form)

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('index'))
