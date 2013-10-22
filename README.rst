Addon registration
##################

.. image:: https://secure.travis-ci.org/mozilla/addon-registration.png?branch=master
   :alt: Build Status
   :target: https://secure.travis-ci.org/mozilla/addon-registration

.. image:: https://coveralls.io/repos/mozilla/addon-registration/badge.png
   :target: https://coveralls.io/r/mozilla/addon-registration 

(Still in development, don't rely on it just yet.)

The goal of this service is to integrate closely with the addons.mozilla.org
website (a.k.a AMO) to provide a way to register non AMO-listed addons as
a really simple process.

How to get started?
===================

Behind the scene, we are using `Celery <http://celeryproject.org>`_ to
distribute our jobs in a queue. We use `Redis <http://redis.io>`_ as a backend
so you would need to get it installed on your machine.

Once you have the redis dependency in place, you would just need to run the
makefile::

    $ make build
    
Then there are two parts. The fist one runs the web service, and the other one
the celery workers.

To start the service::

    $ make serve

To start the celery workers::

    $ make workers

And you should have the server up & running!

How to run the tests?
=====================

You just need to type `make test` to run the tests. The default behaviour is to
run the tests against a temporary database, but you can change that by
explicitely setting up the SQL_URI environment variable to the backend you
want, e.g. SQLURI=mysql://addonreg:addonreg@localhost/addonreg make test
