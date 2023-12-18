from django.db import models

class Dashboard(models.Model):
    
    specification = models.JSONField(blank=False)

    def __str__(self):
        return self.specification
