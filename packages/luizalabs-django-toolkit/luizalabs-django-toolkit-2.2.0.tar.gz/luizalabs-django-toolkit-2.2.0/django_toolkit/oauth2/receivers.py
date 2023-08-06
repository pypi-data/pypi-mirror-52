# -*- coding: utf-8 -*-
from django.core.cache import caches
from django.db.models.signals import post_delete
from django.dispatch import receiver
from oauth2_provider.models import get_access_token_model

from django_toolkit import toolkit_settings

cache = caches[toolkit_settings.ACCESS_TOKEN_CACHE_BACKEND]
AccessToken = get_access_token_model()


@receiver(post_delete, sender=AccessToken)
def invalidate_token_cache(sender, instance, **kwargs):
    cache.delete(instance.token)
