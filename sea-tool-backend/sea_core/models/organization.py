from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(blank=True)
    image = models.ImageField(
        blank=True,
        upload_to="organization/",
        default='organization/default.png',
    )
    users = models.ManyToManyField('User', through='UserOrganization')

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
