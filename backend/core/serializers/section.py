from rest_framework import serializers

from ..models import Section, Question
from .text_fragment import TextFragmentSerializer
from .question import QuestionSerializer


class SectionSerializer(serializers.ModelSerializer):
    questions = serializers.ReadOnlyField()
    text_fragments = TextFragmentSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'survey', 'order', 'title', 'questions', 'text_fragments']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        question_serializer = QuestionSerializer(instance.questions, many=True)
        representation['questions'] = question_serializer.data
        return representation