from django.db import models


class Method(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField(default=False)

    organization = models.ForeignKey(
        'Organization', related_name="methods", on_delete=models.CASCADE
    )

    def __repr__(self):
        return (
            f"<Method id='{self.id}' name='{self.name}' "
            f"description='{self.description}' is_public='{self.is_public}' "
            f"organization='{self.organization}'>"
        )
