from rest_framework import serializers

from ..models import Survey, SurveyResponse, QuestionResponse
from .question_response import QuestionResponseSerializer

import random
import string


class SurveyResponseSerializer(serializers.ModelSerializer):
    question_responses = QuestionResponseSerializer(many=True, required=False)
    respondent = serializers.StringRelatedField()
    organisation = serializers.StringRelatedField(source='respondent.organisation')
    method = serializers.ReadOnlyField(source='survey.method.id')
    survey = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)

    class Meta:
        model = SurveyResponse
        fields = '__all__'
        read_only_fields = ['respondent', 'survey', 'organisation', 'method', 'token']

    # When a Survey Response gets updated
    def update(self, survey_response, validated_data):
        survey_response.finished = validated_data.get('finished', survey_response.finished)
        question_responses = validated_data.pop('question_responses')

        # Updates individual question response objects based on survey response changes
        for item_data in question_responses:
            qr, _ = QuestionResponse.objects.get_or_create(survey_response=survey_response, question=item_data.get('question'), direct_indicator_id=item_data.get('direct_indicator_id'))
            if 'values' in item_data.keys():
                if len(item_data['values']):
                    qr.values.clear()
                    for value in item_data['values']:
                        qr.values.add(value)
            qr.value = item_data.get('value', qr.value)
            qr.save()

        survey_response.save()
        return survey_response


class SurveyResponseCalculationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    topic = serializers.StringRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    key = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    formula = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    calculation = serializers.CharField(read_only=True)
    absolute_weights = serializers.ListField(read_only=True, required=False)
    absolute = serializers.DecimalField(read_only=True, max_digits=None, decimal_places=5)
    scoring_level = serializers.IntegerField(read_only=True, required=False)
    indicator_impact = serializers.DecimalField(read_only=True, max_digits=None, decimal_places=5)
    critical_impact = serializers.BooleanField(read_only=True, required=False)
    outliers = serializers.BooleanField(read_only=True, required=False)
    cut_off_lower_limit =  serializers.StringRelatedField(read_only=True)
    cut_off_upper_limit = serializers.StringRelatedField(read_only=True)
    value = serializers.CharField(read_only=True)
    responses = serializers.ListField(child=serializers.CharField(read_only=True))

# question_responses_dict = dict((i.id, i) for i in survey_response.question_responses.all())