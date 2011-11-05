Django Server Configuration
===========================

Overview
--------

Adds a server_conf management command to Django for quick generation of nginx, apache & supervisor configuration files based on the project's settings file. Detects celery, uwsgi & gunicorn.

This exists because I seem to be doing the same thing over and over again on a regular basis.
It's mainly meant for generating a boilerplate configuration files.

Usage
-----

In settings.py:

    SERVER_APP_NAME = "foobar_project"
    SERVER_DOMAIN = "foobar.com"
    SERVER_SUPERVISOR_USER = "foobar"
    SERVER_ROOT_LOG = "/home/foobar/logs/fp"

###Generating files

    python manage.py server_conf

Would print the configuration to the console

    python manage.py server_conf --nginx --supervisor

Would generate the files foobar_project-nginx.conf and foobar_project-supervisor.conf

Settings
--------

No settings are required, everything is optional.

* SERVER_APP_NAME - The name of the application, appears in  templates. Defaults to the first part of the ROOT_URLCONF.
* SERVER_DOMAIN - Defaults to test.com.
* SERVER_UPSTREAM - Allows for specifying what upstream server to use. If nothing is specified, the following setting is generated from the following values.
    * SERVER_UPSTREAM_HOST (Defaults to "127.0.0.1")
    * SERVER_UPSTREAM_PORT (Uses 8000 if gunicorn is detected, 3031 otherwise)
* SERVER_ROOT_LOG - Root name of the log file, recommended that you set this to something, by default it's set to */var/log/appname*. The ".log" is appended in the templates.
* SERVER_USE_SSL - Generate SSL block, default false
* SERVER_SSL_REWRITE - Rewrite all requests to SSL, default false
* SERVER_SSL_CRT_PATH - Path to crt file, defaults to */path_to_parent_folder/ssl/appname.crt*
* SERVER_SSL_KEY_PATH - Path to key file, defaults to */path_to_parent_folder/ssl/appname.key*
* SERVER_SSL_CA_PATH - Path to CA folder, defaults to */path_to_parent_folder/ssl/CA*
* SERVER_SSL_CA_FILE - Path to CA file, defaults to */path_to_parent_folder/ssl/CA/appname.crt*
* SERVER_DISABLE_CELERYBEAT - If celery is detected and you don't want to generate a supervisor block for celerybeat, set this as true
* SERVER_SUPERVISOR_USER - Specifies which user runs the applications, defaults to www-user.
* WSGI_SCRIPT_ALIAS - Point this to your wsgi file if you're using Apache, defaults to "django.wsgi" in the parent folder of the project.

Todo
----

Tests
