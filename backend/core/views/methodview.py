from rest_framework.response import Response 
from rest_framework import viewsets, response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from ..models import Method, Organisation, CustomUser, Topic, DirectIndicator, IndirectIndicator, Survey
from ..serializers import MinimalMethodSerializer,  MethodSerializer, SurveyResponseCalculationSerializer
from ..utils import process_yaml_method, process_textual_method, merge_indicators


class MethodViewSet(viewsets.ModelViewSet):
    serializer_class = MethodSerializer
    serializer_action_classes = { 'list': MinimalMethodSerializer }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        mymethods = self.request.GET.get('mymethods', None)
        allmethods = self.request.GET.get('allmethods', None)
        network = self.request.GET.get('network', None)
        organisation = self.request.GET.get('organisation', None)
        excludenetwork = self.request.GET.get('excludenetwork', None)

        if mymethods is not None:
            return Method.objects.filter(created_by=self.request.user)
        if allmethods is not None:
            if self.request.user.is_superuser:
                return Method.objects.all() # 
            else:
                return Method.objects.filter(Q(created_by=self.request.user) | Q(ispublic = True))
        if network is not None:
            return Method.objects.filter(networks=network)
        if excludenetwork is not None:
            return Method.objects.exclude(networks=excludenetwork)
        if organisation is not None:
            return Method.objects.filter(organisations=organisation).distinct()
        
        return Method.objects.all()

    def create(self, request):
        serializer = MethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def indicators(self, request):
        method = self.request.GET.get('method', None)
                # eseaaccount = get_object_or_404(EseaAccount, pk=esea_account_pk)
                # respondents = SurveyResponse.objects.filter(esea_account=esea_account_pk) #Respondent.objects.filter(organisation__esea_accounts=74)
                # # print(respondents)
                # responses = SurveyResponse.objects.filter(esea_account=esea_account_pk, finished=True)

                # question_responses = QuestionResponse.objects.filter(survey_response__esea_account=esea_account_pk, survey_response__finished=True)
                # # print(question_responses)

        indirect_indicators = IndirectIndicator.objects.filter(topic__method=method)
        direct_indicators = DirectIndicator.objects.filter(topic__method=method)
                
        indicators = merge_indicators(direct_indicators, indirect_indicators) #calculate_indicators(indirect_indicators, direct_indicators)                 
        serializer = SurveyResponseCalculationSerializer(indicators.values(), many=True)
        return Response({ "indicators": serializer.data })


@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def upload_method(request):
    print('xxxx')
    if request.method == 'POST':
        if 'file' in request.FILES.keys():
            textfile = request.FILES['file'].readlines()
            method_instance = process_textual_method(textfile, request.user)

            serializer = MinimalMethodSerializer(method_instance)
            return Response(serializer.data)
    return Response({})