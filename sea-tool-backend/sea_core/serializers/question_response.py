from rest_framework import serializers
from ..models import QuestionResponse


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ['direct_indicator_id', 'value']
