# shift-user
A [shiftboiler](https://github.com/projectshift/shift-boiler) project skeleton extension providing user registration and [authentication](https://flask-login.readthedocs.io/en/latest/) including [OAuth](https://pythonhosted.org/Flask-OAuth/) support for facebook, google vk, instagram and linkedin.
Provides support for RBAC and access control with [Principal](http://pythonhosted.org/Flask-Principal/)


## Requirements

You will need to have  shiftboiler installed and an initialized project skeleton with following feature enabled:

  * ORM
  * Routing
  * Mail


## Installation

### get the package

You can install the package wrom PyPI:

```
pip install shiftuser
```

### enabling user feature
To enable the feature run the code below at bootstrap time passing it an instance
of you flask application

```python
from shiftuser.feature import user_feature
user_feature(app)
```

There is a lot to user feature - it provides facilities to create and manage user profiles, authenticate with username, passwords and oauth, manage user profiles, reset passwords, confirm and activate accounts and a handy set of console commands for your cli to perform admin tasks.

### user cli
To connect user commands to your project CLI edit cli file in your project root and mount the commands:

```python
from shiftuser.cli import user_cli
cli.add_command(user_cli, name='user')
```

### migrations
If you are using Alembic migrations, make sure to import user models in `migrations/env.py`:

```python
# using boiler users?
from shiftuser import models
```

### routes and views
Shiftuser provides extendible default implementation for a lot of register, login, OAuth and profile functionality. You can see everything in the [`urls.py`](https://github.com/projectshift/shift-user/blob/master/shiftuser/urls.py) file. You are free to selectively enable what you will be using, or simply import everything that is provided: 

```python
from shiftuser.urls import user_urls
urls = dict()
urls.update(user_urls)
```

You can use base implementation and re-configure it or even do your own implementation:

```python
from shiftuser.views import Login

class MyCustomLogin(Login):
    invalid_message = 'This is not a correct set of credentials'
    template = 'custom-login.j2'
```


## Configuration

Shiftuser provides a base Config mixin that you can use with your own application configs. Extending from it will provide a set of sensible defaults that you can override in your concrete config implementations:

```python
from shiftuser.config import UserConfig

class MyConfig(UserConfig):
    USER_PUBLIC_PROFILES = False
    USER_ACCOUNTS_REQUIRE_CONFIRMATION = True
    USER_SEND_WELCOME_MESSAGE = True
```

Here is the full list of configuration options:

| **Setting** | **Default** | **Description** |
|---|---|---|
| `PASSLIB_ALGO` | `bcrypt` | Passwords encryption algorithm supported by [Passlib](https://passlib.readthedocs.io/en/stable/) |
| `PASSLIB_SCHEMES` | `['bcrypt', 'md5_crypt']` | A list of supported password encryption algorithms |
| `USER_JWT_SECRET` | `None` | This typically will come from an environment variable called `APP_USER_JWT_SECRET` |
| `USER_JWT_ALGO` | `HS256` | JWT encryption algorithm |
| `USER_JWT_LIFETIME_SECONDS` | `86400` | JWT lifetime in seconds |
| `USER_JWT_IMPLEMENTATION` | `None` | Importable string module name to replace JWT default token implementation |
| `USER_JWT_LOADER_IMPLEMENTATION` | `None` | Importable string module name to replace default JWT token loader|
| `USER_PUBLIC_PROFILES` | `False` | Wether to allow user profile pages to be publicly accessible |
| `USER_ACCOUNTS_REQUIRE_CONFIRMATION` | `True` | Whether new users have to confirm their email addresses |
| `USER_SEND_WELCOME_MESSAGE` | `True` | Whether to send welcome message to new users |
| `USER_BASE_EMAIL_CONFIRM_URL` | `None` | Allows to override base URL for email confirmation links. This is helpful when the app/API and the frontend are on different domains |
| `USER_BASE_PASSWORD_CHANGE_URL` | `None` | Allows to override base URL for password reset links. This is helpful when the app/API and the frontend are on different domains |

### User email subjects

Configuration contains a `USER_EMAIL_SUBJECTS` dict that you can modify to override to set what your transactional email subjects will be:

```python
{
  'welcome': 'Welcome to our site!',
  'welcome_confirm': 'Welcome,  please activate your account!',
  'email_change': 'Please confirm your new email.',
  'password_change': 'Change your password here.',
}
```

### OAuth application keys

Shiftuser out of the box supports OAuth with several popular providers. For each provider you would like to use, you must register an OAuth app and get application ID and application secret.

The config contains a dict with all the supported provides where you can put your keys:

```python
{
  'facebook': {
    'id': 'app-id',
    'secret': 'app-seceret',
    'scope': 'email',
  },
  'vkontakte': {
    'id': 'app-id',
    'secret': 'service-access-key',
    'scope': 'email',
    'offline': True
  },
  'google': {
    'id': 'app-id',
    'secret': 'app-secret',
    'scope': 'email',
    'offline': True
  },
  'instagram': {
    'id': 'app-id',
    'secret': 'app-secret',
    'scope': 'basic'
  },
}
```


