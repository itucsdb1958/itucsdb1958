Developer Guide
===============

* :ref:`Database design`
* :ref:`Setting environment`
* :ref:`Database setup`
* :ref:`Running SQL`
* :ref:`Adding Functionalities`

.. _Database design:

Database Design
---------------

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
	Query functions flashes the error if exists, and returns the error code. You can use this code to redirect the user appropriately.

.. note:: 
	Additional input checks can be added here.

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

3) Else, create a python file with an descriptive name such as admin_add which indicates that the file will contain functionalities of an admin adding something. 

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


.. toctree::

   member1
   member2
   member3
