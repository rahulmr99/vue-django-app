"""
copy the file to env.py when you develop locally and want to set the 
per-machine configurations. see config.py for all options available.
"""

# base config
DJANGO_SECRET_KEY = None

# APP_AWS_ACCESS_KEY_ID =
# APP_AWS_SECRET_ACCESS_KEY =


# DB_PASSWORD = ""
RUN_ENV = "local"

# needed only if you use fabric tasks to start services and deploy
# local_username =
# local_password =

base_domain_name = 'http://localhost:8001'

DYNAMO_DB_HOST = 'http://localhost:9000'
