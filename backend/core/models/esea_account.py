from django.db import models
from django.shortcuts import get_object_or_404
from datetime import date

from core.models.survey_audit import SurveyAudit

from .respondent import Respondent
from .survey_response import SurveyResponse
from .question import Question



class EseaAccount(models.Model):
    method = models.ForeignKey("Method", on_delete=models.CASCADE)
    organisation = models.ForeignKey("Organisation", related_name="esea_accounts", on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', related_name="organisation_accounts", on_delete=models.CASCADE, null=True)

    year = models.IntegerField(default=date.today().year)
    deployed_to_respondents = models.BooleanField(default=False)
    sufficient_responses = models.BooleanField(default=False)      # Could be replaced by status enum with 'sufficient, unsufficient, ongoing, overdue, etc.'
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    verified_surveys = models.ManyToManyField('Survey', related_name="verified_surveys", blank=True)
    # auditor = 

    def __str__(self):
        return f'organisation:{self.organisation} - campaign:{self.campaign}'
    
    @property
    def network(self):
        if self.campaign:
            return self.campaign.network
        return None

    # Shows list of additional information about the ESEA Account
    def survey_response_by_survey(self):
        arr = []
        for survey in self.method.surveys.all():
            tempdict = {'id': survey.id, 'name': survey.name, 'questions': len([q for q in Question.objects.filter(section__survey=survey)]), 'stakeholdergroup': str(survey.stakeholdergroup), 'type': survey.response_type}
            if len(self.responses.filter(survey=survey)):
                tempdict['auditor'] = self.responses.filter(survey=survey).first().auditor
            else:
                tempdict['auditor'] = None
            try:
                survey_audit = SurveyAudit.objects.filter(survey=survey, account_audit__esea_account=self).first()
                print(survey_audit)
                if survey_audit:
                    tempdict['survey_audit'] = survey_audit.id
            except SurveyAudit.DoesNotExist:
                tempdict['survey_audit'] = None
            tempdict['respondees'] = [{'name':str(respondee)} for respondee in Respondent.objects.filter(response__esea_account=self, response__survey=survey).distinct()]
            tempdict['responses'] = len(self.responses.filter(survey=survey, finished=True))
            tempdict['required_response_rate'] = survey.min_threshold
            tempdict['current_response_rate'] = int((tempdict['responses'])/(len((tempdict['respondees'])) or 1) * 100)
            tempdict['sufficient_responses'] = tempdict['current_response_rate'] >= tempdict['required_response_rate']
            arr.append(tempdict)
        responserates = [item['current_response_rate'] for item in arr if len(item['respondees']) > 0]
        self.response_rate = (sum(responserates)/(len(responserates) or 1))
        
        for survey in arr:
            if survey['type'] == 'multi' and not len(survey['respondees']):
                return arr
        self.deployed_to_respondents = True

        for survey in arr:
            if (survey['sufficient_responses'] == False):
                return arr
        self.sufficient_responses = True
        return arr

    def all_respondents(self):
        respondents = len(Respondent.objects.filter(response__esea_account=self))            
        return respondents

    def all_responses(self):
        responses = SurveyResponse.objects.filter(esea_account=self, finished=True)
        return responses