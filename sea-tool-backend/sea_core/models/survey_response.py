from django.db import models
from django.utils.translation import gettext_lazy as _


class SurveyResponse(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    user_organization = models.ForeignKey(
        'UserOrganization',
        related_name="survey_responses",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    token = models.CharField(max_length=128, blank=True, null=True)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('survey_response')
        verbose_name_plural = _('survey_responses')

    def filter_question_responses(self, question_responses):
        indicator_ids = self.survey.questions.values_list('id', flat=True,)
        return [
            question_response
            for question_response in question_responses
            if question_response['direct_indicator_id'] in indicator_ids
        ]

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
                question_response_list.append(
                    self.question_responses.create(**data)
                )
            elif question_response.value is not data['value']:
                question_response.value = data['value']
                question_response.save()
                question_response_list.append(question_response)

        # Perform deletions.
        for id, question_response in question_response_mapping.items():
            if id not in data_mapping:
                question_response.delete()
        return question_response_list
