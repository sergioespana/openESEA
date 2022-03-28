from django.db import models
from django.utils.translation import gettext_lazy as _


class QuestionResponse(models.Model):
    survey_response = models.ForeignKey('SurveyResponse', related_name='question_responses', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name="question_responses", on_delete=models.CASCADE)
    direct_indicator_id = models.IntegerField()
    values = models.ManyToManyField('AnswerOption', related_name="question_responses", blank=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    # Timestamp
    # When the Survey Response.finished == True, create a new QuestionResponse while keeping the old QuestionResponse

    # under_audit = models.BooleanField(default=False)
    
    NOT_UNDER_AUDIT = "Not Under Audit"
    OPEN = "Open"
    AWAITING_DOCUMENTATION = "Awaiting Documentation"
    AWAITING_CORRECTION = "Awaiting Correction"
    VERIFIED = "Verified"
    REJECTED = "Rejected"

    AUDIT_STATUSES = (
        (NOT_UNDER_AUDIT, "Not Under Audit"),
        (OPEN, "Open"),
        (AWAITING_DOCUMENTATION, "Awaiting Documentation"),
        (AWAITING_CORRECTION, "Awaiting Correction"),
        (VERIFIED, "Verified"),
        (REJECTED, "Rejected"),
    )

    auditstatus = models.CharField(max_length=100, blank=True, choices=AUDIT_STATUSES, default="Not Under Audit")

    doc_request_note = models.TextField(max_length=1000, blank=True)
    doc_upload_note = models.TextField(max_length=1000, blank=True)
    note = models.TextField(max_length=1000, blank=True)

    class Meta:
        verbose_name = _('question_response')
        verbose_name_plural = _('question_responses')

    def __str__(self):
        return f"{self.survey_response}, {self.direct_indicator_id}, values: {self.values.all()}"

   

''' Attribute 'Value' should contain Question Response '''
# QuestionResponse.objects.filter(newest=true)