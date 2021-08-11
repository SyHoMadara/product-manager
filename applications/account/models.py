from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # user properties
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True,blank=True, null=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True)
    home_number = PhoneNumberField(_('home telephone'),blank=True, null=True)
    fax_number = PhoneNumberField(_('fax number'),blank=True, null=True)
    deleted = models.BooleanField(_('deleted'), default=False)

    # settings
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    hide_email = models.BooleanField(default=True)
    hide_phone_number = models.BooleanField(default=True)

    # methods
    def __str__(self):
        return self.username

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
