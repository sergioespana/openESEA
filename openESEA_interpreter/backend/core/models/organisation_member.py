from django.db import models


class OrganisationMember(models.Model):
    organisation = models.ForeignKey('Organisation', related_name='teammembers', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', related_name="organisationteams", on_delete=models.CASCADE)
        
    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"

    STATUS_OPTIONS = (
        (PENDING, "pending"),
        (ACCEPTED, "accepted"),
        (DENIED, "denied")
    )
    invitation = models.CharField(max_length=100, blank=False, choices=STATUS_OPTIONS, default=PENDING)

    AUDITOR = 4
    ORGANISATIONADMIN = 3
    ESEAACCOUNTANT = 2
    GUEST = 1

    ROLES = (
        (ORGANISATIONADMIN, 'organisation admin'),
        (ESEAACCOUNTANT, 'esea accountant'),
        (GUEST, "guest"),
        (AUDITOR, "auditor")
    )
    role = models.IntegerField(blank=False, choices=ROLES, default=GUEST)

    def __str__(self):
        return f"{self.organisation.name} - {self.user.username} ({self.get_role_display()})"
