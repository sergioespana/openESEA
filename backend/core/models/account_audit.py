from django.db import models

class AccountAudit(models.Model):
    esea_account = models.OneToOneField("EseaAccount", related_name="account_audit", on_delete=models.CASCADE, primary_key=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    auditor = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    
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

    assurance = models.CharField(max_length=100, blank=True, choices=ASSURANCE)

    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    FINISHED = "finished"

    STATUS = (
        (NOT_STARTED, "not started"),
        (IN_PROGRESS, "in progress"),
        (FINISHED, "finished")
    )

    status = models.CharField(max_length=100, blank=False, choices=STATUS, default="not started")

    def __str__(self):
        return f'esea_account: {self.esea_account.organisation} - {self.esea_account.campaign.name}'