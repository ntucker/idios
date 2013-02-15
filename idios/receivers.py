from django.db.models.signals import post_save
from django.contrib.auth.models import User

from idios.utils import get_profile_model

def create_profile(sender, instance=None, **kwargs):
    if instance is None or kwargs.get('raw', False) or not kwargs.get('created', True):
        return
    profile, created = get_profile_model().objects.get_or_create(user=instance)
post_save.connect(create_profile, sender=User)
