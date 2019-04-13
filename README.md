# GodMode 2

GodMode is a customizable semi-automatic admin site generator for any SQL databases and lazy coders like me. 

Inspired by [Django Admin site](https://docs.djangoproject.com/en/dev/ref/contrib/admin/) 
and [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/), it was designed to be a standalone 
app. GodMode automatically creates CRUD pages for any table in your database with an ability to customize views, 
create filters, implement batch actions, and manage access policies for users. 
It uses power of Python 3, Flask, SQLAlchemy and WTForms. 

Doesn't matter if your application is written in Django, asyncio or even in Python at all. 
All you need is a SQL database — tested with PostgreSQL, MySQL and SQLite.
You need a few lines of code to create and manage a model which can be extended with more features as your project grow. 

**:warning: Use it with caution! Check the code before applying on sensitive data.**

GodMode is immature but tested by myself in couple medium-sized startups and my personal blog for years.
Use it at your own risk.

![Screenshot](static/screenshot.png?raw=true)

## Installation

Using docker-compose:

```
$ git clone https://github.com/vas3k/GodMode2.git
$ cd GodMode2
$ docker-compose up
```

**OR**

Or build it locally:

```
$ git clone https://github.com/vas3k/GodMode2.git
$ cd GodMode2
$ sudo pip3 install -r requirements.txt
$ DEBUG=true python3 app.py
```

Then go to [localhost:1414](http://localhost:1414) and enter demo/demo to access demo version.

### Demo user and password: demo/demo

## Quick Start: Create Your First Model

Let's say you have a PostgreSQL database on `localhost` called `dbname` with a `users` table in there.

**Step one:** create a new file in `db` directory. Name is up to you, I will use `my.py`.
You need to declare database connection and a User model there. 
Use `db/demo.py` file as an example.

```python
import sqlalchemy as sa

from base.db import BaseDatabase


class MyDatabase(BaseDatabase):
    dsn = "postgresql+psycopg2://username:password@postgres.example.com/dbname"


class User(MyDatabase.TableBase):
    __table__ = sa.Table("users", MyDatabase.metadata, autoload=True)
    # you can describe your columns here but autoload=True will do it for you
```

**Step two:** create a new GodMode model file in the `models` directory. Let's say, `users.py`. 
Here's a minimal setup:

```python
from base.model import BaseAdminModel
from db.my import MyDatabase, User

class UsersAdminModel(BaseAdminModel):
    db = MyDatabase
    table = User
    name = "users"      # path for URL's
    title = "Users"     # sidebar title
    icon = "icon-user"  # sidebar icon
```

**Step three:** add the database and admin model to the `app.py` file like this:

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

Done. You're beautiful. Now run the app again and open the [localhost:1414](http://localhost:1414) to see your new model.
I hope, all these steps will be automated one day with a wizard. Now let's go deeper to configurations.


## Usage

![list_view](static/list_view.png?raw=true)

### Databases and Tables

The first thing is always a database. GodMode is designed to work with multiple databases at the same time,
so I recommend to put each in a separate file (but it's not a strict rule). 
See a [demo example](database/demo.py) and let's create a new file `database/first_database.py`. 


```python
from godmode.database import database

# connect to database using standard connection string
FirstDatabase = database("sqlite:///database/first_database.sqlite")

# refer tables you want to use here
class User(FirstDatabase.TableBase):
    __table__ = sa.Table('users', FirstDatabase.metadata, autoload=True)
    # autoload=True will try to load table schema automatically 
    # so you don't need to define each column here by hand (but you can)


class Post(FirstDatabase.TableBase):
    __table__ = sa.Table('posts', FirstDatabase.metadata, autoload=True)

    # with explicit relationships GodMode will be able 
    # create an inteface links for between models
    user = relationship('User')
```

That's it. Now let's define some models to use with our database.

### Admin Models

Admin Model is the place where you will spend most of time. Here you can define CRUD-views, 
attach actions, customize widgets, forms and lists. 
Put your models to a [models](models) directory, each to a separate file. Look there for examples.
Let's start with creating a `models/<name_your_model>.py` file.

```python
from godmode.models.base import BaseAdminModel
from database.first_database import FirstDatabase


class FirstAdminModel(BaseAdminModel):
    db = FirstDatabase                      # database class
    table = User                            # table class
    name = "users"                          # name for url path (must be unique)
    # ^ this is actually a minimal setup
    # fields below are used to customize things
    
    acl = ACL.ADMIN                         # lowest ACL group who has access this model
    id_field = "id"                         # primary key field (used is urls too)
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
        "my_custom_field_that_not_in_database"  # <- useful for custom widgets
    ]
    widgets = {                             # custom widget classes for certain fields
        "name": NameWidget,
        "is_locked": BooleanWidget,
        "my_custom_field_that_not_in_database": MyCustomWidget
    }

    # use BaseListView to display this table (default behaviour)
    list_view = BaseListView

    # do not generate create, edit and delete views — now our model is read-only
    edit_view = None
    create_view = None
    delete_view = None

    # you can make your custom details view based on BaseDetailsView
    # for example if you want to use your own template
    class CustomDetailsView(BaseDetailsView):
        template = "views/my_custom_details.html"
        widgets = {...}

    details_view = CustomDetailsView        # see Views section below for more info
```

Now let's go to the [app.py](app.py) file and add the newly defined model to our app.

```python
from models.first_model import FirstAdminModel

app = create_app(
    models=[
        FirstAdminModel,  # put your new models here
    ]
)
```

Now you can run the app and check our your table in the interface.

### Views

Views are web pages. There are five main views in GodMode: create, update, delete, list and details, 
but you can create your own views using inheritance from a BaseView. Here's a full reference of a view object:

```python
from godmode.views.list_view import BaseListView


class MyListView(BaseListView):
    acl = ACL.MODERATOR                     # lowest ACL group who has access to this view
    title = "My List"                       # title for HTML page
    template = "view/ist.html"              # template file for this view
    fields = [...]                          # same as "fields" in model, but specific for this view
    sorting = ["id", "name"]                # fields allowed for sorting (default = None — all fields)
    batch_actions = [MyBatchAction]         # see screenshot above
    object_actions = [MyObjectAction]
    max_per_page = 100
    has_list_delete = True                  # if you have DeleteView but want to hide [x] button from ListView
    default_sorting = text("id desc")       # default ordering, better specify in SQLAlchemy manner: User.id.desc()
    widgets = {
        "name": TextWidget                  # overwrite or append model widgets
    }
```

After creating a view you can attach it to any model like this:

```python
from views.my_list_view import MyListView


class CustomAdminModel(BaseAdminModel):
    # --- required model params ---
    
    list_view = MyListView
```

### Actions

Actions are special scripts that can be executed on one or several records in a table. 
For example, [Ban User](actions/demo_ban_user.py) action — it updates a model with `is_locked=True`.
Batch actions are executed one by one now, so be careful banning 1M users.

```python
from godmode.actions.base import BaseAction


class BanUserAction(BaseAction):
    title = "Ban"
    name = "ban"
    acl = ACL.ADMIN
    enable_log = True

    # defines how to render the form of this action (if it has a form)
    def render_form(self, *args, **kwargs):
        return render_template("actions/button_action.html", url=self.name, button_label="Submit")

    # code triggered with action; kwargs have all request parameters
    # but all you usually need is kwargs["id"] — id of current object
    def do_item_action(self, *args, **kwargs):
        user_id = kwargs.pop("id")
        self.model.update(id=user_id, is_banned=True)
        return render_template("success.html", message="User {} was banned".format(id))
```

Action can be attached to a model using the `actions` field, but usually it makes more sense to use them with a view: 

```python
from actions.ban_user import BanUserAction


class UsersListView(BaseListView):
    title = "User list"
    object_actions = [
        BanUserAction,
    ]
    batch_actions = [
        BanUserAction,
    ]
```

### Widgets

Widgets are powered by a [WTForms](https://github.com/wtforms/wtforms) library for form parsing, validation and rendering.
They are responsible for rendering in all the views — create, list, details, delete.
If you're familiar with WTForms, you have all the superpowers in your hands. Otherwise, check the documentation.

You can also create widgets which are completely independent from WTForms. 
Check out [widgets/polygon.py](widgets/polygon.py) for example.

```python
from godmode.widgets.base import BaseWidget


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

When widget is created, assign it to any field in a model or view:


```python
from widgets.my_widget import MyWidget


class DemoAdminModel(BaseAdminModel):
    # --- required model params ---

    widgets = {
        "name": MyWidget
    }
    
    # --- or using a view ---
    
    class UsersListView(BaseListView):
        widgets = {
            "name": MyWidget  # it will overwrite the standard model widgets
        }
        
    list_view = UsersListView 
```

Feel free to reuse existing widgets from [godmode/widgets](godmode/widgets) directory.


### Groups

Groups allow you to combine models into logical sets in the sidebar.
Models without a group have higher priority and displayed at the top of the sidebar.

```python
from godmode.groups.base import BaseGroup


class MyGroup(BaseGroup):
    acl = ACL.MODERATOR   # you can hide the whole group from users lower than MODERATOR level
    name = "Group name"   # title to display in sidebar
    index = 1000          # higher index -> higher position
```

Here's how to put a model into group:

```python
from groups.my_group import MyGroup


class GroupedAdminModel(BaseAdminModel):
    # --- required model params ---

    group = MyGroup
```

### ACLs

ACLs and their priorities are defined in `common/acl.py` file: `PRIORITY = [SUPERUSER, ADMIN, MODERATOR, ALL]`.
You can create any group for yourself but don't forget to put it into PRIORITY list.

* SUPERUSER is a group of users with highest privileges. They have permission to do everything in GodMode. 
Use carefully. Usually 1 superuser per project is enough.
* ADMINs have all the permissions to edit the databases but they cannot create and manage other GodMode users.
* MODERATORs are read-only users by default. You can hide any models, views, groups and actions from moderators.
* ALL specifies that module is visible even for unauthorized users. It was made for login screen — don't know how it can be useful for you.


## Plans and TODO

- [x] Buy more beer
- [ ] Make deletion action instead of view
- [ ] Get rid of database field in admin models — table is enough
- [ ] Tests? whahaha
- [ ] Fix HTML/CSS bugs (maybe with a redesign)
- [ ] Make Widgets Great Again (+sexy appearance)
- [ ] Support default values from more database drivers
- [ ] Security test for XSS and SQL injections (be careful with that; check all the models you create and send me pull requests)
- [ ] Think about better filtering/sorting interface
- [ ] Make an installation wizard for easier cold start
- [ ] More AJAX for validation and inline editing, probably

## Similar Projects

Other great projects of automatic admin interfaces:

* [Django Admin Module (Python)](https://docs.djangoproject.com/en/dev/ref/contrib/admin/)
* [Flask-Admin (Python)](https://github.com/flask-admin/flask-admin)
* [Sonata Admin Bundle (PHP)](https://github.com/sonata-project/SonataAdminBundle)

## License
(c) vas3k.com

Licensed under the [WTFPL](http://www.wtfpl.net/) license.
Full text of the license can be found in the LICENSE.txt file.

> [vas3k.com](http://vas3k.com) &nbsp;&middot;&nbsp;
> GitHub [@vas3k](https://github.com/vas3k) &nbsp;&middot;&nbsp;
> Twitter [@vas3kcom](https://twitter.com/vas3kcom)
