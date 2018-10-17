# dbhub

[![Build Status](https://travis-ci.org/huifenqi/dbhub.png?branch=master)](https://travis-ci.org/huifenqi/dbhub)

![demo](./screenshoot.png)

This project has the following basic apps:

* schema (manage table schema like wiki but automatically)

## Installation

To set up a development environment quickly, install Python 2.x first. It
comes with virtualenv built-in. so create a virtual environment with:

`mkvirtualenv dbhub`

Install dependencies:

`pip install -r requirements.txt`

## Support dialects

* Firebird
* Microsoft SQL Server
* MySQL
* Oracle
* PostgreSQL
* SQLite
* Sybase

## Sync databases' schema:

`python manage.py runscript sync`

## Check columns' enumeration:

`python manage.py runscript parser`

## Run server:

`python manage.py runserver --settings=dbhub.settings.dev`
