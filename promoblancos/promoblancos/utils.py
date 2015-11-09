from django.core.exceptions import ImproperlyConfigured
import os


def get_env_variable(var_name):
    """Get the enviroment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s enviroment variable" % var_name
        raise ImproperlyConfigured(error_msg)
