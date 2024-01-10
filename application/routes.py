from flask import render_template, flash, session, redirect, url_for

from application import app, db
from application.utils import login_required

from application.models import User, Note
from application.forms import *

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # user_id = session.get(session("user.id"))
    user = User.query.get(session("user.id"))
    notes = user.notes
    notes = user.notes.all()

    return render_template("index.html", notes=notes)

@app.route("/delete/<int:note_id>")
@login_required
def delete(note_id):
    note = Note.query.filter(Note.id == note_id, Note.created_by==session['user_id']).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully", "success")
    else:
        flash("Note not found", "warning")
    return redirect(url_for("index"))

@app.route("/update/<int:note_id>", methods=["GET", "POST"])
@login_required
def update(note_id):
    form = CreateNoteForm()
    note = Note.query.filter(Note.id == note_id, Note.created_by == session['user_id']).first()
    # note = Note.query.filter_by(id=note_id, created_by=session['user_id']).first()
        if form.validate_on_submit():
            new_note = form.note.data
            note.note = new_note
            db.session.commit()
            flash("Note updated successfully", "success")
            return redirect(url_for("index"))

        return render_template("note_detail.html", note=note, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                session["user_id"] = user.id
                flash("Login successful", "success")
                return redirect(url_for("index"))
        flash("Invalid username or password", "warning")
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    # session.pop("user_id", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))
    