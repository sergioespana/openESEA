from rest_framework import serializers
from ..models import SurveyResponse
from .question_response import QuestionResponseSerializer


class SurveyResponseSerializer(serializers.ModelSerializer):
    question_responses = QuestionResponseSerializer(many=True)

    class Meta:
        model = SurveyResponse
        fields = "__all__"
        read_only_fields = ["survey", "user_organization", "token"]

    def create(self, validated_data):
        question_responses = validated_data.pop("question_responses")
        survey_response = SurveyResponse.objects.create(**validated_data)
        survey_response.save_question_responses(question_responses)
        return survey_response

    def update(self, survey_response, validated_data):
        survey_response.finished = validated_data.get(
            "finished", survey_response.finished,
        )
        survey_response.save()
        question_responses = validated_data.get("question_responses", [])
        survey_response.save_question_responses(question_responses)
        return survey_response


class SurveyResponseCalculationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    topic = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    key = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    formula = serializers.CharField(read_only=True)
    calculation = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)
    responses = serializers.ListField(
        child=serializers.CharField(read_only=True)
    )
