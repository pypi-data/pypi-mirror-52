Python wrappers for google spread and slack
+++++++++++++++++++++++++++++++++++++++++++

Presentation
============

Available modules
-----------------

WIP

Installation
------------

.. code:: bash

   pip3 install --upgrade slackspread

Prerequisites for a smooth authentication
=========================================

Authentication to slack API
---------------------------

If using python sdk for slack API is new to you, head over `here <https://github.com/slackapi/python-slackclient>`__
to get a nice introduction. When everyting is in place and you got your slack bot
token from Slack, just store it as an environment variable (``MYBOT_TOKEN`` in
the below exemple) and initiate the slack web client on python by giving the
variable's name as argument.

.. code:: python

   from slackbot import SlackBot

   mybot = SlackBot(token = "MYBOT_TOKEN")

Authentication to google spreads API
------------------------------------

``Gspread`` revolves on a json credentials file to authenticate on google
spreads API. The ``init`` method of ``Gspread`` needs both the json file and a
set of environment variables.

Details on have to obtain that file can be found `here <https://gspread.readthedocs.io/en/latest/>`__.
This file would generally have the following form ::

   {
      "type": "service_account",
      "project_id": "project id",
      "private_key_id": "private key id",
      "private_key": "private key",
      "client_email": "client email",
      "client_id": "client id",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": ""
   }


Some of the fields in the ``credentials.json`` must be kept private, so we strongly
advise to replace those fields with empty or non-explicit values, especially if
you push the json credentials file to a git repo.

In any case, when initiating a ``Gspread`` object, several environment variables
will be looked for to replace the sensitive fields from the json with the right
values (stored as environment variables). Here is the list of fields that will
be replaced within the json before trying to authenticate on the spread API ::

   PROJECT_ID
   PRIVATE_KEY_ID
   PRIVATE_KEY
   CLIENT_ID
   CLIENT_EMAIL

Precisely, ``Gspread()`` takes three arguments :

:name: name of spreadsheet to connect to
:environ_prefix: prefix for above listed environment variables
:credentials: path to json file containing credentials with *false* sensitive
              fields

The prefix allows to store environment variables for several spreadsheet API
projects. Say your project's name is something like ``my daily budget``. You
would first store the following environment variables ::

   BUDGET_PROJECT_ID
   BUDGET_PRIVATE_KEY_ID
   BUDGET_PRIVATE_KEY
   BUDGET_CLIENT_ID
   BUDGET_CLIENT_EMAIL

And store somewhere a ``credentials.json``, let's say at
``~/.gscredits/budget-credentials.json`` (on which you would have
replaced the sensitive fields with non-explicit or wrong values).

All you need to do is call ``Gspread`` with the following syntax :

.. code:: python

   from easyspread import Gspread

   budget_spread = Gspread(
       name = 'my daily budget',
       environ_prefix = 'BUDGET',
       credentials = "~/.gscredits/budget-credentials.json"
   )

Using environment variables makes it possible to have your code working while
being safe on a network server, since the json file is stored without any sensitive
data in it and the sensitive values are protected as environment variables.
