from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from secrets import token_urlsafe
from ..models import (
    SurveyResponse,
    Survey,
    UserOrganization,
    IndirectIndicator,
    QuestionResponse,
    DirectIndicator,
)
from ..serializers import (
    SurveyResponseSerializer,
    SurveyResponseCalculationSerializer,
)
from ..utils import calculate_indicators, map_responses_by_indicator


class SurveyResponseViewset(viewsets.ModelViewSet):
    serializer_class = SurveyResponseSerializer

    def get_queryset(self):
        return SurveyResponse.objects.filter(
            survey__method__organization=self.kwargs["organization_pk"],
            survey__method__organization__user=self.request.user,
            survey__method=self.kwargs["method_pk"],
            survey=self.kwargs["survey_pk"],
        )

    def perform_create(self, serializer):
        user_organization = get_object_or_404(
            UserOrganization,
            user=self.request.user,
            organization=self.kwargs["organization_pk"],
        )
        survey = get_object_or_404(Survey, pk=self.kwargs["survey_pk"])
        serializer.save(survey=survey, user_organization=user_organization)

    @action(detail=False, methods=["get"])
    def all(self, request, organization_pk, method_pk, survey_pk):
        all_respondents = SurveyResponse.objects.filter(
            survey__method=method_pk, survey=survey_pk,
        )
        question_responses = QuestionResponse.objects.filter(
            survey_response__survey__method=method_pk,
            survey_response__survey=survey_pk,
            survey_response__finished=True,
        )
        indirect_indicators = IndirectIndicator.objects.filter(
            topic__method=method_pk,
        )
        direct_indicators = DirectIndicator.objects.filter(survey=survey_pk,)

        map_responses_by_indicator(
            direct_indicators, question_responses,
        )
        indicators = calculate_indicators(
            indirect_indicators, direct_indicators,
        )
        serializer = SurveyResponseCalculationSerializer(
            indicators.values(), many=True
        )

        return Response(
            {
                "all_respondents": len(all_respondents),
                "respondents": len(all_respondents.filter(finished=True)),
                "indicators": serializer.data,
            }
        )

    @action(detail=True, methods=["get"])
    def calculations(self, request, organization_pk, method_pk, survey_pk, pk):
        survey_response = get_object_or_404(self.get_queryset(), pk=pk)
        indirect_indicators = IndirectIndicator.objects.filter(
            topic__method=method_pk,
        )
        direct_indicators = survey_response.survey.questions.all()
        question_responses = survey_response.question_responses.all()

        map_responses_by_indicator(
            direct_indicators, question_responses,
        )
        indicators = calculate_indicators(
            indirect_indicators, direct_indicators,
        )
        serializer = SurveyResponseCalculationSerializer(
            indicators.values(), many=True
        )
        return Response(serializer.data)


class PublicSurveyResponseViewset(viewsets.ModelViewSet):
    serializer_class = SurveyResponseSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        token = self.request.query_params.get("token")
        return SurveyResponse.objects.filter(
            survey=self.kwargs["survey_pk"],
            user_organization=None,
            token=token,
        )

    def perform_create(self, serializer):
        token = self.request.query_params.get("token", token_urlsafe())
        survey = get_object_or_404(Survey, pk=self.kwargs["survey_pk"])
        serializer.save(survey=survey, token=token)
