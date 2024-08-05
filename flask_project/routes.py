import secrets
import os
import re
import pdfkit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import jwt

from datetime import datetime, timedelta
from PIL import Image
from flask import render_template,flash, redirect, url_for, request, make_response, jsonify
from flask_project import app, db, bcrypt
from flask_project.forms import BookRequestForm, RegistrationForm, LoginForm, SPRegistrationForm, SPLoginForm, UpdateStudentAccount, UpdateSPAccount, SectionForm, BookAddForm, FeedBackForm, SearchSectionForm, SearchTitleForm, SearchAuthorForm
from flask_project.models import Student, Librarian, Book, BookIssue, Genre, BookRequest, FeedBack
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from flask_project.auth_middleware import token_required
from flask_wtf.csrf import CSRFProtect, generate_csrf

csrf = CSRFProtect(app)

with app.app_context():
  db.create_all()


@app.route("/auth_status", methods=["GET"])
def auth_status():
    
    csrf_token = generate_csrf()
    if current_user.is_authenticated:
        if current_user.role == 'student':
            student = Student.query.filter_by(id=current_user.id).first()
            user_info = {
                  'isAuthenticated': 'True',
                  'role': current_user.role,
                  'username':   student.username,
                  'email': student.email,
                  'csrf':csrf_token,
                  'id': current_user.id
            }
        else: 
            librarian = Librarian.query.filter_by(id=current_user.id).first()
            user_info = {
                  'isAuthenticated': 'True',
                  'role': current_user.role,
                  'username':   librarian.username,
                  'email': librarian.email,
                  'csrf':csrf_token,
                  'id': current_user.id
            }
    else:
        user_info = {'is_authenticated': False, "role": '', 'csrf': csrf_token, 'id':'null'}
    
    return jsonify(user_info)

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html", title="Home")

@app.route("/student-dash", methods=['GET', 'POST'])
@login_required
def student_dash():
   if current_user.role == "student":
        return jsonify({
            'username': current_user.username,
            'role': current_user.role
        })
   else:
        return jsonify({'error': 'Access Denied! You do not have permission to view this page.'}), 403


@app.route("/register", methods=['POST'])
def register():
   if current_user.is_authenticated:
        if current_user.role == "librarian":
            return jsonify({'redirect': url_for('sp_dash')}), 200
        else:
            return jsonify({'message': "Access Denied! You do not have permission to view this page."}), 403
        
   data = request.get_json()
   form = RegistrationForm(data=data)
   if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      student = Student(username=form.username.data, email=form.email.data, password=hashed_password)
      with app.app_context():
            db.session.add(student)
            db.session.commit()

      return jsonify({'message': f'Account Created for Student {form.username.data}!'}), 201

   errors = {field: form.errors.get(field, []) for field in form.errors}
   return jsonify({'errors': errors}), 400  


@app.route("/login", methods=['GET', 'POST'])
def login():
  try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No input data provided', 'success': False}), 400
        
        data['remember'] = True if data['remember'] == 'true' else False
        form = LoginForm(data=data)
        if form.validate_on_submit():
         student = Student.query.filter_by(email=form.email.data).first()
         if not student:
            return jsonify({'message': 'Invalid credentials', 'success': False}), 401
         if bcrypt.check_password_hash(student.password, form.password.data):
               token = jwt.encode({'email': form.email.data, 'role': 'student'}, app.config['SECRET_KEY'])
               login_user(student, remember=data['remember'])
               return jsonify({
                  'token': token,
                  'success': True,
                  'isAuthenticated': 'True',
                  'role': current_user.role,
                  'username': student.username,
                  'email': student.email
               }), 200
         else:
            return jsonify({'message': 'Invalid credentials', 'success': False}), 401
         
        else:
            errors = {field: form.errors.get(field, []) for field in form.errors}
            return jsonify({'errors': errors}), 200  
        
        
  except Exception as e:
        return jsonify({'message': str(e), 'success': False}), 500


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    if current_user.is_authenticated:
      logout_user()
      return jsonify({"message": "Successfully logged out"}), 200
    else:
       return jsonify({"message": "Unexpected error"}), 200



@app.route("/sp-register", methods=['POST'])
def sp_register():
    if current_user.is_authenticated:
        if current_user.role == "librarian":
            return jsonify({'redirect': url_for('sp_dash')}), 200
        else:
            return jsonify({'message': "Access Denied! You do not have permission to view this page."}), 403

    data = request.get_json()
    form = SPRegistrationForm(data=data)
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        librarian = Librarian(username=form.username.data, email=form.email.data, admin_id=form.admin_id.data, password=hashed_password)
        with app.app_context():
            db.session.add(librarian)
            db.session.commit()

        return jsonify({'message': f'Account Created for Admin {form.username.data}!'}), 201

    errors = {field: form.errors.get(field, []) for field in form.errors}
    return jsonify({'errors': errors}), 200

@app.route("/sp-login", methods=['GET', 'POST'])
def sp_login():
   form = SPLoginForm()
   if current_user.is_authenticated:
         if current_user.role == "librarian":
               return jsonify({'redirect': url_for('sp_dash')}), 200
         else:
               return jsonify({'message': "Access Denied! You do not have permission to view this page."}), 403

   data = request.get_json()
   data['remember'] = True if data['remember'] == 'true' else False 
   form = SPLoginForm(data=data)
      
   if form.validate():
      librarian = Librarian.query.filter_by(email=form.email.data).first()
      if not librarian:
         return jsonify(message="Login unsuccessful, please check email and password", success= False), 401
      if librarian and bcrypt.check_password_hash(librarian.password, form.password.data):
               login_user(librarian, remember=form.remember.data)
               token = jwt.encode({'email': form.email.data, 'role': 'librarian'}, app.config['SECRET_KEY'])
               return jsonify({'message':"Login successful",'token':token,'success':True}), 200
      else:
               return jsonify(message="Login unsuccessful, please check email and password", success= False), 401

   return jsonify(message="Form validation failed", errors=form.errors,success=False), 400


@app.route("/section/new", methods=['GET', 'POST'])
@login_required
def new_section():

  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role} acc", "danger")
    return redirect(url_for("home"))
  
  data = request.get_json()
  d = data['date_created']
  d = datetime.strptime(d, "%Y-%m-%d")
  data['date_created'] = d.strftime("%d-%m-%Y")
  form = SectionForm(data=data)
  if form.validate_on_submit():
      if form.date_created.data == '':
        section = Genre(name=form.title.data, description=form.content.data, librarian_id=current_user.id)
      else:
        if len(Genre.query.filter(func.lower(Genre.name).ilike(f"%{form.title.data.lower()}%")).all()) > 0:
           return jsonify(message='Section with that name already exists!', success=True), 200
        
        section = Genre(name=form.title.data, description=form.content.data, date_created=d, librarian_id=current_user.id)
      with app.app_context():
         db.session.add(section)
         db.session.commit()
         return jsonify(message = 'The Section has been created!', success=True), 200
  return jsonify(message="Error",errors={field: form.errors.get(field, []) for field in form.errors}), 200


@app.route("/sections")
@login_required
def sections():
  with app.app_context():
     sections_ = Genre.query.all()
     sections_ = [[i.to_dict(), Librarian.query.filter_by(id=i.librarian_id).first().username] for i in sections_]
  return jsonify(sections=sections_, success=True), 200



@app.route("/search-results-author", methods=["GET", "POST"])
@login_required
def search_results_author():
   data = request.get_json()
   query = data['author']
   books = Book.query.filter(func.lower(Book.author).ilike(f"%{query.lower()}%")).all()
   books = [[{'title':book.title, 'author':book.author,'lang': book.lang ,'content':book.content, 'rating':book.rating, 'release_year':book.release_year,'id':book.id},book.genre_id, Genre.query.filter_by(id=book.genre_id).first().name] for book in books]
   if current_user.role == 'student':
           for book in books:
              if len(BookIssue.query.filter_by(student_id=current_user.id, book_id=book[0].get('id')).all()) <= 0:
                 del book[0]['content']
   books.sort(key = lambda x: x[0].get('rating'), reverse=True)
   if len(books) <= 0:
      return jsonify(message="No books found", success=True), 200
   return jsonify(books=books, success=True),200


@app.route("/search-results-section", methods=["GET", "POST"])
@login_required
def search_results_section():
   data = request.get_json()
   query = data['section']
   sections = Genre.query.filter(func.lower(Genre.name).ilike(f"%{query.lower()}%")).all()
   sections = [[{'id':genre.id,'name':genre.name, 'date_created':genre.date_created,'description': genre.description ,'librarian_username':Librarian.query.filter_by(id=genre.librarian_id).first().username}] for genre in sections]
   if len(sections) <= 0:
      return jsonify(message=f'No sections found for the query {query}!', success=True),200
   return jsonify(sections=sections, success=True), 200


@app.route("/section", methods=["GET","POST"])
@login_required
def section():
  with app.app_context():
    section_id=request.get_json()['section_id']
    section = Genre.query.get_or_404(section_id)

    librarian_username = Librarian.query.filter_by(id=section.librarian_id).first().username
    section = section.to_dict()
    section.update({'librarian_username': librarian_username})
    books = Book.query.filter_by(genre_id=section_id).all()
    books = [{'title':book.title, 'author':book.author, 'lang': book.lang,'content':book.content, 'rating':book.rating, 'release_year':book.release_year,'id':book.id} for book in books]
    if current_user.role == 'student':
           for book in books:
              if len(BookIssue.query.filter_by(student_id=current_user.id, book_id=book.get('id')).all()) <= 0:
                 del book['content']
              
  return jsonify(success=True,section=section,book_list=books),200



@app.route("/delete-section", methods=['POST'])
@login_required
def delete_section():
  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return jsonify(success=False, message="Unauthorized action")
  
  section_id=request.get_json()['section_id']
  with app.app_context():
     section = Genre.query.get_or_404(section_id)
     books = Book.query.filter_by(genre_id=section_id).all()
     for book in books:
        feedbacks = FeedBack.query.filter_by(book_id=book.id).all()
        for feedback in feedbacks:
           db.session.delete(feedback)
           db.session.commit()
        db.session.delete(book)
        db.session.commit()
     db.session.delete(section)
     db.session.commit()
     flash('Section Deleted!', 'success')
     return jsonify(success=True, message="Successfully deleted the section")



@app.route("/section/update", methods=['GET', 'POST'])
@login_required
def update_section():
  if current_user.role != "librarian":
    return jsonify(message=f"Access Denied! You do not have permission to view this page.{current_user.role} acc", success=False)
  
  data = request.get_json()
  section_id = data['section_id']
  data = data['data']
  section = Genre.query.get_or_404(section_id)
  form = SectionForm(data=data)
  if form.validate_on_submit():
     if section.name.lower() != form.title.data.lower() and len(Genre.query.filter(func.lower(Genre.name).ilike(f"%{form.title.data.lower()}%")).all()) > 0:
           return jsonify(message='Section with that name already exists!',success=False)
     section.name = form.title.data
     section.description = form.content.data
     section.date_created = form.date_created.data
     section.librarian_id = current_user.id
     db.session.commit()
     return jsonify(message=f'Updated the Section successfully', success=True)
  elif request.method == 'GET':
    form.title.data = section.name
    form.content.data = section.description
    form.date_created.data = section.date_created
  return render_template('create_section.html', title='Update Section', section=section, form=form, legend='Update Section')
  


















@app.route("/search-results-title/<query>")
@login_required
def search_results_title(query):
   titles = Book.query.filter(func.lower(Book.title).ilike(f"%{query.lower()}%")).all()
   books = [[{'title':book.title, 'author':book.author,'lang': book.lang ,'content':book.content, 'rating':book.rating, 'release_year':book.release_year,'id':book.id},book.genre_id, Genre.query.filter_by(id=book.genre_id).first().name] for book in titles]
   if current_user.role == 'student':
           for book in books:
              if len(BookIssue.query.filter_by(student_id=current_user.id, book_id=book[0].get('id')).all()) <= 0:
                 del book[0]['content']
   books.sort(key = lambda x: x[0].get('rating'), reverse=True)
   if len(books) <= 0:
      flash(f'No books found for the query {query}!', 'danger')
      return redirect(url_for('student_dash'))
   return render_template('search_results_title.html', titles=books, title='Search by book title')


@app.route("/sp-dash", methods=['GET', 'POST'])
@login_required
def sp_dash():
  if current_user.role == "librarian":
       
       form = SearchSectionForm()
       if form.validate_on_submit():
          section = form.section.data
          flash(f'{section}', 'success')
          return redirect(url_for('search_results_section', query=section))
       form1 = SearchTitleForm()
       if form1.validate_on_submit():
          title = form1.title.data
          flash(f'{title}', 'success')
          return redirect(url_for('search_results_title', query=title))
       form2 = SearchAuthorForm()
       if form2.validate_on_submit():
          author = form2.author.data
          return redirect(url_for('search_results_author', query=author))
       
       book_issues = BookIssue.query.all()
       book_issues = [[book_issue.issue_date, book_issue.return_date, Student.query.filter_by(id=book_issue.student_id).first().username, Book.query.filter_by(id=book_issue.book_id).first().title, Librarian.query.filter_by(id=book_issue.librarian_id).first().username, book_issue.id] for book_issue in book_issues]
       
       return render_template("sp_dashboard.html", title="Librarian Dashboard", issued_books = book_issues, form=form, form1=form1, form2=form2)
  else:
       flash("Access Denied! You do not have permission to view this page.", "danger")
       return redirect(url_for("home"))


@app.route("/about-us")
def about_us():
  return render_template("about_us.html", title="About us")

@app.route("/contact")
def contact():
  return render_template("contact.html", title="Contact")


def save_picture(form_picture, role):
   random_hex = secrets.token_hex(8)
   _, ext = os.path.splitext(form_picture.filename)
   picture_fn = random_hex + ext
   picture_path = os.path.join(app.root_path, f'static/profile_pics/{role}', picture_fn)
   
   output_size = (125, 125)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(picture_path)
   
   return picture_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
  image_file = None
  if current_user.role == "student":
        form = UpdateStudentAccount()
        if form.validate_on_submit():
            if form.picture.data:
               picture_file = save_picture(form.picture.data, 'student_pics')
               with app.app_context():
                current_user.image_file = picture_file
                db.session.commit()
            with app.app_context():
              current_user.username = form.username.data
              current_user.email = form.email.data
              db.session.commit()
            flash('Your Account has been updated!', category='success')
            return redirect(url_for('account'))
        elif request.method == "GET":
           form.username.data = current_user.username
           form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/student_pics/' + current_user.image_file)
        return render_template("student_account.html", title="Student Account", image_file=image_file, form=form)
  
  elif current_user.role == "librarian":
        form = UpdateSPAccount()
        if form.validate_on_submit():
            if form.picture.data:
               picture_file = save_picture(form.picture.data, 'admin_pics')
               with app.app_context():
                current_user.image_file = picture_file
                db.session.commit()
            with app.app_context():
              current_user.username = form.username.data
              current_user.email = form.email.data
              current_user.admin_id = form.admin_id.data
              db.session.commit()
            flash('Your Account has been updated!', category='success')
            return redirect(url_for('account'))
        elif request.method == "GET":
           form.username.data = current_user.username
           form.email.data = current_user.email
           form.admin_id.data = current_user.admin_id
        image_file = url_for('static', filename='profile_pics/admin_pics/' + current_user.image_file)
        return render_template("sp_account.html", title="Librarian Account", image_file=image_file, form=form)
  
  else:
        flash(f"Access Denied! You do not have permission to view this page.{current_user.role} acc", "danger")
        return redirect(url_for("home"))
    
@app.route("/section/<int:section_id>/add-book", methods=['GET', 'POST'])
@login_required
def add_book(section_id):
  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role} acc", "danger")
    return redirect(url_for("home"))
  
  form = BookAddForm()
  if form.validate_on_submit():
     if len(Book.query.filter(func.lower(Book.title).ilike(f"%{form.title.data.lower()}%")).all()) > 0:
           flash('Book with that name already exists!', 'danger')
           return redirect(url_for('add_book', section_id=section_id))
     book = Book(title=form.title.data,author=form.author.data,content=form.content.data, lang=form.lang.data, rating=form.rating.data,release_year=form.release_year.data,librarian_id=current_user.id,genre_id=section_id)
     with app.app_context():
        db.session.add(book)
        db.session.commit()
        flash('The Book has been Added Successfully.', 'success')
     
     return redirect(url_for('section', section_id=section_id))
  
  return render_template('add_book.html', title="Add a new Book", form=form, legend='New Book')

@app.route("/section/<int:section_id>/<int:book_id>/update-book", methods=['GET', 'POST'])
@login_required
def update_book(section_id, book_id):
  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role} acc", "danger")
    return redirect(url_for("home"))
  
  book = Book.query.get_or_404(book_id)
  form = BookAddForm()
  if form.validate_on_submit():
        if book.title.lower() != form.title.data.lower() and len(Book.query.filter(func.lower(Book.title).ilike(f"%{form.title.data.lower()}%")).all()) > 0:
           flash('Book with that title already exists!', 'danger')
           return redirect(url_for('update_book', section_id=section_id,book_id=book_id))
        book.title=form.title.data
        book.author=form.author.data
        book.content=form.content.data
        book.lang=form.lang.data
        book.rating=form.rating.data
        book.release_year=form.release_year.data
        db.session.commit()
        flash(f'The Book has been Updated Successfully.', 'success')
    
        return redirect(url_for('section', section_id=section_id))
  elif request.method == 'GET':
    form.title.data = book.title
    form.author.data = book.author
    form.lang.data = book.lang
    form.content.data = book.content
    form.rating.data = book.rating
    form.release_year.data = book.release_year

     
  return render_template('add_book.html', title="Update this Book", form=form, legend='Update Book')

@app.route("/section/<int:section_id>/<int:book_id>/delete", methods=['POST'])
@login_required
def delete_book(section_id, book_id):
  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return redirect(url_for("home"))
  
  with app.app_context():
     book = Book.query.get_or_404(book_id)
     
     feedbacks = FeedBack.query.filter_by(book_id=book_id).all()
     for feedback in feedbacks:
           db.session.delete(feedback)
           db.session.commit()
     
     db.session.delete(book)
     db.session.commit()
     flash('Book Deleted!', 'success')
     return redirect(url_for('section', section_id=section_id))

@app.route("/section/<int:section_id>/<int:book_id>/request_book", methods=['GET', 'POST'])
@login_required
def request_book(section_id, book_id):
   if current_user.role != 'student':
    flash(f"Access Denied! Only Students can request books", "danger")
    return redirect(url_for("home"))
   else:
      form = BookRequestForm()
      if form.validate_on_submit():
        if len(BookIssue.query.filter_by(student_id=current_user.id).all()) == 5:
         flash('You have already borrowed 5 books. Return a Book to request this!', 'danger')
         return redirect(url_for('home'))
        elif len(BookIssue.query.filter_by(student_id=current_user.id,book_id=book_id).all()) > 0:
           flash('You have already borrowed this book!', 'danger')
           return redirect(url_for('home'))
        elif len(BookRequest.query.filter_by(student_id=current_user.id,book_id=book_id).all()) > 0:
           flash('You have already requested this book! Wait for admin approval of previous request.', 'danger')
           return redirect(url_for('home'))
        else:
         request_duration = form.request_duration.data
         student_id = current_user.id
         with app.app_context():
            br = BookRequest(request_duration=request_duration,student_id=student_id, book_id=book_id)
            db.session.add(br)
            db.session.commit()
            flash('Book Requested Successfully!', 'success')
            return redirect(url_for('home'))

      return render_template('request_book.html', title="Request this Book", form=form, legend=f'Request {Genre.query.filter_by(id=section_id).first().name} Book - {Book.query.filter_by(id=book_id).first().title} by {Book.query.filter_by(id=book_id).first().author}')
   
@app.route('/student-requests')
@login_required
def student_requests():
   if current_user.role == 'librarian':
      flash(f"Access Denied! Only Students view requested books", "danger")
      return redirect(url_for("home"))
   else:
      requested_books = BookRequest.query.filter_by(student_id=current_user.id).all()
      details = [[Book.query.filter_by(id=x.book_id).first().title, BookRequest.query.filter_by(id=x.id).first().request_duration] for x in requested_books]
   return render_template('student_requests.html', requested_books=details, title='Requests')

@app.route('/pending-requests')
@login_required
def pending_requests():
   if current_user.role != 'librarian':
      flash(f"Access Denied! Only Librarian can view this page", "danger")
      return redirect(url_for("home"))
   else:
      pending_requests = BookRequest.query.all()
      details = [[x.id, Book.query.filter_by(id=x.book_id).first().title, Student.query.filter_by(id=x.student_id).first().username, x.request_duration] for x in pending_requests]
   return render_template('pending_requests.html', requests=details, title="Pending Requests")
   
  

def duration_to_timedelta(st):
    s = 0
    pattern = re.compile(r'(\d+)\s*([a-zA-Z]+)')
    matches = pattern.findall(st)
    result = [[int(match[0]), match[1]] for match in matches]
    for i, j in result:
       if j == 'minutes' or j == 'minute':
          s += (i * 60)
       elif j == 'hours' or j == 'hour':
          s += (i * 60 * 60)
       elif j == 'days' or j == 'day':
          s += (i * 60 * 60 * 24)
       elif j == 'weeks' or j == 'week':
          s += (i * 60 * 60 * 24 * 7)
    return timedelta(seconds=s)

@app.route("/pending-requests/<int:request_id>/issue", methods=['POST'])
@login_required
def issue_book(request_id):
  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return redirect(url_for("home"))
  
  with app.app_context():
     book_request = BookRequest.query.get_or_404(request_id)
     issue_date = datetime.now()
     return_date = issue_date + duration_to_timedelta(book_request.request_duration)
     student_id = book_request.student_id
     book_id = book_request.book_id
     librarian_id = current_user.id

     bi = BookIssue(issue_date=issue_date,return_date=return_date,student_id=student_id,book_id=book_id,librarian_id=librarian_id)
     db.session.add(bi)
     db.session.commit()

     db.session.delete(book_request)
     db.session.commit()
     flash('Book Issued to Student!', 'success')
  return redirect(url_for('pending_requests'))

@app.route("/pending-requests/<int:request_id>/disapprove", methods=['POST'])
@login_required
def disapprove_request(request_id):
  if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return redirect(url_for("home"))
  
  with app.app_context():
     book_request = BookRequest.query.get_or_404(request_id)
     db.session.delete(book_request)
     db.session.commit()
     flash('Book Request disapproved to Student!', 'danger')
  return redirect(url_for('pending_requests'))

@app.route("/student-issued")
@login_required
def student_issued():
  if current_user.role == "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return redirect(url_for("home"))
  else:
     books = BookIssue.query.filter_by(student_id=current_user.id).all()
     books = [Book.query.filter_by(id=book.book_id).all()+[book.return_date, Genre.query.filter_by(id=Book.query.filter_by(id=book.book_id).first().genre_id).first().name, book.id] for book in books]
  return render_template('student_issued_books.html', issued_books=books, title='Issued books')


@app.route("/revoke-access/<int:issue_id>", methods=['POST'])
@login_required
def revoke_access(issue_id):
   if current_user.role != "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return redirect(url_for("home"))
   else:
      with app.app_context():
         book_issue = BookIssue.query.filter_by(id=issue_id).first()
         db.session.delete(book_issue)
         db.session.commit()
      flash(f"Access revoked", "danger")   
      return redirect(url_for('sp_dash'))
   
@app.route("/return-book/<int:issue_id>", methods=['POST'])
@login_required
def return_book(issue_id):
   if current_user.role == "librarian":
    flash(f"Access Denied! You do not have permission to view this page.{current_user.role}", "danger")
    return redirect(url_for("home"))
   else:
      with app.app_context():
         book_issue = BookIssue.query.filter_by(id=issue_id).first()
         bid = book_issue.book_id
         sid = book_issue.student_id
         db.session.delete(book_issue)
         db.session.commit()
      return redirect(url_for('book_feedback', book_id=bid, student_id=sid))
   

@app.route('/book-feedback/<int:book_id>/<int:student_id>', methods=['GET', 'POST'])
@login_required
def book_feedback(book_id, student_id):
   if current_user.role == "librarian" or current_user.id != student_id:
    flash("Access Denied! You do not have permission to view this page.", "danger")
    return redirect(url_for("home"))
   else:
      bname = Book.query.filter_by(id=book_id).first().title
      sname = Student.query.filter_by(id=student_id).first().username

      form = FeedBackForm()
      if form.validate_on_submit():
        feedback = form.feedback.data
        if len(feedback) >= 200:
           flash("Limit your feedback to less than or equal to 200 words.", "danger")
           return redirect(url_for('book_feedback', book_id=book_id, student_id=student_id))
        with app.app_context():
            f = FeedBack(feedback=feedback,student_id=student_id, book_id=book_id)
            db.session.add(f)
            db.session.commit()
            flash('Feedback Submitted Successfully!', 'success')
            return redirect(url_for('home'))

      return render_template('feedback.html', book_name=bname, student_name=sname, legend='Feedback Form', form=form, title="Book Feedback")
   
@app.route("/feedbacks")
def feedbacks():
    feed_backs = FeedBack.query.all()
    f = [{'book_title': Book.query.filter_by(id=i.book_id).first().title,
          'student_username': Student.query.filter_by(id=i.student_id).first().username,
          'feedback': i.feedback} for i in feed_backs]
    return jsonify(f)


@app.route("/download/<int:book_id>")   
@login_required
def download_book(book_id):
   if current_user.role == "librarian" or len(BookIssue.query.filter_by(book_id=book_id,student_id=current_user.id).all()) <= 0:
    flash("Access Denied! You do not have permission to view this page.", "danger")
    return redirect(url_for("home"))
   else:
      lang_dict = {'hindi': 'Noto Sans Devanagari', 'tamil': 'Noto Serif Tamil', 'telugu': 'Noto Sans Telugu', 'malayalam': 'Noto Sans Malayalam', 'kannada': 'Noto Sans Kannada', 'english':''}
      book=Book.query.filter_by(id=book_id).first()
      lang = book.lang.lower()

      if lang not in lang_dict.keys():
         flash(f'Cannot download {lang} language book!', 'danger')
         return redirect(url_for("home"))
      
      rendered = render_template('download_content.html', book=book, font_lang=lang_dict[lang])
      
      config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
      pdf = pdfkit.from_string(rendered, configuration=config)

      response = make_response(pdf)
      response.headers['Content-Type'] = 'application/pdf'
      response.headers['Content-Disposition'] = 'inline;filename=output.pdf'

      return response
   

def save_graph(filename, role):
   _, ext = os.path.splitext(filename)
   picture_fn = f"{role}_available" + ext
   picture_path = os.path.join(app.root_path, f'static/graphs', picture_fn)
   
   i = Image.open(filename)
   i.save(picture_path)
   
   return picture_fn

@app.route("/student-graphs")
@login_required
def student_graphs():
   if current_user.role == 'librarian':
      flash("Access Denied! You do not have permission to view this page.", "danger")
      return redirect(url_for("home"))
   issued_books = BookIssue.query.filter_by(student_id=current_user.id).all()
   values = [k.name for i in issued_books for j in Book.query.filter_by(id=i.book_id).all() for k in Genre.query.filter_by(id=j.genre_id).all()]
   value_counts = {}
   for value in values:
      value_counts[value] = value_counts.get(value, 0) + 1

   # Pie chart
   plt.figure(figsize=(8, 8))
   plt.pie(value_counts.values(), labels=value_counts.keys(), autopct='%1.1f%%', startangle=140)
   plt.axis('equal')
   plt.title('Distribution of Genres in Issued Books')
   picture_path = os.path.join(app.root_path, f'static/graphs/one.png')
   plt.savefig(picture_path)
   plt.close()

   image = save_graph(picture_path, 'student')
   image_url = url_for('static', filename='graphs/' + image)

   genres = [i.name for i in Genre.query.all()]
   value_counts = {}
   for value in genres:
      value_counts[value] = value_counts.get(value, 0) + 1

   # Pie chart
   plt.figure(figsize=(8, 8))
   plt.pie(value_counts.values(), labels=value_counts.keys(), autopct='%1.1f%%', startangle=140)
   plt.axis('equal')
   plt.title('Distribution of Genres Available')
   picture_path = os.path.join(app.root_path, f'static/graphs/two.png')
   plt.savefig(picture_path)
   plt.close()

   image1 = save_graph(picture_path, 'all')
   image_url1 = url_for('static', filename='graphs/' + image1)

   return render_template('graph.html', image=image_url, image1=image_url1, title="Graph")


@app.route("/sp-graphs")
@login_required
def sp_graphs():
   if current_user.role != 'librarian':
      flash("Access Denied! You do not have permission to view this page.", "danger")
      return redirect(url_for("home"))
   issued_books = BookIssue.query.all()
   values = [k.name for i in issued_books for j in Book.query.filter_by(id=i.book_id).all() for k in Genre.query.filter_by(id=j.genre_id).all()]
   value_counts = {}
   for value in values:
      value_counts[value] = value_counts.get(value, 0) + 1

   # Pie chart
   plt.figure(figsize=(8, 8))
   plt.pie(value_counts.values(), labels=value_counts.keys(), autopct='%1.1f%%', startangle=140)
   plt.axis('equal')
   plt.title('Distribution of Genres in Issued Books')
   picture_path = os.path.join(app.root_path, f'static/graphs/three.png')
   plt.savefig(picture_path)
   plt.close()

   image = save_graph(picture_path, 'librarian')
   image_url = url_for('static', filename='graphs/' + image)

   genres = [i.name for i in Genre.query.all()]
   value_counts = {}
   for value in genres:
      value_counts[value] = value_counts.get(value, 0) + 1

   # Pie chart
   plt.figure(figsize=(8, 8))
   plt.pie(value_counts.values(), labels=value_counts.keys(), autopct='%1.1f%%', startangle=140)
   plt.axis('equal')
   plt.title('Distribution of Genres Available')
   picture_path = os.path.join(app.root_path, f'static/graphs/four.png')
   plt.savefig(picture_path)
   plt.close()

   image1 = save_graph(picture_path, 'all')
   image_url1 = url_for('static', filename='graphs/' + image1)

   return render_template('graph.html', image=image_url, image1=image_url1, title="Graph")





# API Endpoints

# get books
@app.route("/api/books", methods=['GET'])
def api_get_books():
   books = Book.query.all()
   books = [{
   'id' : book.id,
   'author' : book.author,
   'lang' : book.lang,
   'content' : book.content,
   'librarian_id' : book.librarian_id,
   'genre_id' : book.genre_id} for book in books]
   return jsonify(books)

# post books
@app.route("/api/books/add", methods=['DELETE'])
@token_required
def api_add_book(user_from_token):
   data = request.json
   if user_from_token.role != 'librarian':
      return ({'message': 'Invalid credentials'}), 401
   
   else:
      if len(Book.query.filter_by(title=data['title']).all()) > 0:
         return ({'message': 'Book already exists'}), 401
      year = datetime.strptime(data['release_year'], "%Y")
      book = Book(title=data['title'],author=data['author'],content=data['content'], lang=data['lang'], rating=data['rating'],release_year=year,librarian_id=user_from_token.id,genre_id=data['genre_id'])
      with app.app_context():
         db.session.add(book)
         db.session.commit()
      return jsonify({"message": "Successfully added the book"}), 200


#put books
@app.route("/api/books/update", methods=["PUT"])
@token_required
def api_update_book(user_from_token):
    if user_from_token.role != "librarian":
      return ({'message': 'Invalid credentials'}), 401
  
    data = request.json
    title = data['title']
    id = Book.query.filter_by(title=title).first().id
    book = Book.query.get_or_404(id)
    if 'author' in data: book.author=data['author']
    if 'content' in data: book.content=data['content']
    if 'lang' in data: book.lang=data['lang']
    if 'rating' in data: book.rating=data['rating']
    if 'release_year' in data: book.release_year=data['release_year']
    db.session.commit()
    
    return jsonify({"message": "Successfully updated the book"}), 200



#delete books
@app.route("/api/books/delete", methods=['POST'])
@token_required
def api_delete_book(user_from_token):
   data = request.json
   if user_from_token.role != 'librarian':
      return ({'message': 'Invalid credentials'}), 401
   
   else:
      if len(Book.query.filter_by(title=data['title']).all()) < 0:
         return ({'message': 'Book does not exist'}), 401
      id = Book.query.filter_by(title=data['title']).first().id
      with app.app_context():
         book = Book.query.get_or_404(id)
         
         feedbacks = FeedBack.query.filter_by(book_id=id).all()
         for feedback in feedbacks:
               db.session.delete(feedback)
               db.session.commit()
         
         db.session.delete(book)
         db.session.commit()
      return jsonify({"message": "Successfully deleted the book"}), 200

# student login api
@app.route("/api/login", methods=['POST'])
def api_login():
  auth = request.json

  if auth and 'email' in auth and 'password' in auth and 'role' in auth:
     email = auth['email']
     password = auth['password']

     student = Student.query.filter_by(email=email).first()
     if(bcrypt.check_password_hash(student.password, password)):
            token = jwt.encode({'email': email, 'role': 'student'}, app.config['SECRET_KEY'])
            return jsonify({'token': token}), 200
 
  return jsonify({'message': 'Invalid credentials'}), 401


# librarian login api
@app.route("/api/sp-login", methods=['POST'])
def api_login_librarian():
  auth = request.json

  if auth and 'email' in auth and 'password' in auth:
     email = auth['email']
     password = auth['password']

     librarian = Librarian.query.filter_by(email=email).first()
     if(bcrypt.check_password_hash(librarian.password, password)):
            token = jwt.encode({'email': email, 'role': 'librarian'}, app.config['SECRET_KEY'])
            return jsonify({'token': token}), 200
 
  return jsonify({'message': 'Invalid credentials'}), 401


#get student books
@app.route("/api/student-books", methods=["GET"])
@token_required
def api_student_books(user_from_token):
   book_issues = BookIssue.query.filter_by(student_id=user_from_token.id).all()
   books = [Book.query.filter_by(id=book_issue.book_id).first() for book_issue in book_issues]
   books = [{
   'id' : book.id,
   'author' : book.author,
   'lang' : book.lang,
   'content' : book.content,
   'librarian_id' : book.librarian_id,
   'genre_id' : book.genre_id} for book in books]
   return jsonify(books)
   


@app.route("/api/search_section", methods=['POST'])
@login_required
def search_section_api():
    data = request.json
    section = data.get('section')
    if section:
        return jsonify({'success': True, 'query': section})
    return jsonify({'success': False, 'message': 'Section is required'}), 400

@app.route("/api/search_title", methods=['POST'])
@login_required
def search_title_api():
    data = request.json
    title = data.get('title')
    if title:
        return jsonify({'success': True, 'query': title})
    return jsonify({'success': False, 'message': 'Title is required'}), 400

