from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    # user properties
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=14, null=True, blank=True)

    # settings
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    hide_email = models.BooleanField(default=True)
    hide_phone_number = models.BooleanField(default=True)
    hide_image_profile = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    registered_google_account = models.BooleanField(default=False, null=True, blank=True)

    # methods
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
