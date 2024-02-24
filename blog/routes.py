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

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    form = EntryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            flash('Wpis został dodany pomyślnie!', 'success')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Błąd w polu {getattr(form, field).label.text}: {error}', 'danger')
    return render_template("entry_form.html", form=form)



@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            flash('Wpis został zaktualizowany pomyślnie!', 'success')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Błąd w polu {getattr(form, field).label.text}: {error}', 'danger')
    return render_template("entry_form.html", form=form)
