import MySQLdb
import jinja2
from flask import Flask, session, request, make_response, redirect, url_for, g
from flask import render_template
from werkzeug import secure_filename
import os
import shutil
import json


# allow jinja to use break and continue statement for loops
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


# define static, template and book upload folder path
app = Flask(__name__, static_folder="files", template_folder="app")
app.config['UPLOAD_FOLDER'] = "files/books/"
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


# connect mysql with default configuration
def connect():
	mysql_config = {
		"host": "localhost",
		"port": 8001,
		"user": "root",
		"passwd": "matrix",
		"db": "library"
	}
	g.conn = MySQLdb.connect(**mysql_config)
	g.cursor = g.conn.cursor()
	return g.cursor


# check for login credentials
def do_login(login_id, password):
	query = "select * from `tabProfile`"
	profiles = run_query(query)
	for user_details in profiles:
		if user_details["login_id"] == login_id and user_details["password"] == password and \
			user_details["enabled"] == 1:
				return {'username': user_details["first_name"] + " " + user_details["last_name"], 
					'role': profiles[0]["role"]}
	return False


# run sql query
def run_query(query, query_type="fetch"):
	connect()
	result = ""
	conn = g.conn
	cursor = g.cursor
	cursor.execute(query)

	if query_type == "fetch":
		# zip columns and rows 
		result = []
		columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
		for row in cursor:
			result.append(dict(zip(columns, row)))
	else:
		conn.commit()

	cursor.close()
	conn.close()
	return result


# get all favorite books
def get_favorites(user):
	query = """select user.book, book.book_name from `tab%s` user, `tabBook` book where 
		book.id=user.book and user.favorite='Yes'""" % (user)
	favorites = run_query(query)

	return favorites


# generate html code for book panels
def get_book_panels(book_details):
	# get no. of panels to be shown in book shelf
	no_of_panels = (len(book_details) / 16) + 1
	counter = 0

	for panel in range(no_of_panels):
		panels = """<div class='panel_slider' id='panel_slider'>
			<div id='panel_items' class='panel_items'>
				<div class='slide_animate'>"""

		for product_box in range(2):
			if counter < len(book_details):
				panels += """<div class='products_box'>"""

				for book in range(8):
					if counter < len(book_details):
						panels += """<div class='product'>
								<input type='checkbox' name='book' data-name='book' data-id='""" + book_details[counter]["book"] + """'>
								<a href='/epub_reader/""" + book_details[counter]["book"] + """' target='_blank'>
									<img src='""" + book_details[counter]["book_cover_path"] + """'>
								</a>
							</div>"""
						counter += 1

				panels += """</div>"""

		panels += """</div>
				</div>
			</div>"""

	return panels


# generate new id for new records
def generate_new_id(module):
	query = """select id from `tab%s`""" % (module)
	ids = run_query(query)
	
	new_id = 0
	if ids and module != "Profile":
		for record_id in ids:
			existing_id = int(record_id["id"].split("-")[1])
			if existing_id > new_id:
				new_id = existing_id

	new_id = module.upper() + "-" + str(new_id + 1)
	return new_id


# checks whether the given id exists in database or not
def check_existing_id(record_id, module):
	if not module:
		module = record_id.split("-")[0]

	query = """select id from `tab%s` where id='%s'""" % (module, record_id)
	result = run_query(query)

	if result:
		return result[0]["id"]

	return result


# ------------------------------------------------------------------------------------------------------------
# Action bar commands


# refresh the current list view
@app.route('/refresh')
def refresh():
	query = """select id from `tab%s`""" % (request.args.get("module"))
	result = run_query(query)

	return json.dumps(result)


# delete all the selected records
@app.route('/delete', methods=["GET", "POST"])
def delete():
	if request.method == "POST":
		module = request.form.get("module")
		ids = eval(request.form.get("ids"))

		# delete each book record from tabBook and table of owner and also delete the files
		for record_id in ids:
			if module == "Book":
				book_owner = run_query("""select owner from `tabBook` where id='%s'""" % (record_id))[0]["owner"]
				run_query("""delete from `tabBook` where id='%s'""" %(record_id), "insert")
				run_query("""delete from `tab%s` where book='%s'""" %(book_owner, record_id), "insert")
				shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], book_owner, record_id))
			else:
				run_query("""delete from `tab%s` where id='%s'""" % (module, record_id), "insert")

		return json.dumps("Ok")


@app.route('/share', methods=["GET", "POST"])
def share():
	if request.method == "POST":
		user_login_id = request.cookies.get("login_id")

		users = eval(request.form.get("users"))
		books = eval(request.form.get("books"))

		# share selected book with selected user
		for user in users:
			for book in books:
				# get book path and book cover path
				query = """select book, book_path, book_cover_path, format from `tab%s` where book='%s'""" % (user_login_id, 
					book)
				book_details = run_query(query)

				book_id = book_details[0]["book"]
				book_path = book_details[0]["book_path"]
				book_cover_path = book_details[0]["book_cover_path"]
				format = book_details[0]["format"]

				query = """insert into `tab%s`(book, favorite, rating, book_path, book_cover_path, 
					format, shared) values('%s', '%s', %s, '%s', '%s', '%s', '%s')""" %(book_id, "No", 
					0, book_path, book_cover_path, format, "Yes")

				run_query(query, "insert")

		return json.dumps("Ok")


# ------------------------------------------------------------------------------------------------------------

# show index or home page
@app.route('/')
def index():
	if "user" in session:
		return redirect(url_for('open_app'))
	return render_template("index.html")


# registration section
@app.route('/registration', methods=['GET', 'POST'])
def registration():
	if request.method == "POST":
		first_name = request.form.get("first_name")
		last_name = request.form.get("last_name")
		login_id = request.form.get("login_id")
		password = request.form.get("password")
		dob = request.form.get("dob")
		role = "User"
		enabled = 1

		# insert new user into profiles record
		query = """insert into `tabProfile`(id, first_name, last_name, login_id, password, 
			role, date_of_birth, enabled) values("%s", "%s", "%s", "%s", "%s", "%s", %s, 
			%s)""" % (login_id, first_name, last_name, login_id, password, role, dob, enabled)

		run_query(query, "insert")

		# create folder for books storage for particular user
		user_files_path = os.path.join(app.config['UPLOAD_FOLDER'], login_id)
		if not os.path.exists(user_files_path):
			os.makedirs(user_files_path)

		# create new table for individual user
		query = """create table `tab%s`(`book` varchar(20), `favorite` varchar(20), `rating` int, 
			`book_path` varchar(100), `book_cover_path` varchar(100), `format` varchar(10), 
			`shared` varchar(5))""" % (login_id)

		run_query(query, "insert")
		return redirect(url_for('login'))

	return render_template("registration/registration.html")


# book section
@app.route('/book')
def show_books():
	query = """select id from `tabBook`"""
	books = run_query(query)
	user_login_id = request.cookies.get("login_id")

	resp = make_response(render_template('misc/list_view.html', user=request.cookies.get("username"), 
		login_id=user_login_id, favorites=get_favorites(user_login_id), records=books, module="book", 
		module_title="Book"))
	resp.set_cookie("current_module", "Book")
	return resp


@app.route('/book/<filename>', methods=["GET", "POST"])
def book(filename):
	user_login_id = request.cookies.get("login_id")

	if request.method == "POST":
		book_name = request.form.get("book_name")
		publisher = request.form.get("publisher")
		edition = request.form.get("edition")
		author = request.form.get("author")
		book_id = request.form.get("id") or generate_new_id("Book")
		rate = request.form.get("rate")
		favorite = request.form.get("favorite")
		more_details = request.form.get("more_details")
		book = request.files["ebook"]
		book_cover = request.files["book_cover_photo"]

		exists = check_existing_id(book_id, "Book")

		# save book in book table
		if exists:
			query = """update `tabBook` set book_name='%s', publisher='%s', author='%s', edition='%s', 
				rate='%s', more_details='%s' where id='%s'""" % (book_name, publisher, author, 
				edition, rate, more_details, book_id)
		else:
			query = """insert into `tabBook` values('%s', '%s', '%s', '%s', %s, '%s', '%s', '%s')""" % (book_id, 
				book_name, author, publisher, rate or 0, edition, more_details, user_login_id)

		run_query(query, "insert")

		# save ebook and its cover photo to user's directory
		upload_path = os.path.join(app.config['UPLOAD_FOLDER'], user_login_id, book_id)

		if book_cover:
			book_cover_photo = secure_filename(book_cover.filename)
			upload_path = os.path.join(upload_path)
			file_format = os.path.splitext(book_cover_photo)[1][1:]

			if not os.path.exists(upload_path):
				os.makedirs(upload_path)

			book_cover_path = os.path.join(upload_path, book_cover_photo)
			book_cover.save(book_cover_path)

		if book:
			ebook = secure_filename(book.filename)
			file_format = os.path.splitext(ebook)[1][1:]

			if not os.path.exists(upload_path):
				os.makedirs(upload_path)

			book_path = os.path.join(upload_path, ebook)
			book.save(book_path)

		# save book to user's table in database
		query = """insert into `tab%s` values("%s", "%s", 0, "%s", "%s", "%s", "No")""" % (user_login_id, book_id, 
			favorite, book_path, book_cover_path, file_format)

		run_query(query, "insert")

		return redirect(url_for("show_books"))
	else:
		if check_existing_id(filename, "Book"):
			query = """select * from `tabBook` where id='%s'""" % (filename)
			book_details = run_query(query)[0]
		else:
			book_details = {"id": generate_new_id("Book")}

		return render_template('book/book.html', user=request.cookies.get("username"), 
			login_id=user_login_id, book=book_details)


# returns the book path for downloading
@app.route('/get_book_path')
def get_book_path():
	query = """select book_path from `tab%s` where book='%s'""" % (request.cookies.get("login_id"), request.args.get("book_id"))
	book_details = run_query(query)[0]

	return json.dumps(book_details["book_path"])


# returns list of all users for purpose of sharing
@app.route('/get_users')
def get_users():
	query = """select id from `tabProfile` where id!='%s'""" % (request.cookies.get("login_id"))
	profile_list = run_query(query)

	return json.dumps(profile_list)

# book shelf section
@app.route('/book_shelf')
def book_shelf():
	user_login_id = request.cookies.get("login_id")
	query = """select * from `tab%s`""" % user_login_id
	book_details = run_query(query)

	return render_template('book_shelf/book_shelf.html', user=request.cookies.get("username"), 
		login_id=user_login_id, favorites=get_favorites(user_login_id), panels=get_book_panels(book_details))


# epub reader section
@app.route('/epub_reader/<filename>')
def read_epub(filename):
	query = """select book.book_name, book.author, user.book_path from `tabBook` book, 
		`tab%s` user where book.id=user.book and book.id='%s'""" % (request.cookies.get("login_id"), filename)
	book_details = run_query(query)[0]

	return render_template('misc/epub_reader.html', book_details=book_details)


# profile section
@app.route('/profile')
def show_profiles():
	query = """select id from `tabProfile`"""
	profiles = run_query(query)
	user_login_id = request.cookies.get("login_id")

	resp = make_response(render_template('misc/list_view.html', user=request.cookies.get("username"), 
		login_id=user_login_id, favorites=get_favorites(user_login_id), records=profiles, 
		module="profile", module_title="Profile"))
	resp.set_cookie("current_module", "Profile")
	return resp

@app.route('/profile/<filename>', methods=["GET", "POST"])
def profile(filename):
	user_login_id = request.cookies.get("login_id")

	if request.method == "POST":
		enabled = 1 if request.form.get("enabled") else 0
		first_name = request.form.get("first_name")
		last_name = request.form.get("last_name")
		user = request.form.get("login_id")
		password = request.form.get("password")
		role = request.form.get("role")

		exists = check_existing_id(user, "Profile")

		if exists:
			query = """update `tabProfile` set enabled=%s, first_name='%s', last_name='%s', 
				password='%s' where login_id='%s'""" % (enabled, first_name, last_name, password, user)
		else:
			query = """insert into `tabProfile` values('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)""" % (user, 
				first_name, last_name, user, password, role, '0000-00-00 00:00:00', enabled)

		run_query(query, "insert")

		# if user folder doesnt exist, create it
		user_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], user)
		if not os.path.exists(user_folder_path):
			os.makedirs(user_folder_path)

		# create user table if does not exist
		query = """show tables like 'tab%s'""" % (user)
		table = run_query(query)
		if not table:
			query = """create table `tab%s`(`book` varchar(20), `favorite` varchar(20), `rating` int, 
				`book_path` varchar(100), `book_cover_path` varchar(100), `format` varchar(10), 
				`shared` varchar(5))""" % (login_id)

			run_query(query, "insert")

		return redirect(url_for("show_profiles"))
	else:
		if check_existing_id(filename, "Profile"):
			query = """select * from `tabProfile` where id='%s'""" % (filename)
			profile_details = run_query(query)[0]
			profile_details["record"] = "existing"
		else:
			profile_details = {"id": generate_new_id("Profile"), "record": "new"}

		return render_template('profile/profile.html', user=request.cookies.get("username"), 
			login_id=user_login_id, favorites=get_favorites(user_login_id), profile=profile_details)


# issue section
@app.route('/issue')
def show_issues():
	query = """select * from `tabIssue`"""
	issues = run_query(query)
	user_login_id = request.cookies.get("login_id")

	resp = make_response(render_template('misc/list_view.html', user=request.cookies.get("username"), 
		login_id=user_login_id, favorites=get_favorites(user_login_id), 
		records=issues, module="issue", module_title="Issue"))
	resp.set_cookie("current_module", "Issue")
	return resp

@app.route('/issue/<filename>', methods=["GET", "POST"])
def issue(filename):
	user_login_id = request.cookies.get("login_id")

	if request.method == "POST":
		issue_id = request.form.get("id")
		subject = request.form.get("subject")
		description = request.form.get("description")

		exists = check_existing_id(issue_id, "Issue")

		if exists:
			query = """update `tabIssue` set subject='%s', description='%s' where id='%s'""" % (subject, description, issue_id)
		else:
			query = """insert into `tabIssue` values('%s', '%s', '%s')""" % (issue_id, subject, description)

		run_query(query, "insert")
		return redirect(url_for("show_issues"))
	else:
		if check_existing_id(filename, "Issue"):
			query = """select * from `tabIssue` where id='%s'""" % (filename)
			issue_details = run_query(query)[0]
		else:
			issue_details = {"id": generate_new_id("Issue")}

		return render_template('issue/issue.html', user=request.cookies.get("username"), 
			login_id=user_login_id, favorites=get_favorites(user_login_id), issue=issue_details)

@app.route('/shout', methods=["GET", "POST"])
def report_issue():
	user_login_id = request.cookies.get("login_id")

	if request.method == "POST":
		issue_id = generate_new_id("Issue")
		subject = request.form.get("subject")
		description = request.form.get("description")

		query = """insert into `tabIssue` values('%s', '%s', '%s')""" % (issue_id, subject, description)
		run_query(query, "insert")

		return redirect(url_for("open_app"))


# search section
@app.route('/search')
def search():
	user_login_id = request.cookies.get("login_id")
	return render_template('search/search.html', user=request.cookies.get("username"), 
		favorites=get_favorites(user_login_id), login_id=user_login_id)


@app.route('/search_books')
def search_books():
	# build condition for searching the text
	condition = ""

	if request.args.get("by_name") == "true":
		condition += ", book_name"
	if request.args.get("by_author") == "true":
		condition += ", author"
	if request.args.get("by_publisher") == "true":
		condition += ", publisher"

	# return books according to the searching criteria
	query = """select * from `tabBook` where CONCAT(id%s) like '%%%s%%'""" % (condition, 
		request.args.get("search_text"))

	books = run_query(query)
	return json.dumps(books)


@app.route('/search_book_name')
def search_book_name():
	query = """select * from `tab%s` user, `tabBook` book where 
		book.id=user.book and book.book_name like '%%%s%%'""" % (request.cookies.get("login_id"), 
		request.args.get("search_text"))

	books = run_query(query)
	book_panels = get_book_panels(books)
	return json.dumps(book_panels)


# refresh section
@app.route('/refresh_books')
def refresh_books():
	query = """select * from `tab%s`""" % (request.cookies.get("login_id"))

	books = run_query(query)
	book_panels = get_book_panels(books)
	return json.dumps(book_panels)

# login section
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		login_id = request.form.get("login_id")
		password = request.form.get("password")
		if (not login_id) or (not password):
			return "Please enter Login ID / Password"
		else:
			user = do_login(login_id, password)
			if user:
				session["user"] = login_id
				session["username"] = user["username"]
				return redirect(url_for('open_app'))
			else:
				return "Invalid Login ID / Password"

	return render_template('login.html')


# set sessions, cookies and then show app
@app.route('/app')
def open_app():
	user_full_name = session["username"]
	user_login_id = session["user"]

	query = """select role from `tabProfile` where login_id='%s'""" % user_login_id
	role = run_query(query)[0]["role"]

	# depends on user role change the app home page for them
	if role == "User":
		resp = make_response(redirect('/book_shelf'))
	elif role == "Administrator":
		resp = make_response(render_template('app.html', user=user_full_name, 
			favorites=get_favorites(user_login_id), login_id=user_login_id))

	# save user defaults to cookies
	resp.set_cookie("username", user_full_name)
	resp.set_cookie("login_id", user_login_id)
	resp.set_cookie("role", role)
	resp.set_cookie("current_module", "App")
	return resp


# destroys user session and logout
@app.route('/logout')
def logout():
	# remove all sessions and cookies related to that user
	session.pop('user', None)
	resp = make_response(render_template('index.html'))

	resp.set_cookie("username", "", expires=0)
	resp.set_cookie("login_id", "", expires=0)
	resp.set_cookie("role", "", expires=0)
	resp.set_cookie("current_module", "", expires=0)
	return resp


# permanently delete the user profile with its data 
@app.route('/deactivate')
def deactivate():
	user_login_id = request.cookies.get("login_id")

	# remove user from profile table
	query = """delete from `tabProfile` where login_id='%s'"""  % (user_login_id)
	run_query(query, "insert")

	# delete user table
	query = """drop table `tab%s`""" % (user_login_id)
	run_query(query, "insert")

	# delete user books from book table
	query = """delete from `tabBook` where owner='%s'""" % (user_login_id)
	run_query(query, "insert")

	# delete user ebooks
	shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], user_login_id))

	return redirect(url_for('logout'))

# mysql connection establishment with every incoming request
@app.before_request
def connect_mysql():
	connect()

# @app.errorhandler(404)
# def not_found(error):
# 	return "Error 404 - File not found"

app.secret_key = "library"

if __name__ == "__main__":
	app.run(debug=True, port=8001)