from django.db import models
from django.utils.translation import gettext_lazy as _


class StakeholderGroup(models.Model):
    name = models.CharField(max_length=120, unique=False, blank=False)
    method = models.ForeignKey('Method', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('stakeholder_group')
        verbose_name_plural = _('stakeholder_groups')

    def __str__(self):
        return self.name

    def update(self, name):
        self.name = name
        self.save()
        return self
