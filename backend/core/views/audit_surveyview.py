from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_backend.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

import math

from ..models import SurveyAudit, SurveyResponse
from ..serializers import SurveyAuditSerializer, RespondentSerializer


class SurveyAuditViewSet(viewsets.ModelViewSet):
    serializer_class=SurveyAuditSerializer
    
    def get_queryset(self):
        # campaign = self.request.GET.get('campaign', None)
        # audit_selection = self.request.GET.get('audit-selection', None)
        # if campaign is not None and audit_selection is not None:
        #     return SurveyAudit.objects.filter(esea_account__campaign=campaign, status__in=['in progress', 'finished'])
        return SurveyAudit.objects.filter(account_audit__esea_account=self.kwargs['esea_account_pk'])
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        serializer = SurveyAuditSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
@permission_classes((AllowAny, ))
def sample_survey_responses(request, eseaaccount_pk, survey_pk):

    # if survey_audit_object has no sample yet.
    if 'sample_size_fixed' or 'sample_size_percentage' in request.data.keys():
        Responses = SurveyResponse.objects.filter(esea_account=eseaaccount_pk, survey=survey_pk)
        respondents = [response.respondent for response in Responses]

        random_responses = []

        if 'sample_size_fixed' in request.data.keys():
            integer_number = request.data['sample_size_fixed']
            random_responses = Responses.order_by('?')[:integer_number]
        if 'sample_size_percentage' in request.data.keys():
            integer_number = math.ceil(len(Responses) * (request.data['sample_size_percentage']/100))
            random_responses = Responses.order_by('?')[:integer_number]
         
        survey_audit = SurveyAudit.objects.get(account_audit__esea_account=eseaaccount_pk, survey=survey_pk)
        survey_audit.sample_size = integer_number
        survey_audit.save()

        survey_audit.sample.clear()

        for response in random_responses:
            response.survey_audit = survey_audit
            response.save()
        
        print(survey_audit.sample.all())
        serializer = RespondentSerializer(respondents, many=True)

        return Response(serializer.data)
    return Response({ "error" })


@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_audit_emails(request, eseaaccount_pk, survey_pk):
    if 'respondents' in request.data.keys():
        # queryset of survey_audit.samples
        sampled_responses = SurveyResponse.objects.filter(esea_account=eseaaccount_pk, survey=survey_pk, respondent__in=request.data['respondents'])

        subject = f"Multiple Respondent Survey Verification - ESEA"
        
        recepient = "seriousdeejay@gmail.com"
        respondents = []
        

        try:
            for response in sampled_responses:
                respondents.append(response.respondent)
                message = f"Please verify that the following are your responses. http://localhost:8080/survey-fill/{response.token} or https://esea.herokuapp.com/survey-fill/{response.token}"
                # recepient = response.respondent.email
                try:
                    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                    
                    print(response.respondent)
                    print(response.survey.response_type)

                    response.succesfully_emailed
                except:
                    response.succesfuly_email = False

                break

            print(sampled_responses, request.data, eseaaccount_pk, survey_pk)
            serializer = RespondentSerializer(respondents, many=True)
            return Response(serializer.data)
        except:
            return Response({ "Could not send e-mails." })