from . import *


DJANGO_SSO_DEFAULT_CONSUMER_GROUP = env('DJANGO_SSO_DEFAULT_CONSUMER_GROUP', default="users")

DJANGO_SSO_CONSUMER_USERNAME_HEADER = env('DJANGO_SSO_CONSUMER_USERNAME_HEADER',
                                          default='HTTP_X_CONSUMER_USERNAME')
DJANGO_SSO_CONSUMER_GROUPS_HEADER = env('DJANGO_SSO_CONSUMER_GROUPS_HEADER',
                                        default='HTTP_X_CONSUMER_GROUPS')


DJANGO_SSO_DEFAULT_FRONTEND_APP = 'django_sso_app.core.apps.frontend'
DJANGO_SSO_FRONTEND_APP = env('DJANGO_SSO_FRONTEND_APP', default=DJANGO_SSO_DEFAULT_FRONTEND_APP)
DJANGO_SSO_NO_CUSTOM_FRONTEND_APP = (DJANGO_SSO_FRONTEND_APP == DJANGO_SSO_DEFAULT_FRONTEND_APP)

DJANGO_SSO_REQUIRED_PROFILE_FIELDS = ('sso_id', 'sso_rev',
                                      "latitude", "longitude",
                                      "first_name", "last_name",
                                      "description",
                                      "picture",
                                      "birthdate",
                                      "address", "country",
                                      "language",
                                      "is_unsubscribed")

DJANGO_SSO_APP_USER_PROFILE = env('DJANGO_SSO_APP_USER_PROFILE',
                                  default='django_sso_app.core.apps.profiles')  # patch
DJANGO_SSO_APP_USER_PROFILE_MODEL = env('DJANGO_SSO_APP_USER_PROFILE_MODEL',
                                        default=DJANGO_SSO_APP_USER_PROFILE + '.models.Profile')  # patch
DJANGO_SSO_APP_HAS_USER_PROFILE = DJANGO_SSO_APP_USER_PROFILE is not None
