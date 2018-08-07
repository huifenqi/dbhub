

# dbhub

This project has the following basic apps:

* schema (manage table schema like wiki but automatically)

## Installation

To set up a development environment quickly, install Python 2.x first. It
comes with virtualenv built-in. so create a virtual environment with:

`mkvirtualenv dbhub`

Install dependencies:

`pip install -r requirements.txt`

Run server:

`python manage.py runserver --settings=dbhub.settings.development`
