from flask_login import LoginManager
from flask_principal import Principal
from flask_oauthlib.client import OAuth

from shiftuser.role_service import RoleService
from shiftuser.user_service import UserService

# instantiate user services (bootstrapped later by user feature)
login_manager = LoginManager()
oauth = OAuth()
principal = Principal()
role_service = RoleService()
user_service = UserService()

