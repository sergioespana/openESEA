from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import QuestionResponse
from ..serializers import QuestionResponseSerializer2


class QuestionResponseViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionResponseSerializer2

    def get_queryset(self):
        surveyresponse = self.request.GET.get('surveyresponse', None)
        print('check')
        if surveyresponse is not None:
            return QuestionResponse.objects.filter(survey_response=surveyresponse) # self.kwargs['survey_response_pk']

    def retrieve(self, request, organisation_pk, esea_account_pk, pk):
        surveyresponse = get_object_or_404(QuestionResponse, pk=pk)
        serializer = QuestionResponseSerializer2(surveyresponse)
        return Response(serializer.data)
    
    def create(self, request, organisation_pk, esea_account_pk):
        surveyresponse = self.request.GET.get('surveyresponse', None)
        print('check')
        if surveyresponse is not None:
            serializer = QuestionResponseSerializer2(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({'use ?surveyresponse=[the surveyresponse pk] to create new question responses.'})
