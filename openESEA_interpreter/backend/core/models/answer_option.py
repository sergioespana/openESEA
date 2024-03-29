#Hallo, first try of GIT collab.
from django.db import models
from django.utils.translation import gettext_lazy as _


class AnswerOption(models.Model):
    direct_indicator = models.ManyToManyField('DirectIndicator', blank=True, related_name="options") 
    order = models.IntegerField(default=1)
    text = models.CharField(max_length=255, blank=False)

#push comments through
    def __str__(self):
        return f"{self.text}"

    def __repr__(self):
        return (f"text='{self.text} '")