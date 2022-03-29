from rest_framework import serializers

from ..models import QuestionResponse


class QuestionResponseSerializer2(serializers.ModelSerializer):

    class Meta:
        model = QuestionResponse
        fields = '__all__'
        extra_kwargs = {'survey_response': {'required': False}}