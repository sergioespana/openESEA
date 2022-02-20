from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .survey import Survey
from .survey_audit import SurveyAudit
from .direct_indicator import DirectIndicator
from .question_response import QuestionResponse
import random
import string


class SurveyResponseManager(models.Manager):

    def create(self, survey, respondent, esea_account, token=None):
        # Generates token (if none is provided) which is used to send out the Survey url to a respondent-to-be
        if token is None:
            token = "".join(random.choice(string.ascii_letters) for i in range(10))

        surveyresponse = SurveyResponse(survey=survey, respondent=respondent, esea_account=esea_account, token=token)
        surveyresponse.save()
        return surveyresponse


class SurveyResponse(models.Model):
    objects = SurveyResponseManager()
    survey = models.ForeignKey('Survey', related_name="responses", on_delete=models.CASCADE)
    survey_audit = models.ForeignKey('SurveyAudit', related_name="sample", on_delete=models.SET_NULL, null=True)
    esea_account = models.ForeignKey('EseaAccount', related_name="responses", on_delete=models.CASCADE)
    respondent = models.ForeignKey('Respondent', related_name="response", on_delete=models.CASCADE, null=True)
    auditor = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)

    token = models.CharField(max_length=10)
    finished = models.BooleanField(default=False)
    # verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('survey_response')
        verbose_name_plural = _('survey_responses')
    
    def __str__(self):
        return f"'{self.survey} ({self.respondent})'"

    # Filters question responses based on Indicator ids
    def filter_question_responses(self, question_responses):
        indicator_ids = self.survey.questions.values_list('id', flat=True,)
        return [
            question_response
            for question_response in question_responses
            if question_response['direct_indicator_id'] in indicator_ids
        ]

    # ??
    def save_question_responses(self, question_responses):
        filtered_question_responses = self.filter_question_responses(
            question_responses
        )
        question_response_mapping = {
            question_response.direct_indicator_id: question_response
            for question_response in self.question_responses.all()
        }
        data_mapping = {
            question_response['direct_indicator_id']: question_response
            for question_response in filtered_question_responses
        }

        # Perform creations and updates.
        question_response_list = []
        for id, data in data_mapping.items():
            question_response = question_response_mapping.get(id, None)
            if question_response is None:
                question_response_list.append(self.question_responses.create(**data))    
            else:
                pass
            
        # Perform deletions.
        for id, question_response in question_response_mapping.items():
            if id not in data_mapping:
                question_response.delete()
        return question_response_list



    '''
    - Add Date as an attribute (DateTimeField())
    - Respondent as 1 to 1 field? -->  # respondent = models.OneToOneField('Respondent', related_name="response", on_delete=models.CASCADE, primary_key=False) # , primary_key=True, null=True for now!
    '''
