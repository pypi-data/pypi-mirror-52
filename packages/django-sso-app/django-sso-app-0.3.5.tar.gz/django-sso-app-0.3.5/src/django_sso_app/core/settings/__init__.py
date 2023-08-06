import environ


env = environ.Env()

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (django_sso_app/backend/config/settings/common.py - 4 = django_sso_app/)


READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))
