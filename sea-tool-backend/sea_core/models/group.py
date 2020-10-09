from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(max_length=120, unique=False, blank=False)

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name
