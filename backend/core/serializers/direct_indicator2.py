from rest_framework import serializers

from ..models import DirectIndicator, Topic, AnswerOption
from .answer_option import AnswerOptionSerializer


class DirectIndicatorSerializer2(serializers.ModelSerializer):
    datatype= serializers.ChoiceField(choices=DirectIndicator.DATA_TYPES, required=False)
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), required=False, allow_null=True)
    method_name = serializers.ReadOnlyField(source='method.name')
    question_name = serializers.ReadOnlyField()
    options = AnswerOptionSerializer(many=True, required=False)
    
    class Meta:
        model = DirectIndicator
        fields = [
            'id',
            'method',
            'method_name',
            'key', 
            'name', 
            'question',
            'question_name', 
            'description', 
            'topic', 
            'datatype', 
            'pre_unit', 
            'post_unit',
            'cut_off_lower_limit',
            'cut_off_upper_limit',
            'options'
            ]

    def create(self, validated_data):
        # DirectIndicator refers to direct_indicator model (see __init__.py). DirectIndicator.object.create refers to create function in the model.
        D = DirectIndicator.objects.create(**validated_data)

        # If the Direct Indicator has any options these will be saved
        if validated_data.get('options') is not None:
            options = validated_data.pop('options')

            for option in options:
                option_instance, _ = AnswerOption.objects.get_or_create(order=option.get('order', 1), text=option['text'])
                D.options.add(option_instance.id)

        return D

    def update(self, instance, validated_data):
        print(validated_data)
        instance.key = validated_data.get('key', instance.key)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.datatype = validated_data.get('datatype', instance.datatype)
        instance.pre_unit = validated_data.get('pre_unit', instance.pre_unit)
        instance.post_unit = validated_data.get('post_unit', instance.post_unit)
        instance.cut_off_lower_limit = validated_data.get('cut_off_lower_limit', instance.cut_off_lower_limit)
        instance.cut_off_upper_limit = validated_data.get('cut_off_upper_limit', instance.cut_off_upper_limit)
    

        # Updates options, required when option order is changed for examples
        if 'options' in validated_data:
            options = validated_data.pop('options')
            instance.options.clear()

            if len(options):
                for option in options:
                    option_instance, _ = AnswerOption.objects.get_or_create(order=option.get('order', 1), text=option['text'])
                    if option_instance.id not in instance.options.all():
                        instance.options.add(option_instance)
        print(instance.topic)
        instance.save()
        return instance

    # Name validation
    def validate_name(self, value):
        if self.instance:
            method_pk = self.instance.method
        else:
            method_pk = self.initial_data['method']

        # if self.instance and self.instance.name == value:
        #     return value
        
        direct_indicator = DirectIndicator.objects.filter(name=value, method=method_pk)

        if direct_indicator.exists():
            if self.instance != direct_indicator.first():
                raise serializers.ValidationError('Name is not unique')

        return value

    # Key validation
    def validate_key(self, value):
        if self.instance:
            method_pk = self.instance.method
        else:
            method_pk = self.initial_data['method']

        # if self.instance and self.instance.key == value:
        #     return value
        
        direct_indicator = DirectIndicator.objects.filter(key=value, method=method_pk)

        if direct_indicator.exists():
            if self.instance != direct_indicator.first():
                raise serializers.ValidationError('Key is not unique')

        return value