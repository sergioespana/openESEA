from django.db import models

class AccountAudit(models.Model):
    esea_account = models.OneToOneField("EseaAccount", related_name="account_audit", on_delete=models.CASCADE, primary_key=False)
    finished = models.BooleanField(default=False)
    finish_date = models.DateTimeField(blank=True, null=True)

    LIMITED = "limited"
    REASONABLE = "reasonable"
    ASSURANCE_REJECTED = "assurance rejected"
    NO_ASSURANCE = "no assurance"

    ASSURANCE = (
        (LIMITED, "limited"),
        (REASONABLE, "reasonable"),
        (ASSURANCE_REJECTED, "assurance rejected"),
        (NO_ASSURANCE, "no assurance")
    )

    assurance = models.CharField(max_length=100, blank=False, choices=ASSURANCE)