# GodMode 2

GodMode is customizable semi-automatic admin interface generator that lets you add an admin interface to any SQL database.
It is written in Python 3.x and Flask, with superpower of WTForms and SQLAlchemy reflections.

GodMode automatically creates CRUD pages for any table in your database, with an ability to customize rows and views, create filters,
batch actions and to manage access policies for users and groups.

Inspired by Django Admin Interface and Flask-Admin extension, it has been designed as a standalone application.
It's not necessary to have your app written using Django, Flask or even in Python at all. All you need is a SQL database.
GodMode has been tested on several pet projects and projects of medium startups. The interface is good for a quick start since you can make a simple CRUD using just a few
lines of code and add additional functionality with growth of your product.

GodMode is more suitable for PostgreSQL, MySQL and SQLite. It also supports other SQLAlchemy drivers such as Firebird, Microsoft SQL Server,
Oracle and Sybase. They were not officially tested though, so pull-requests and issue reports are welcome.

![Screenshot](static/screenshot.png?raw=true)

## Installation

**Demo user and password: demo/demo.**

Make sure that you have Python 3.x. Python 2.x is not supported.

Clone this repository, install all the requirements and run app.py.

```
$ git clone https://github.com/vas3k/GodMode2.git
$ cd GodMode2
$ sudo pip3 install -r requirements.txt
$ python3 app.py
```

Then open your browser at [localhost:1488](http://localhost:1488), enter demo/demo to access the demo version of the main screen.

## Quick Start

For example, your PostgreSQL database on `localhost` is called `dbname`
and you have the `users` table in the database you want to manage.
Then your DSN is `postgresql+psycopg2://username:password@localhost/dbname`.
Check if you have access to the database from your computer before you move to the first step.

**First step:** create new file in `db` directory and name it `my.py`, for example.
You can use `demo.py` as an example.
If you're familiar with SQLAlchemy it will be easy.

```python
import sqlalchemy as sa

from base.db import BaseDatabase


class MyDatabase(BaseDatabase):
    dsn = "postgresql+psycopg2://username:password@postgres.example.com/dbname"

MyDatabase.bind()  # you need to call bind() before any table declarations


class User(MyDatabase.TableBase):
    __table__ = sa.Table("users", MyDatabase.metadata, autoload=True)
    # you can declare your table columns here, but autoload=True will try to do it for you
```

**Second step:** create new model file for user administration in `models` directory. For example `users.py`.

```python
from base.model import BaseAdminModel
from db.my import MyDatabase, User

class UsersAdminModel(BaseAdminModel):
    db = MyDatabase
    table = User
    name = "users"  # for URL's
    title = "Users"  # for sidebar
    icon = "icon-user"
```

**Third step:** modify `app.py` file in the root directory and specify your database and model classes.

```python
import settings
from godmode import GodModeApp
from db.my import MyDatabase
from models.users import UsersAdminModel

app = GodModeApp(
    databases=[MyDatabase],
    models=[
        UsersAdminModel,
    ]
)

if settings.DEBUG:
    app.run()
```

Now run `$ python3 app.py` and open [localhost:1488](http://localhost:1488). You should see your Users table in the sidebar.

Great, you've just created your first simple CRUD for `users` table. Check the Usage section to learn how to configure it.

Probably, all of these steps will be automated with a script one day.

## Usage

![list_view](static/list_view.png?raw=true)

### Databases and Tables

`db/<your_db_name>.py`

```python
# how to connect to your database
class FirstDatabase(BaseDatabase):
    dsn = "sqlite:///internal/demo.sqlite"

# bind your database class with engine (call it before any table declaration!)
FirstDatabase.bind()

# you can even have multiple databases (it's better to describe them in separate files though)
class SecondDatabase(BaseDatabase):
    dsn = "postgresql+psycopg2://username:password@postgres.example.com/dbname"

SecondDatabase.bind()

# describe a couple of tables
class User(FirstDatabase.TableBase):
    __table__ = sa.Table('users', FirstDatabase.metadata, autoload=True)


class Post(FirstDatabase.TableBase):
    __table__ = sa.Table('posts', FirstDatabase.metadata, autoload=True)

    # if you want GodMode to make fast links for you
    user = relationship('User')
```

Now, tell GodMode about all your databases by editing `app.py`.

```python
app = GodModeApp(
    databases=[DemoDatabase, SecondDatabase],
    models=[]
)
```

### Models

`models/<name_your_model>.py`

```python
class YourAdminModel(BaseAdminModel):
    db = FirstDatabase                      # database class
    table = User                            # table class
    acl = ACL.ADMIN                         # lowest ACL group who has access to this model
    name = "my_table"                       # name for url building (must be unique)
    title = "My Table"                      # title for sidebar
    icon = "icon-loadingeight"              # icon from webhostinghub.com/glyphs/
    index = 0                               # higher index -> higher position
    place = "sidebar"                       # "sidebar" (left) or "navbar" (top)
    group = None                            # group class (see Groups section)
    actions = []                            # default actions for all views (see Actions section)
    enable_log = False                      # turn off activity logging for this model
    excluded_fields_for_log = ["password"]  # exclude "password" field from activity log
    fields = [                              # default fieldset for all views
        "id",
        "name",
        "bio",
        "is_locked",
        "my_custom_field_that_not_in_database"
    ]
    id_field = "id"                         # primary key field (for relative linking)
    widgets = {                             # custom widget classes for certain fields
        "name": NameWidget,
        "is_locked": BooleanWidget,
        "my_custom_field_that_not_in_database": MyCustomWidget
    }

    # use BaseListView to display this table (default behaviour)
    list_view = BaseListView

    # do not generate create, edit and delete views,
    # for example for read-only tables
    edit_view = None
    create_view = None
    delete_view = None

    # you can make your custom details view based on BaseDetailsView
    # for example if you want to use your own template
    class CustomDetailsView(BaseDetailsView):
        template = "views/my_custom_details.html"
        widgets = {...}

    details_view = CustomDetailsView        # see Views section for more info
```

Now return to `app.py` file to specify new models for your app.


```python
app = GodModeApp(
    databases=[FirstDatabase, SecondDatabase],
    models=[YourAdminModel]  # put new model here
)
```

### Views

```python
class MyListView(BaseListView):
    acl = ACL.MODERATOR                     # lowest ACL group who has access to this view
    title = "My List"                       # title for HTML
    template = "list.html"                  # you can specify your template for this view
    fields = [...]                          # same as "fields" in model, but specific for this view
    sorting = ["id", "name"]                # fields allowed for sorting (default = None — all fields)
    batch_actions = [MyBatchAction]         # see screenshot above
    object_actions = [MyObjectAction]
    max_per_page = 100
    has_list_delete = True                  # if you have DeleteView but want to hide [x] button from ListView
    default_sorting = "id desc"             # default ordering, better specify in SQLAlchemy manner: User.id.desc()
    widgets = {
        "name": TextWidget                  # overwrite or append model widgets
    }
```

### Actions

```python
class MyAction(BaseAction):
    title = "Ban"
    name = "ban"
    acl = ACL.ADMIN
    enable_log = True

    # defines how to render the form of this action (if it has a form)
    def render_form(self, *args, **kwargs):
        return render_template("actions/button_action.html", url=self.name, button_label="Submit")

    # some code, triggered with action; kwargs have all request parameters
    # but all you usually need is kwargs["id"]
    def do_item_action(self, *args, **kwargs):
        user_id = kwargs.pop("id")
        self.model.update(id=user_id, is_banned=True)
        return render_template("success.html", message="User {} was banned".format(id))
```

### Widgets

Widgets are powered by a great [WTForms](https://github.com/wtforms/wtforms) library for form parsing, validation and rendering.
They are responsible for rendering in all the views — create, list, details, delete.
If you're familiar with WTForms, you have all the superpowers in your hands. Otherwise, check the documentation.

You can also create widgets which are completely independent from WTForms. Check `widgets/polygon.py` for example.

```python
class MyWidget(BaseWidget):
    filterable = True   # allows you to filter by this field
    field = wtforms.StringField()  # field class from WTForms
    field_kwargs = {"style": "max-width: 100px;"}  # kwargs for WTForms Field rendering

    # how to render this field in EditView
    def render_edit(self, form=None, item=None):
        # default implementation with WTForm rendering, but it can be overridden
        pass

    # how to render this field in ListView
    def render_list(self, item):
        value = getattr(item, self.name, None)
        return jinja2.escape(str(value)) if value is not None else "null"

    # how to render this field in DetailsView
    def render_details(self, item):
        return self.render_list(item)
```

### Groups

Groups allow you to combine models into logical sets in the sidebar.
Models without a group have higher priority and displayed at the top of the sidebar.

```python
class MyGroup(BaseGroup):
    acl = ACL.MODERATOR   # you can hide the whole group from users lower than MODERATOR level
    name = "Group name"   # title to display in sidebar
    index = 1000          # higher index -> higher position
```

### ACLs and policies

ACLs and their priorities are defined in `common/acl.py` file: `PRIORITY = [SUPERUSER, ADMIN, MODERATOR, ALL]`.
You can create any group for yourself but don't forget to put it into PRIORITY list.

* SUPERUSER is a group of users with highest privileges. They have permission to do everything in GodMode. 
Use carefully. Usually 1 superuser per project is enough.
* ADMINs have all the permissions to edit the databases but they cannot create and manage other GodMode users.
* MODERATORs are read-only users by default. You can hide any models, views, groups and actions from moderators.
* ALL specifies that module is visible even for unauthorized users. It was made for login screen — don't know how it can be useful for you.

Policies are written in a bad and unoptimized way, so large refactoring is needed.
**Do not use it for now.**

## Future Plans

* ~~Buy more beer~~
* Fix HTML/CSS bugs (maybe make a redesign)
* Make Widgets Great Again (+sexy appearance)
* Support default values from more database drivers
* Rewrite policies
* Security test for XSS and SQL injections (be careful with that; check all the models you create and send me pull requests)
* Think about better filtering/sorting interface
* Make an install~~.php~~ file for easier cold start
* More AJAX for validation and inline editing, probably

## Similar Projects

Other great projects of automatic admin interfaces:

* [Django Admin Module (Python)](https://docs.djangoproject.com/en/dev/ref/contrib/admin/)
* [Flask-Admin (Python)](https://github.com/flask-admin/flask-admin)
* [Sonata Admin Bundle (PHP)](https://github.com/sonata-project/SonataAdminBundle)

## License
vas3k (c) 2016+

Licensed under the [WTFPL](http://www.wtfpl.net/) license.
Full text of the license can be found in the LICENSE.txt file.

> [vas3k.ru](http://vas3k.ru) &nbsp;&middot;&nbsp;
> GitHub [@vas3k](https://github.com/vas3k) &nbsp;&middot;&nbsp;
> Twitter [@vas3k](https://twitter.com/vas3k)
