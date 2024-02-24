from flask import render_template, request, flash, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
from utils import generate_entries

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/generate_entries")
def generate_blog_entries():
    generate_entries(10)
    return "Wpisy zostały wygenerowane."

def save_entry(form, entry=None):
    if entry is None:
        entry = Entry()
    form.populate_obj(entry)
    db.session.add(entry)
    db.session.commit()
    flash('Wpis został zaktualizowany pomyślnie!', 'success' if entry.id else 'success')
    return entry

@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_or_create_entry(entry_id=None):
    entry = Entry.query.get_or_404(entry_id) if entry_id else None
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        save_entry(form, entry)
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Błąd w polu {getattr(form, field).label.text}: {error}', 'danger')
    return render_template("entry_form.html", form=form)
    
