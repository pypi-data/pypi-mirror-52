# -*- coding: utf-8
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from .conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, **kwargs):
    """
    After User.save is called we check to see if it was a created user. If so,
    we check if the User object wants account creation. If all passes we
    create an Account object.
    We only run on user creation to avoid having to check for existence on
    each call to User.save.
    """

    # Disable post_save during manage.py loaddata
    if kwargs.get("raw", False):
        return False

    user, created = kwargs["instance"], kwargs["created"]
    disabled = getattr(user, "_disable_account_creation", not settings.CREATE_PROFILE_ON_SAVE)
    if created and not disabled:
        models.Profile.objects.create(user=user)
