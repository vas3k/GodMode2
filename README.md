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

Then open your browser at [localhost:1488](http://localhost:1488), enter demo/demo to access demo version of the main screen.

## Quick Start

For example your PostgreSQL database on `localhost` called `dbname`
and you have the `users` table in your database that you want to manage.
So your DSN is `postgresql+psycopg2://username:password@localhost/dbname`.
Check that you have an access to the database from your computer before the first step.

**First step:** create new file in `db` directory and name it for example `my.py`.
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

**Second step:** create new model file for users admin in `models` directory. For example `users.py`.

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

Maybe one day all these steps will be automated by the one script.

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

# you even can have multiple databases (but better to describe them in separate files)
class SecondDatabase(BaseDatabase):
    dsn = "postgresql+psycopg2://username:password@postgres.example.com/dbname"

SecondDatabase.bind()

# describe couple of tables
class User(FirstDatabase.TableBase):
    __table__ = sa.Table('users', FirstDatabase.metadata, autoload=True)


class Post(FirstDatabase.TableBase):
    __table__ = sa.Table('posts', FirstDatabase.metadata, autoload=True)

    # if you want GodMode to make fast links for you
    user = relationship('User')
```

Now tell GodMode about all your databases by editing `app.py`.

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
        ("name", {"widget": NameWidget}),
        "bio",
        ("is_locked", {"widget": BooleanWidget})
    ]
    id_field = "id"                         # primary key field (for relative linking)
    custom_widgets = {                      # default widget classes for certain fields
        "name": NameWidget                  # if you don't want to specify all fields in big table
    }

    # use BaseListView for display this table (default behaviour)
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

    details_view = CustomDetailsView        # see Views section for more info
```

Now return to the `app.py` file to specify new models for your app.


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
    fields = [...]                          # like "fields" in model, but specific for this view
    sorting = ["id", "name"]                # fields which allowed to sorting (default = None — all fields)
    batch_actions = [MyBatchAction]         # see screenshot above
    object_actions = [MyObjectAction]
    max_per_page = 100
    has_list_delete = True                  # if you have DeleteView but want to hide [x] button from ListView
    default_sorting = "id desc"             # default ordering, better specify in SQLAlchemy manner: User.id.desc()
```

### Actions

```python
class MyAction(BaseAction):
    title = "Ban"
    name = "ban"
    acl = ACL.ADMIN
    enable_log = True

    def render_form(self, *args, **kwargs):
        # defines how to render the form of this action (if it has a form)
        return render_template("actions/button_action.html", url=self.name, button_label="Submit")

    def do_item_action(self, *args, **kwargs):
        # some code then action is executed, kwargs have all request parameters
        # but all you usually need is kwargs["id"]
        id = kwargs.pop("id")
        self.model.update(id=id, is_banned=True)
        return render_template("success.html", message="User {} was banned".format(id))
```

### Widgets

```python
class MyWidget(BaseWidget):
    filterable = True   # allows you to filter by this field

    def render_list(self, item):
        # defines how to render this field in ListView

    def render_edit(self, item=None):
        # how to render this field in EditView
        pass

    def render_details(self, item):
        # how to render this field in DetailsView
        pass

    def parse_value(self, value):
        # how to parse string representation of this value
        # submitted from HTML form on editing or creation
        pass
```

### Groups

Groups allows you to combine models into logical sets in sidebar.
Models without group have a higher priority and displayed at the top of sidebar.

```python
class MyGroup(BaseGroup):
    acl = ACL.MODERATOR   # you can hide whole group from users lower than MODERATOR level
    name = "Group name"   # title to display in sidebar
    index = 1000          # higher index -> higher position
```

### ACL's and policies

ACL's and their priorities are defined in `common/acl.py` file: `PRIORITY = [SUPERUSER, ADMIN, MODERATOR, ALL]`.
You can create any group for yourself but don't forget to put it into PRIORITY list.

* SUPERUSER is a group of users with the highest privileges. They have permission to do everything in GodMode. Use carefully.
* ADMIN's have all permissions to edit all databases but can't create and manage other GodMode users.
* MODERATOR's are read-only users by default. You're able to hide some models, views, groups and actions from moderators.
* ALL specifies that module is public even for unauthorized users. Made for login screen, don't know why they can be useful for you.

Policies are written in a very bad and unoptimized way, so they really need a huge refactoring.
**Don't use it for now.**

## Future Plans

* Buy more beer
* Fix HTML/CSS bugs
* Support default values from database
* Security test for XSS and injections (be careful with that, check all models you create and send me pull requests)
* Think about better filtering/sorting interface
* Make an install~~.php~~ file for easier cold start
* Maybe more AJAX for validation and inline editing

## Similar Projects

Other great projects for automatic admin interfaces:

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
