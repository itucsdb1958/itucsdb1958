Developer Guide
===============

* :ref:`Database design`
* :ref:`Setting environment`
* :ref:`Database setup`
* :ref:`Running SQL`
* :ref:`Adding Functionalities`
* :ref:`Login process`
* :ref:`Logout process`
* :ref:`File and image upload`
* :ref:`Error pages`

.. _Database design:

Database Design
***********************

DIAGRAMLAR BURAYA GELECEK

.. _Setting environment:

Setting up the environment for development
***********************************************

Clone the repository from github and install requirements as follows,

.. code-block:: console

	$ git clone https://github.com/itucsdb1958/itucsdb1958.git
	$ cd itucsdb1958
	$ pip install -r requirements.txt

After the installation, you can simply call the following command to run the server.

.. code-block:: console

	$ python server.py

.. _Database setup:

Database setup for local development
**************************************

The project uses Postgresql database. Therefore, to do local development, you should have postgresql installed in your system. 

By default, the project is meant to be used with a PostgreSQL server.
You can use a local installation or a hosted service like
`ElephantSQL <https://www.elephantsql.com/>`_ (they have a free plan),
but we recommend that you use `Docker <https://www.docker.com/>`_::

  $ docker pull postgres

In order to make changes to your database persistent, you have to set up
a folder that will be shared between your regular operating system and
the Docker container. Create the folder, e.g.::

  $ mkdir -p $HOME/docker/volumes/postgres

The command for running the container is::

  $ docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres

This will start a PostgreSQL server that runs on the host ``localhost``,
on port 5432. The username is ``postgres``, the password is ``docker``,
and the database name is ``postgres``. You can use the following command
to connect to it::

  $ psql -h localhost -U postgres -d postgres


If you successfuly complete the steps above, you are ready for development.

Database initialization
*****************************

Since the website is deployed on HEROKU, the database connection has to be set up appropriately.
When *server.py* runs on HEROKU, the database needs to be initialized by calling *db_init.py*. The code block in db_init.py does just that.

.. code-block:: python

	def initialize(url):
	    with dbapi2.connect(url) as connection:
		cursor = connection.cursor()
		for statement in INIT_STATEMENTS:
		    cursor.execute(statement)
		cursor.close()


	if __name__ == "__main__":
	    url = os.getenv("DATABASE_URL")
	    if url is None:
		print("Usage: DATABASE_URL=url python dbinit.py")  # , file=sys.stderr)
		sys.exit(1)
	    initialize(url)

Init statements must be filled with table initialization queries such as:

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS TABLE1 (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    	)

For multiple tables, add comma seperated SQL statements with triple quotation marks as follows:

.. code-block:: python

	INIT_STATEMENTS = [

	    """CREATE TABLE IF NOT EXISTS TABLE1 (
		ID SERIAL PRIMARY KEY,
		NAME VARCHAR NOT NULL,
	    )
	    """,
	    """CREATE TABLE IF NOT EXISTS TABLE2(
		ID SERIAL PRIMARY KEY,
		NAME VARCHAR NOT NULL,
	    )
	    """
	]

.. note:: The table initialization is serial. Take care of the references you make, since if the table is referenced before its creation, there will be an error.


.. warning:: Always switch from RELEASE mode to LOCAL mode by setting the boolean RELEASE in server.py line:26 FALSE. The code block below will set up the database for your local database if it is false, and for HEROKU if it is true.

.. code-block:: python

	RELEASE = False

	if(not RELEASE):
	    os.environ['DATABASE_URL'] = "postgres://postgres:docker@localhost:5432/postgres"
	    initialize(os.environ.get('DATABASE_URL'))

.. _Running SQL:

Running SQL statements
*****************************

In order to run an SQL statement, since we cannot use ORM libraries, a boilerplate code has been written in order to save time and effort from developers. You can simply import "*queries.py*" and use the common SQL statements. These codes can be found in *queries.py* script as follows:

.. code-block:: python

	def insert(table,columns,values):
	    query = """insert into {} ({}) values({})""".format(table,columns,values)
	    run(query)

	def select(columns, table, where=None):
	    if (where != None):
		query = """select {} from {} where {}""".format(columns, table, where)
	    else:
		query = """select {} from {}""".format(columns, table)
	    return run(query)


	def update(table, columns, where):
	    query = """update {} set {} where {}""".format(table, columns, where)
	    run(query)


	def delete(table, where):
	    query = """delete from {} where {}""".format(table, where)
	    run(query)

.. code-block:: python

	def run(query):
	    connection = None
	    cursor = None
	    result = None
	    print(query)
	    try:
		connection = db.connect(os.getenv("DATABASE_URL"))
		cursor = connection.cursor()
		cursor.execute(query)
		if(not 'drop' in query and not 'update' in query and not 'delete' in query and not 'insert' in query):
		    result = cursor.fetchall()
	    except db.DatabaseError as dberror:
		if connection != None:
		    connection.rollback()
		result = dberror
		print("Error",result)
		flash(result.message, 'danger')
	    finally:
		if connection != None:
		    connection.commit()
		    connection.close()
		if cursor != None:
		    cursor.close()
		if(type(result) == list and len(result) == 1):
		    return result[0]
		return result

The functions above allows us to abstract the queries by one level. Instead of writing the database connection try/catch in each database call, it is only written once and called by a function which deals with the exceptions.

.. note::
	Query functions flashes the error if exists, and returns the error code in the catching of the exception. You can change this part to redirect the user appropriately.

.. note::
	If there is going to be a string input (varchar), the formatted string should be inside single quotation marks

	.. code-block:: python
		
		result = select(columns="id,name", table="table1", where="name='{}'".format(name_str))

.. _Adding Functionalities:

Adding new functionalities
*****************************

In order to add a new screen, there are a couple of steps needed to be done.

1) Create the appropriate html under /templates folder extending layout.html as follows.


	.. code-block:: html
	
		{% extends "layout.html" %}
		{% block title %}PAGE TITLE COMES HERE{% endblock %}
		{% block content %}

			YOUR HTML COMES HERE		

		{% endblock content %}

	This will ensure that the navigation bar and the footer is the same and consistent with every page.

2) If adding something to an existing page, insert the necessary function to the concering python file.

	For example, if you are going to add a new functionality for admin. Simply go to *admin.py* and insert the new route and the function.

	.. code-block:: python
	
		@admin.route("/admin/new_functionality")
		def admin_new_functionality():
			return render_template("new_page.html")

	Else, create a python file with an descriptive name such as admin_add which indicates that the file will 	contain functionalities of an admin adding something. 
	
	Make sure that you create your blueprint as follows:

	.. code-block:: python

		new_method = Blueprint(name='new_method', import_name=__name__,
		               template_folder='templates')

	
	The routing will be done as follows:

	.. code-block:: python
	
		@new_method.route("/new_method_url")
		def new_method_page():
			return render_template("new_method_page.html")

	Then in *server.py*, register your blueprint as follows:

	.. code-block:: python
	
		from new_method import new_method
		...
		...
		app.register_blueprint(new_method)

.. _Login process:

Login Process
***********************

Our login procedure is secure since we do not store passwords without encryption. The encryption is built-in in postgresql by *pycrypto* extension. This extention allows us to use encryption algorithms such as BlowFish. The extension is created at the beginning of *db_init.py* as follows:

.. code-block:: sql
	
	CREATE EXTENSION IF NOT EXISTS pgcrypto

While registering a new user or login, the credentials are checked at *login.py* in both among users or admins as follows:

.. code-block:: sql

	SELECT * FROM USERS WHERE USERNAME = '%s' AND PASSWORD = crypt('%s',PASSWORD)
 
It automatically encrypts the input password and checks it against the database entries. If a match occurs, we can login. 

.. note::
	We do not store unencrypted passwords and we do not transfer the actual password in the network, just the input.

After login process is completed, we store some information that might be used about the current authorized user in *session* such as authentication type.

.. code-block:: python
	
	session['logged_in'] = True # To check if login process is completed in other pages.
	session['username'] = username 
	session['member_id'] = result[2] # To easily access the member information in profile page and other pages.
	session['team_id'] = select("team_id",...) # To easily access the team information in other pages.
	session['auth_type'] = select("auth_type",...) # To easily check the authentication type to prevent unauthorized access.
            
.. note:: 
	If any additional information is needed in other pages, in order to save time and effort, it can be put into session here.

.. note::
	You can check the authentication of the current session in python side simply by:

	.. code-block:: python
			
		if session.get("auth_type") == "admin":
			...
		if session.get("auth_type"=="Team leader"):
			...
		if session.get("auth_type"=="Subteam leader"):
			...
		if session.get("auth_type"=="Member"):
		
	Note that there are 4 different authentication types. Namely, *admin*,*team leader*, *subteam leader*, *member*. Team's *Consultant* authority is soon to be added. 

.. note::
	You can check the authentication of the current session in HTML side simply by:
	
	.. code-block:: html
		
		{% if session['auth_type'] == 'Team leader' or session['auth_type'] == 'Subteam leader' %}
			...
		{% endif %}

This can be used to hide or show different aspects of the website to a certain authentication type. Such as showing admin panel to admin, member panel to member.

.. _Logout process:

Logout Process
***********************

The logout procedure is simply clearing out the information stored in session in *login.py* as follows:

.. code-block:: python

	if 'logged_in' in session:
		try:
		    session.pop('username', None)
		    session['member_id'] = 0
		    session.pop('logged_in', None)
		    session.pop('auth_type', None)
		    session.pop('team_id', None)
		    flash('You have been successfully logged out.', 'success')
		except:
		    flash('Logging out is not completed.','danger')

.. _File and image upload:

File and Image Upload Process
*********************************

The process is designed such that when a picture or a file is uploaded, the previous one is deleted from the server and the new one is saved in files and updated in the database.

.. code-block:: python
	
	filename = select("picture", "tutorial", "id={}".format(id))[0] # Get the previous picture file name of a tutorial.
		if(image):
			extension = image.filename.split('.')[1] # Get the extension of the image (png, jpeg etc)
			current_date = time.gmtime() # Get the current time to generate a unique name for the new image
			filename = secure_filename(
				"{}_{}.{}".format(id, current_date[0:6], extension)) # 17_2019_12_20.jpg is a sample file name
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath) # Finding the previous image that concernes current tutorial
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imageFolderPath, im)) # Delete the previous image if exists
			image.save(filePath)  # Save the new image
		# Provide an sql statement here to update the database.

The same is valid for a CV upload.

.. code-block:: python
 
 	if(cv and '.pdf' in cv.filename): # To ensure pdf files.
		date = time.gmtime()
		filename = secure_filename(
			"{}_{}.pdf".format(person_id, date[0:6]))
		cvPath = os.path.join(cvFolder, filename)
		cvs = os.listdir(cvFolder)
		digits = int(math.log(int(person_id), 10))+1
		for c in cvs:
			if(c[digits] == '_' and c[0:digits] == str(person_id)):
				os.remove(os.path.join(cvFolder, c))
		cv.save(cvPath)
		# Provide an sql statement here to update the database.
	elif(cv):
		flash("Upload a PDF file.", 'danger')

.. _Error pages:

Error Pages
*********************************

We designed 2 error pages, *page not found* (404) and *internal server error* 500. The first occurs when the user goes to a non-existing page. The latter occurs if there is an error occured in the backend side such as database errors. These pages are designed in HTML and then assigned to their specific errors in *server.py* as follows:

.. code-block:: python

	@app.errorhandler(404)
	def not_found(e):
		return render_template("error_404.html")

	@app.errorhandler(500)
	def server_error(e):
		return render_template("error_500.html")

