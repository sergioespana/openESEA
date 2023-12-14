from django.db import models

class SurveyAudit(models.Model):
    account_audit = models.ForeignKey('AccountAudit', related_name="survey_audits", on_delete=models.CASCADE)
    survey = models.ForeignKey('Survey', related_name="survey_audits", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    sample_size = models.IntegerField(blank=True, null=True)
    

    NOT_STARTED = "not started"

    # single
    QUESTION_SELECTION = "question selection"
    DOCUMENTATION_UPLOAD = "documentation upload"
    
    # multiple
    RESPONSE_SAMPLE = "response sample"
    SAMPLE_OVERVIEW = "sample overview"

    AUDIT_IN_PROGRESS = "audit progress"

    VERIFIED = "verified"
    REJECTED = "rejected"    

    STATUS = (
        (NOT_STARTED, "not started"),
        (QUESTION_SELECTION, "question selection"),
        (DOCUMENTATION_UPLOAD, "documentation upload"),
        (RESPONSE_SAMPLE, "response sample"),
        (SAMPLE_OVERVIEW, "sample overview"),
        (AUDIT_IN_PROGRESS, "audit progress"),
        (VERIFIED, "verified"),
        (REJECTED, "rejected")
    )

    status = models.CharField(max_length=100, blank=False, choices=STATUS, default="not started")


    def __str__(self):
        return f'esea_account: {self.account_audit.esea_account} - survey: {self.survey.name}'





# list of sampled respondents
# verified boolean