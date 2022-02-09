import os
from typing import Any

env_module = {}

try:
    from backend import env as env_module
except Exception as ex:
    print("backend/env.py is not found. Getting variables from environment.", ex)

UNDEFINED = '~~undefined'


class _Env(object):
    def __init__(self, default: Any = UNDEFINED):
        """if not given a default explicitly then this will raise an error."""
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        """
            Get the given environment variable in followind order
            1. os.environment
            2. env.py
            3. default value
        """

        if self.name in os.environ:
            return os.environ[self.name]
        if env_module and hasattr(env_module, self.name):
            return getattr(env_module, self.name)
        if self.default != UNDEFINED:
            return self.default

        raise Exception(f"Failed to get {self.name} variable from os.environ/env.py")


class CONFIG(object):
    """singleton to be used for configuring from os.environ and env.py"""
    # default settings
    DB_NAME = _Env("easybookingdb")
    DB_HOST = _Env('127.0.0.1')
    DB_PORT = _Env('3306')
    DB_USER_NAME = _Env("root")
    RUN_ENV = _Env("production")
    base_domain_name = _Env("https://secure.bookedfusion.com")

    # must be set explicitly
    DB_PASSWORD = _Env()
    DJANGO_SECRET_KEY = _Env()

    # AWS environment variables should not be overridden
    # see https://github.com/Miserlou/Zappa/issues/984#issuecomment-313789220
    APP_AWS_ACCESS_KEY_ID = _Env()
    APP_AWS_SECRET_ACCESS_KEY = _Env()
    REGION_NAME = _Env('us-east-1')

    DYNAMO_DB_HOST = _Env(None)
    '''on local machine and during tests use this to set dynalite or dynamodb local server'''
    
    # useful only on development
    local_username = _Env("root")
    local_password = _Env("root")


if __name__ == '__main__':
    print(CONFIG.__dict__)
