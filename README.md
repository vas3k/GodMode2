# GodMode 2

GodMode is a semi-automatic customizable admin interface generator that lets you add admin interface to any SQL database.
Written in Python 3.x, Flask and SQLAlchemy reflections.

Automatically creates CRUD pages for any table in your database with ability to customize rows and views, create filters,
batch actions and manage access policies for users and groups.

Inspired by Django Admin Interface and Flask-Admin extension, but designed to be a standalone application.
So you don't need to have you app written using Django, Flask or even in Python at all. All you need is a SQL database.
Tested on several pet-projects and medium startups. Good for a quick start because you can make a simple CRUD using a few
lines of code and may add additional functionality as your product grows.

Best for PostgreSQL, MySQL and SQLite. Also supports other SQLAlchemy drivers: Firebird, Microsoft SQL Server,
Oracle and Sybase but they were not officially tested.

![Screenshot](static/screenshot.png?raw=true)

## Installation

**Demo user and password: demo/demo.**

Make sure that you have a Python 3.x. Python 2.x is not supported.

Clone this repository, install all requirements and run app.py.

```
$ git clone https://github.com/vas3k/GodMode2.git
$ cd GodMode2
$ sudo pip3 install -r requirements.txt
$ python3 app.py
```

Then open your browser at [localhost:1488](http://localhost:1488), enter demo/demo to access the main screen.

## Quick Start

UNDER CONSTRUCTION

## Usage

UNDER CONSTRUCTION

## Future Plans

* Buy more beer
* Fix HTML/CSS bugs
* Support default values from database
* Security test for XSS and injections (be careful with that, check all models you create and send me pull requests)
* Think about better filtering/sorting interface
* Make an install~~.php~~ file for easier cold start

## Similar Projects

Other great projects for automatic admin interfaces:

* [Django Admin Module (Python)](https://docs.djangoproject.com/en/dev/ref/contrib/admin/)
* [Flask-Admin (Python)](https://github.com/flask-admin/flask-admin)
* [Sonata Admin Bundle (PHP)](https://github.com/sonata-project/SonataAdminBundle)

## License
vas3k (c) 2016

Licensed under the [WTFPL](http://www.wtfpl.net/) license.
Full text of the license can be found in the LICENSE.txt file.

> [vas3k.ru](http://vas3k.ru) &nbsp;&middot;&nbsp;
> GitHub [@vas3k](https://github.com/vas3k) &nbsp;&middot;&nbsp;
> Twitter [@vas3k](https://twitter.com/vas3k)
