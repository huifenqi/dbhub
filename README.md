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

## Run server

`python manage.py runserver --settings=dbhub.settings.dev`

## Add database

* name: database name
* config: whole url for connect with database
* for MySQL: mysql://{username}:{password}@{database-url}:3306/{database-name}?charset=utf8
* for SQLite: sqlite:////{absolute-path-to-db-file}

## Sync databases' schema and check columns' enumeration

`python manage.py runscript sync`

`python manage.py runscript check`

## How to write comments with enumeration

1. write description first;
2. write enumerations after.

```
charset with description, blah, blah, blah

utf8: A UTF-8 encoding of the Unicode character set using one to three bytes per character. default utf8 of mysql, max length is 3 bytes, not support characters, such as emoji.

utf8mb4: A UTF-8 encoding of the Unicode character set using one to four bytes per character.

```

## Supported dialects

* Firebird
* Microsoft SQL Server
* MySQL
* Oracle
* PostgreSQL
* SQLite
* Sybase
