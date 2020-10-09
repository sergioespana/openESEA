from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Survey, Method
from ..serializers import SurveyOverviewSerializer, SurveyDetailSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyOverviewSerializer

    def get_queryset(self):
        return Survey.objects.filter(
            method__organization=self.kwargs['organization_pk'],
            method__organization__user=self.request.user,
            method=self.kwargs['method_pk'],
        )

    def perform_create(self, serializer):
        method = get_object_or_404(
            Method,
            pk=self.kwargs['method_pk'],
            organization=self.kwargs['organization_pk'],
        )
        serializer.save(method=method)

    def retrieve(self, request, organization_pk, method_pk, pk):
        survey = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = SurveyDetailSerializer(survey)
        return Response(serializer.data)


class PublicSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveyOverviewSerializer
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk):
        survey = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = SurveyDetailSerializer(survey)
        return Response(serializer.data)
