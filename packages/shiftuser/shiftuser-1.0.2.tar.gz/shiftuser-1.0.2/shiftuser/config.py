import os


class UserConfig:
    """
    User config
    Use this class as a mixin in your flask/boiler config. It will add
    all the sensible defaults that you can later override in your concrete
    config implementation.
    """

    # passwords
    PASSLIB_ALGO = 'bcrypt'
    PASSLIB_SCHEMES = ['bcrypt', 'md5_crypt']

    # oauth keys
    USER_OAUTH = {
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

    # jwt
    USER_JWT_SECRET = os.environ.get('APP_USER_JWT_SECRET')
    USER_JWT_ALGO = 'HS256'
    USER_JWT_LIFETIME_SECONDS = 60 * 60 * 24 * 1 # days
    USER_JWT_IMPLEMENTATION = None # string module name
    USER_JWT_LOADER_IMPLEMENTATION = None # string module name

    USER_PUBLIC_PROFILES = False
    USER_ACCOUNTS_REQUIRE_CONFIRMATION = True
    USER_SEND_WELCOME_MESSAGE = True
    USER_BASE_EMAIL_CONFIRM_URL = None
    USER_BASE_PASSWORD_CHANGE_URL = None
    USER_EMAIL_SUBJECTS = {
        'welcome': 'Welcome to our site!',
        'welcome_confirm': 'Welcome,  please activate your account!',
        'email_change': 'Please confirm your new email.',
        'password_change': 'Change your password here.',
    }