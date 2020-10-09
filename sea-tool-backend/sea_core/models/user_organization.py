from django.db import models


class UserOrganization(models.Model):

    user = models.ForeignKey(
        'User', related_name='users', on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        'Organization', related_name='organizations', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [['user', 'organization']]
