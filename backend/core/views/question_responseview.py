from rest_framework import viewsets
from rest_framework.response import Response

from ..models import QuestionResponse
from ..serializers import QuestionResponseSerializer


class QuestionResponseViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionResponseSerializer

    def get_queryset(self):
        print('check')
        return QuestionResponse.objects.filter(survey_response=self.kwargs['survey_response_pk'])