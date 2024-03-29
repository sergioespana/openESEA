from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..models import Report
from ..serializers import QuestionSerializer, SurveyResponseCalculationSerializer
from ..utils import audit_data, calculate_scoring_scheme

# class ReportViewSet(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = ReportSerializer

#     def get_queryset(self):
#         return Report.objects.filter(method=self.kwargs['method_pk'])

# Import Respondents for a Survey

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def audit_eseaaccount(request, eseaaccount_pk):
    result = audit_data(eseaaccount_pk, verbose=False, boxplot=False)
    

    if isinstance(result, dict):
        serializer = SurveyResponseCalculationSerializer(result.values(), many=True)
        return Response(serializer.data)
    return Response({'error': result})