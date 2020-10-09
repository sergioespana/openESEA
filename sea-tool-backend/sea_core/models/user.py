from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name_prefix = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    registered_on = models.DateTimeField(default=now, editable=False)
    organizations = models.ManyToManyField(
        'Organization', through='UserOrganization'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if not self.last_name_prefix:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.last_name_prefix} {self.last_name}"
