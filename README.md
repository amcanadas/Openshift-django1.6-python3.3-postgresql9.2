Django 1.6 and Python 3 on OpenShift
====================================

This git repository helps you get up and running quickly w/ a Django 1.6 and
Python 3.3 installation on OpenShift.  The Django project name used in this
repo is 'blas' but you can feel free to change it.  Two backends are supported; SQLite3
and PostgreSQL 9.
SQLite3 database runtime is found in `$OPENSHIFT_DATA_DIR/sqlite3.db`.


If using SQLite3
----------------

Before you push this app for the first time, you will need to change
the [Django admin password](#admin-user-name-and-password).
Then, when you first push this
application to the cloud instance, the SQLite database is copied from
`wsgi/blas/sqlite3.db` to $OPENSHIFT_DATA_DIR/ with your newly 
changed login credentials. Other than the password change, this is the 
stock database that is created when `python manage.py syncdb` is run with
only the admin app installed.

On subsequent pushes, a `python manage.py syncdb` is executed to make
sure that any models you added are created in the DB.  If you do
anything that requires an alter table, you could add the alter
statements in `GIT_ROOT/.openshift/action_hooks/alter.sql` and then use
`GIT_ROOT/.openshift/action_hooks/deploy` to execute that script (make
sure to back up your database w/ `rhc app snapshot save` first :) )

If PostgreSQL is used
---------------------

On every push a 'python manage.py syncdb' is executed to make sure that any
models you add is created in the DB. In preloaded data is needed, use of 
fixtures is recomended (not in applied in this project).
If admin database is created for the first time, an admin user is created,
otherwhise, admin passord is automatically changed for security reasons.


With this you can install Django 1.6 with Python 3.3 on OpenShift.

Running on OpenShift
--------------------

Create an account at http://openshift.redhat.com/

Install the RHC client tools if you have not already done so:
    
    sudo gem install rhc

Create a python-3.3 application

    rhc app create -a djangopy3 -t python-3.3

If PostgreSQL is used, add Python 9.2 Cartridge

    rhc cartridge-add -a djangopy3 -c postgresql-9.2

Set some environment variables for the OpenShift application

    rhc env set DJANGO_PROJECT_NAME='blas' --app djangopy3
    rhc env set DJANGO_DB_ENGINE='postgresql' --app djangopy3

where DJANGO_PROJECT_NAME is the name of your django project in the wsgi directory and DJANGO_DB_ENGINE
has de values 'postgresql' or 'sqlite3' depending on your backend. In working on local developement, this
 variables are needed too.

Add this upstream repo

    cd djangopy3
    git remote add upstream -m master git://github.com/amcanadas/django-py3-openshift-quickstart.git
    git pull -s recursive -X theirs upstream master

Then push the repo upstream

    git push

Here, the [admin user name and password will be displayed](#admin-user-name-and-password), so pay
special attention.
	
That's it. You can now checkout your application at:

    http://djangopy3-$yournamespace.rhcloud.com

Admin user name and password
----------------------------
As the `git push` output scrolls by, keep an eye out for a
line of output that starts with `Django application credentials: `. This line
contains the generated admin password that you will need to begin
administering your Django app. This is the only time the password
will be displayed, so be sure to save it somewhere. You might want 
to pipe the output of the git push to a text file so you can grep for
the password later.

When you make:

     git push

In the console output, you must find something like this:

     remote: Django application credentials:
     remote: 	user: admin
     remote: 	pwd: SY1ScjQGb2qb

Or you can go to SSH console, and check the CREDENTIALS file located 
in $OPENSHIFT_DATA_DIR.

     cd $OPENSHIFT_DATA_DIR
     vi CREDENTIALS

You should see the output:

     Django application credentials:
     		 user: admin
     		 pwd: SY1ScjQGb2qb

After, you can change the password in the Django admin console.

Django project directory structure
----------------------------------

     django3/
        .gitignore
     	.openshift/
     		README.md
     		action_hooks/  (Scripts for deploy the application)
     			build
     			post_deploy
     			pre_build
     			deploy
     			secure_db.py
                secure_pgdb.py
     		cron/
     		markers/
     	setup.py   (Setup file with de dependencies and required libs)
     	app.py (This file execute Django over on WSGI)
     	README.md
     	libs/   (Adicional libraries)
     	data/	(For not-externally exposed wsgi code)
     	wsgi/	(Externally exposed wsgi goes)
     		application (Script to execute the application on wsgi)
     		blas/	(Django project directory)
     			__init__.py
     			manage.py
     			openshiftlibs.py
                openshiftstaticfiles.py (lib to use static files on the same server)
     			settings.py
     			urls.py
     			views.py
     			wsgi.py
     			templates/
     				home/
     					home.html (Default home page, change it)
     		static/	(Public static content gets served here)
     			README

From HERE you can start with your own application.

Important
---------

Django doesn't recommend use of its static file (like css, js) on production server for a number of reasons.

For use Django on wsgi and serve the static files in the same server, it is necesary use the additional package static3.
You can install it in the setup.py

On OpenShift, Django is served through wsgi, like cherrypy, this package can be installed with setup.py

     from setuptools import setup

     setup(name='YourAppName', version='1.0',
           description='OpenShift Python-3.3 / Django-1.6 Community Cartridge based application',
           author='Your Name', author_email='admin@example.org',
           url='https://pypi.python.org/pypi',

           #  Uncomment one or more lines below in the install_requires section
           #  for the specific client drivers/modules your application needs.
           install_requires=['Django<=1.6',
                             'CherryPy', # If you want serve Django through CherryPy
                             'static3',  # If you want serve the static files in the same server
                             #  'mysql-connector-python',
                             #  'pymongo',
                             'psycopg2',
           ],
     )

if you don't install cherrypy, OpenShift uses wsgiref.
