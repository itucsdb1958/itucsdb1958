Developer Guide
===============

Database Design
---------------

DIAGRAMLAR BURAYA GELECEK


Setting up the environment for development
---------------------------------------------

Clone the repository from github and install requirements as follows,

.. code-block:: console

	$ git clone https://github.com/itucsdb1958/itucsdb1958.git
	$ cd itucsdb1958
	$ pip install -r requirements.txt

After the installation, you can simply call the following command to run the server.

.. code-block:: console

	$ python server.py

Database setup for local development
-----------------------------------------

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
-----------------------------------------

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

	if(not RELEASE):
	    os.environ['DATABASE_URL'] = "postgres://postgres:docker@localhost:5432/postgres"
	    initialize(os.environ.get('DATABASE_URL'))


.. toctree::

   member1
   member2
   member3
   member4
   member5
