from django.db import models
from django.utils.translation import gettext_lazy as _
from .stakeholder_group import StakeholderGroup


class SurveyManager(models.Manager):
    def create(
        self, name, description, anonymous, stakeholder, method, rate=0,
    ):
        stakeholder_group, _ = StakeholderGroup.objects.get_or_create(
            name=stakeholder, method=method,
        )
        survey = Survey(
            name=name,
            description=description,
            rate=rate,
            anonymous=anonymous,
            stakeholder_group=stakeholder_group,
            method=method,
        )
        survey.save()
        return survey


class Survey(models.Model):
    objects = SurveyManager()
    name = models.CharField(max_length=120, unique=False, blank=False)
    description = models.CharField(max_length=45, blank=True)
    rate = models.IntegerField(default=0)
    anonymous = models.BooleanField(null=False)
    questions = models.ManyToManyField("DirectIndicator", blank=True)
    method = models.ForeignKey(
        'Method', related_name="surveys", on_delete=models.CASCADE
    )
    stakeholder_group = models.ForeignKey(
        'StakeholderGroup', related_name="surveys", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')
