from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from secrets import token_urlsafe

from ..models import (Survey, SurveyResponse, QuestionResponse, DirectIndicator, IndirectIndicator, Respondent, StakeholderGroup, EseaAccount)
from ..serializers import (SurveyResponseSerializer, QuestionResponseSerializer, SurveyResponseCalculationSerializer)
from ..utils import map_responses_by_indicator, calculate_indicators


class BaseModelViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = ''
    permission_classes = (AllowAny,)

    # Refer to https://stackoverflow.com/a/35987077/1677041
    permission_classes_by_action = {
        'create': permission_classes,
        'list': permission_classes,
        'retrieve': permission_classes,
        'update': permission_classes,
        'destroy': permission_classes,
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get('permission_classes')
            else:
                permission_classes = None

            return [permission() for permission in (permission_classes or self.permission_classes)]


class SurveyResponseViewSet(BaseModelViewSet):
    serializer_class = SurveyResponseSerializer
    lookup_field = 'token'
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'update': (AllowAny,),
        'destroy': (IsAuthenticated,),
        'all': (AllowAny,)
    }
    permission_classes = [AllowAny,]            
    
    # http://localhost:8000/organisations/3/esea-accounts/20/responses/
    # htp://localhost:8000/organisations/3/esea-accounts/20/surveys/6/responses/0/

    def get_queryset(self):
        return SurveyResponse.objects.filter(esea_account=self.kwargs['esea_account_pk']) # finished=False
        
    def retrieve(self, request, organisation_pk, esea_account_pk, token):
        # Get Accountant response that belongs to an Survey & Esea Account
        ## SurveyResponse, survey=survey_pk, esea_account=esea_account_pk
        if 'survey' in token:
            token = token.replace('survey=', '')
            try : 
                token = int(token)
                surveyresponse = get_object_or_404(SurveyResponse, survey=token, esea_account=esea_account_pk)
            except ValueError  :
                print("This string doesn't contain an integer")
                return HttpResponse(status=400)
        
        # Get Response by PK
        elif token.isnumeric():
            surveyresponse = get_object_or_404(SurveyResponse, pk=token)

        # Get Response by unique token (multiple respondent responses)
        else:
            surveyresponse = get_object_or_404(SurveyResponse, token=token)
        serializer = SurveyResponseSerializer(surveyresponse)
        return Response(serializer.data)
    
    def update(self, request, organisation_pk, esea_account_pk, token):
        # Bit of a hack to check whether a survey response is single or multi-respondent
        if token.isnumeric():
            surveyresponse = get_object_or_404(SurveyResponse, pk=token)
            # surveyresponse = get_object_or_404(SurveyResponse, survey=token, esea_account=esea_account_pk)
        else:
            surveyresponse = get_object_or_404(SurveyResponse, token=token)
        serializer = SurveyResponseSerializer(surveyresponse, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, organisation_pk, esea_account_pk, token):
        instance = get_object_or_404(SurveyResponse, pk=token)
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    # Shows all responses belonging to an ESEA Account
    @action(detail=False, methods=['get'])
    def all(self, request, organisation_pk, esea_account_pk):
        if True: #self.request.user.is_authenticated:
            eseaaccount = get_object_or_404(EseaAccount, pk=esea_account_pk)
            respondents = SurveyResponse.objects.filter(esea_account=esea_account_pk) #Respondent.objects.filter(organisation__esea_accounts=74)
            responses = SurveyResponse.objects.filter(esea_account=esea_account_pk, finished=True)

            question_responses = QuestionResponse.objects.filter(survey_response__esea_account=esea_account_pk, survey_response__finished=True)

            indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
            direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)

            # for direct_indicator in direct_indicators:
            #     direct_indicator.filter_responses(question_responses)
            # for item in question_responses:
            #     s = QuestionResponseSerializer(item, many=True)
          
            map_responses_by_indicator(direct_indicators, question_responses)
            indicators = calculate_indicators(indirect_indicators, direct_indicators)

            # for indicator in indicators.values():
            #     print('----->',  indicator)

            serializer = SurveyResponseCalculationSerializer(indicators.values(), many=True)
            return Response(
                {
                    "respondents": len(respondents),
                    "responses": len(responses.filter(finished=True)),
                    #"indics": [i.value for i in indicators.values()],
                    "indicators": serializer.data,
                    
                }
            )
        return Response({})

    @action(detail=True, methods=["get"])
    def calculations(self, request, organization_pk, method_pk, survey_pk, pk):
        survey_response = get_object_or_404(self.get_queryset(), pk=pk)
        indirect_indicators = IndirectIndicator.objects.filter(topic__method=method_pk)
        direct_indicators = survey_response.survey.questions.all()
        question_responses = survey_response.question_responses.all()
        
        map_responses_by_indicator(direct_indicators, question_responses)
        indicators = calculate_indicators(indirect_indicators, direct_indicators)
        serializer = SurveyResponseCalculationSerializer(indicators.values(), many=True)

        return Response(serializer.data)

    # def create_df(self, request, organisation_pk, esea_account_pk):
    #    /survey-responses/create_df/
    #    audit-data.py (=script file)
    # call script to create df from database values