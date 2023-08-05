Python wrappers for google spread and slack
+++++++++++++++++++++++++++++++++++++++++++

Introduction
============

This package contains two classes that are basic wrappers around slack and
google spread APIs meant to be used to build more complex programs (including
slack bots) upon them. Installing is simply made using pip::

   pip3 install --upgrade slackspread

Only installation will be covered here, head over to the specific documentation
about the slack bot `here <https://slack-and-gspread-tools.readthedocs.io/en/latest/slackbot.html>`__
and the google spreadsheet wrapper 
`here <https://slack-and-gspread-tools.readthedocs.io/en/latest/easyspread.html>`__.

Connect to slack API with ``SlackBot()``
========================================

If using the slack API with python is new to you, head over `here <https://github.com/slackapi/python-slackclient>`__
to get a nice introduction. When everything is in place and you've got a slack bot
token from Slack, store it as an environment variable (``MYBOT_TOKEN`` in
the below exemple) and initiate the slack web client on python by giving the
variable's name as argument.

.. code:: python

   from slackbot import SlackBot
   mybot = SlackBot(token = "MYBOT_TOKEN")

Connect to google spread API with ``Gspread()``
===============================================

``Gspread`` revolves on a json credentials file to authenticate on google
spreadsheets API. The ``init`` method of ``Gspread`` needs both a credentials
json file and a set of environment variables to replace sensitive values on
the json credentials file.

Details on have to obtain that file can be found `here <https://gspread.readthedocs.io/en/latest/>`__.
This file would generally have the following form ::

   {
      "type": "service_account",
      "project_id": "#project id",
      "private_key_id": "#private key id",
      "private_key": "#private key",
      "client_email": "#client email",
      "client_id": "#client id",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "client certification url"
   }


Some of the fields in the ``credentials.json`` must be kept private (in the above
example, the ones preceded with ``#``), so we strongly
advise to replace those fields with empty or non-explicit values in the json file,
especially if you're to push it to git repository, and use environment variables
to store those fields instead. The ``Gspread`` object *will* look for environment
the following variables at initialisation::

   PROJECT_ID
   PRIVATE_KEY_ID
   PRIVATE_KEY
   CLIENT_ID
   CLIENT_EMAIL

More precisely, ``Gspread()`` takes three arguments :

:name: name of spreadsheet to connect to
:environ_prefix: prefix for above listed environment variables
:credentials: path to json file containing credentials with *false* sensitive
              fields

The prefix is combined to the above-listed variables names to build the environment
variables names that the class will look for. The ``init`` method will
replace the corresponding fields in the ``credentials.json`` dictionary with the
values read from those variables.

Say your project's name is something like ``my daily budget``. You
would first store the following environment variables ::

   BUDGET_PROJECT_ID
   BUDGET_PRIVATE_KEY_ID
   BUDGET_PRIVATE_KEY
   BUDGET_CLIENT_ID
   BUDGET_CLIENT_EMAIL

And store somewhere a ``credentials.json``, let's say at
``~/.gscredits/budget-credentials.json`` (on which you would have
replaced the sensitive fields with non-explicit or wrong values). All you need
to do is call ``Gspread`` with the following syntax :

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

Note that you can use the same credits for different spreadsheets. Each set of
credits corresponds to a single project on google cloud, but can connect to *any*
spreadsheet, provided it was authorized to in the spreadsheet's parameters.
