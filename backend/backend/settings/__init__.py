try:
    from backend.config import CONFIG
except Exception as ex:
    print(str(ex))
    print('You have two options: '
          '1. Set the environment variables. '
          '2. Create backend/env.py with variable names needed.')
environment = CONFIG.RUN_ENV

exec(f'from .env.{environment} import *')
from .debug_settings import *
