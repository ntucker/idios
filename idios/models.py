from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import idios

from idios.utils import get_profile_form

try:
    from pinax.apps.account.signals import user_logged_in
except ImportError:
    user_logged_in = None

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ClassProperty(property):
    
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class ProfileBase(models.Model):
    
    # @@@ could be unique=True if subclasses don't inherit a concrete base class
    # @@@ need to look at this more
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_("user"))
    
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        abstract = True
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        if idios.settings.MULTIPLE_PROFILES:
            # @@@ using PK here is kind of ugly. the alternative is to
            # generate a unique slug for each profile, which is tricky
            kwargs = {
                "profile_slug": self.profile_slug,
                "pk": self.pk
            }
        else:
            if idios.settings.USE_USERNAME:
                kwargs = {"username": self.user.username}
            else:
                kwargs = {"pk": self.pk}
        return reverse("profile_detail", kwargs=kwargs)
    
    @classmethod
    def get_form(cls):
        return get_profile_form(cls)
    
    def _default_profile_slug(cls):
        return cls._meta.module_name
    
    profile_slug = ClassProperty(classmethod(_default_profile_slug))



def additional_info_kickstart(sender, **kwargs):
    request = kwargs.get("request")
    request.session["idios_additional_info_kickstart"] = True
if user_logged_in: # protect against Pinax not being available
    user_logged_in.connect(additional_info_kickstart)
