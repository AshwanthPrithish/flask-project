from flask import render_template,flash, redirect, url_for
from flask_project import app, db, bcrypt
from flask_project.forms import RegistrationForm, LoginForm, SPRegistrationForm, SPLoginForm
from flask_project.models import Student, Librarian, Book, BookIssue
from flask_login import login_user

with app.app_context():
  db.create_all()

BOOKS = [
    {
        "book_id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic",
        "rating": 7.5,
        "release_year": 1925
    },
    {
        "book_id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Fiction",
        "release_year": 1960
    },
    {
        "book_id": 3,
        "title": "1984",
        "author": "George Orwell",
        "genre": "Dystopian",
        "rating": 8,
        "release_year": 1949
    },
    {
        "book_id": 4,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "release_year": 1937
    },
    {
        "book_id": 5,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "genre": "Coming-of-age",
        "release_year": 1951
    }
]

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html", title="Home")

@app.route("/books")
def books():
  return render_template("books.html", book_list=BOOKS, title="Book List")

@app.route("/about-us")
def about_us():
  return render_template("about_us.html", title="About us")

@app.route("/contact")
def contact():
  return render_template("contact.html", title="Contact")

@app.route("/general-user")
def general_user():
  return render_template("general_user.html", title="General User")

@app.route("/librarian")
def librarian():
  return render_template("librarian.html", title="Librarian")


@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    student = Student(username=form.username.data, email=form.email.data, password=hashed_password)
    with app.app_context():
      db.session.add(student)
      db.session.commit()

    flash(f'Your Student Account has been created! Proceed to Login', 'success')
    return redirect(url_for("home"))
  return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    student = Student.query.filter_by(email=form.email.data).first()
    if student and bcrypt.check_password_hash(student.password, form.password.data):
      login_user(student, remember=form.remember.data)
      return redirect(url_for('home'))
    else:
      flash('Login unsuccessful, please check email, and password', 'danger')
  return render_template("login.html", title="Login", form=form)

@app.route("/sp-register", methods=['GET', 'POST'])
def sp_register():
  form = SPRegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    librarian = Librarian(username=form.username.data, email=form.email.data, admin_id=form.admin_id.data, password=hashed_password)
    with app.app_context():
      db.session.add(librarian)
      db.session.commit()

    flash(f'Account Created for Admin {form.username.data}!', 'success')
    return redirect(url_for("home"))
  return render_template("sp_register.html", title="Admin Register", form=form)

@app.route("/sp-login", methods=['GET', 'POST'])
def sp_login():
  form = SPLoginForm()
  if form.validate_on_submit():
    librarian = Librarian.query.filter_by(email=form.email.data).first()
    if librarian and bcrypt.check_password_hash(librarian.password, form.password.data):
      login_user(librarian, remember=form.remember.data)
      return redirect(url_for('home'))
    else:
      flash('Login unsuccessful, please check email, and password', 'danger')
  return render_template("sp_login.html", title="Admin Login", form=form)
