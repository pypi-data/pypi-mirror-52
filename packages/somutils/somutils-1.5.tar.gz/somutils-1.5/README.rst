somenergia-utils
================

This module includes different Python modules and scripts ubiquiously
used on scripts in SomEnergia cooperative but with no entity by
themselves to have their own repository.

-  ``venv``: run a command under a Python virtual enviroment
-  ``sql2csv.py``: script to run parametrized sql queries and get the
   result as (tab separated) csv.
-  ``dbutils.py``: module with db related functions

   -  ``fetchNs``: a generator that wraps db cursors to fetch objects
      with attributes instead of psycopg arrays
   -  ``nsList``: uses the former to build a list of such object (slower
      but maybe convinient)
   -  ``csvTable``: turns the results of a query into a tab separated
      table with proper header names

-  ``sheetfetcher.py``: convenience class to retrieve data from gdrive
   spreadshets
-  ``trace``: quickly enable and disable tracing function calling by
   decorating them with ``@trace``

``venv`` script
---------------

This script is useful to run Python scripts under a given virtual
environment. It is specially useful to run Python scripts from crontab
lines.

.. code:: bash

    usage: venv /PATH/TO/PYTHON/VIRTUALENV COMMAND [PARAM1 [PARAM2...]]

``sql2csv.py`` script
---------------------

Runs an SQL file and outputs the result of the query as tabulator
separated csv.a

You can provide query parameters either as yamlfile or as commandline
options.

.. code:: bash

     sql2csv.py <sqlfile> [<yamlfile>] [--<var1> <value1> [--<var2> <value2> ..] ]

``dbutils`` Python module
-------------------------

Convenient cursor wrappers to make the database access code more
readable.

Example:

.. code:: python

    import psycopg2, dbutils
    db = psycopg2.connect(**dbconfiguration)
    with db.cursor() as cursor :
        cursor.execute("SELECT name, age FROM people")
        for person as dbutils.fetchNs(cursor):
            if person.age < 21: continue
            print("{name} is {age} years old".format(person))

``sheetfetcher`` Python module
------------------------------

Convenient wraper for gdrive.

.. code:: python

    from sheetfetcher import SheetFetcher

    fetcher = SheetFetcher(
        documentName='My Document',
        credentialFilename='drive-certificate.json',
        )
    table = fetcher.get_range("My Sheet", "A2:F12")
    fulltable = fetcher.get_fullsheet("My Sheet")

-  Document selectors can be either an uri or the title
-  Sheet selectors can be either an index, a name or an id.
-  Range selectors can be either a named range, index tuple or a "A2:F5"
   coordinates.
-  You should `Create a certificate and grant it access to the
   document <http://gspread.readthedocs.org/en/latest/oauth2.html>`__

trace
-----

This decorator is a fast helper to trace calls to functions and methods.
It will show the name of the functions the values of the parameters and
the returned values.

.. code:: python

    from trace import trace

    @trace
    def factorial(n):
        if n<1: return 1
        return n*factorial(n-1)

    factorial(8)

    ('> factorial', (8,))
    ('> factorial', (7,))
    ('> factorial', (6,))
    ('> factorial', (5,))
    ('> factorial', (4,))
    ('> factorial', (3,))
    ('> factorial', (2,))
    ('> factorial', (1,))
    ('> factorial', (0,))
    ('< factorial', (0,), '->', 1)
    ('< factorial', (1,), '->', 1)
    ('< factorial', (2,), '->', 2)
    ('< factorial', (3,), '->', 6)
    ('< factorial', (4,), '->', 24)
    ('< factorial', (5,), '->', 120)
    ('< factorial', (6,), '->', 720)
    ('< factorial', (7,), '->', 5040)
    ('< factorial', (8,), '->', 40320)

