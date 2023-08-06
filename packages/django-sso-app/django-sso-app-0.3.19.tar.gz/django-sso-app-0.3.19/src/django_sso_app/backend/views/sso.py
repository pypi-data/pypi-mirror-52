import logging
import os

from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

logger = logging.getLogger('backend')

CURRENT_DIR = os.getcwd()


class AuthAPIRoot(APIView):
    """
    Auth API Root
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            return Response({
                'users': reverse('users:list', request=request, *args, **kwargs),
                'groups': reverse('groups:list', request=request, *args, **kwargs),

                'login': reverse('rest_login', request=request, *args, **kwargs),
                'logout': reverse('rest_logout', request=request, *args, **kwargs),
                'subscribe': reverse('rest_register', request=request, *args, **kwargs),
            })
        except:
            logger.exception('Error getting auth-api-root')


# custom views

class WebpackBuiltTemplateView(TemplateView):
    """
    Base built template view
    """
    template_name = "frontend/built.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WebpackBuiltTemplateView, self).get_context_data(*args,
                                                                         **kwargs)
        context['COOKIE_DOMAIN'] = settings.COOKIE_DOMAIN
        context['DJANGO_SSO_DEFAULT_REFERRER'] = settings.DJANGO_SSO_DEFAULT_REFERRER
        return context


class ProfileView(TemplateView):
    template_name = "pages/profile.html"

    def get(self, *args, **kwargs):
        logger.info('Getting profile')
        try:
            return super(ProfileView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting profile')
            raise


class ProfileUpdateView(WebpackBuiltTemplateView):

    def get(self, *args, **kwargs):
        logger.info('Getting profile update')
        try:
            return super(ProfileUpdateView, self).get(*args, **kwargs)
        except:
            logger.exception('Error getting profile update')
            raise
