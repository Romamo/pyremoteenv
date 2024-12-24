import io
import os

import remoteenv

# Extend local .env with remote
# Check original example https://github.com/joke2k/django-environ

try:
    import environ
except ImportError:
    raise Exception("The 'django-environ' library is required to run this example. "
                    "Install it with 'pip install django-environ'")

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Take environment variables from remote env config
remote_env = remoteenv.Env('zk')
with remote_env:
    with io.StringIO() as buffer:
        remote_env.read_to_file(file=buffer)
        environ.Env.read_env(buffer, overwrite=True)

# False if not in os.environ because of casting above
DEBUG = env('DEBUG')
