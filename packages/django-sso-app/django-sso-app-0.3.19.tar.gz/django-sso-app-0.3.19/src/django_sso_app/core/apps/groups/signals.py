import logging

from django.conf import settings
from django.contrib.auth.models import Group as GroupModel
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Group
from ..api_gateway.functions import create_consumer_acl, delete_consumer_acl

logger = logging.getLogger('groups')


def create_user_group(user, group):
    logger.info('creating user group {} for {}'.format(group, user))
    if settings.DJANGO_SSO_BACKEND_ENABLED and not settings.TESTING_MODE:
        status_code, resp = create_consumer_acl(user, group.name)
        print('CREATED', status_code, resp)
        return True
    return False


def delete_user_group(user, group):
    logger.info('deleting user group {} for {}'.format(group, user))
    if settings.DJANGO_SSO_BACKEND_ENABLED and settings.DJANGO_SSO_BACKEND_ENABLED and not settings.TESTING_MODE:
        status_code, resp = delete_consumer_acl(user, group.name)
        print('DELETED', status_code)
        return True
    return False


@receiver(m2m_changed)
def signal_handler_when_user_is_added_or_removed_from_group(action, instance, pk_set, model, **kwargs):
    if model == GroupModel:
        user = instance
        user_updated = False
        if action == 'pre_add':
            for pk in pk_set:
                group = Group.objects.get(id=pk)
                user_updated = create_user_group(user, group)
        elif action == 'pre_remove':
            for pk in pk_set:
                group = Group.objects.get(id=pk)
                user_updated = delete_user_group(user, group)
        if user_updated:
            user.update_rev(True)
