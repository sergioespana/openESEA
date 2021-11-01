from rest_framework import serializers

from ..models import Question, DirectIndicator, AnswerOption
from .answer_option import AnswerOptionSerializer
from .direct_indicator2 import DirectIndicatorSerializer2


class QuestionSerializer(serializers.ModelSerializer):
    uiComponent = serializers.ChoiceField(choices=Question.UI_COMPONENT_TYPES)
    direct_indicator = serializers.PrimaryKeyRelatedField(queryset=DirectIndicator.objects.all(), many=True, required=False)
    section_name = serializers.ReadOnlyField(source='section.title')

    class Meta:
        model = Question
        fields = ['id', 'method', 'topic', 'section', 'section_name', 'order', 'isMandatory', 'name','description', 'instruction', 'uiComponent', 'direct_indicator']
    
    def create(self, validated_data):
        try:
            direct_indicator_data = validated_data.pop('direct_indicator', None)
        except KeyError:
            pass

        question = Question.objects.create(**validated_data)

        # Directly adds direct indicator to a question if it exists
        if direct_indicator_data:
            question.direct_indicator.clear()
            for item in direct_indicator_data:
                question.direct_indicator.add(item)
            question.save()
            
        return question

    # When a question gets updated
    def update(self, instance, validated_data):
        instance.method = validated_data.get('method', instance.method)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.section = validated_data.get('section', instance.section)
        instance.order = validated_data.get('order', instance.order)
        instance.isMandatory = validated_data.get('isMandatory', instance.isMandatory)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.instruction = validated_data.get('instruction', instance.instruction)
        instance.uiComponent = validated_data.get('uiComponent', instance.uiComponent)
        
        # If a direct indicator gets attached to the question it will be added to the question
        if 'direct_indicator' in validated_data:
            instance.direct_indicator.clear()
            for item in validated_data.get('direct_indicator'):
                instance.direct_indicator.add(item)
            instance.save()

        return instance

    # Shows direct indicator that is connected to the question
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        direct_indicator_serializer =  DirectIndicatorSerializer2(instance.direct_indicator, many=True)
        representation['direct_indicator'] = direct_indicator_serializer.data
        return representation

    '''
        TODO: Validation for possible UI Components.
    '''