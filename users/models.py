from django.db import models
from django.utils import timezone
from django.utils.translation import *
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group


# Create your models here.

class DuplicateUser(AbstractBaseUser):

    password = None
    last_login = None
    caps_token = models.CharField(max_length=70,blank=True)
    caps_id = models.IntegerField(
        verbose_name=ugettext_lazy("CAPS ID"),
        unique=True,
    )
    phone_number = PhoneNumberField(
        verbose_name=ugettext_lazy("Phone number"),
        null=True,
        blank=True,
    )
    email = models.CharField(
        verbose_name=ugettext_lazy("Email"),
        null=True,
        blank=True,
        max_length=63,
    )
    first_name = models.CharField(
        verbose_name=ugettext_lazy("First name"),
        null=True,
        blank=True,
        max_length=63,
    )
    last_name = models.CharField(
        verbose_name=ugettext_lazy("Last name"),
        null=True,
        blank=True,
        max_length=63,
    )
    avatar = models.URLField(
        verbose_name=ugettext_lazy("Avatar"),
        null=True,
        blank=True,
    )
    thumbnail = models.URLField(
        verbose_name=ugettext_lazy("Thumbnail"),
        null=True,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name=ugettext_lazy("Birthday"),
        null=True,
        blank=True,
    )
    last_seen = models.DateTimeField(
        verbose_name=ugettext_lazy("Last seen"),
        default=timezone.now,
    )
    gender = models.IntegerField(
        verbose_name=ugettext_lazy("Gender"),
        default=0,
    )
    is_manager = models.BooleanField(
        verbose_name=ugettext_lazy("Is manager"),
        default=False,
    )
    created = models.DateTimeField(
        verbose_name=ugettext_lazy("Created"),
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name=ugettext_lazy("Updated"),
        auto_now=True,
    )

    USERNAME_FIELD = 'caps_id'

    class Meta:

        ordering = ('-created',)
        verbose_name = ugettext_lazy('User')
        verbose_name_plural = ugettext_lazy('Users')

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.pk)
