from rest_framework import serializers

from ..models import QuestionResponse, AnswerOption, DirectIndicator


class QuestionResponseSerializer(serializers.ModelSerializer):
    values = serializers.SlugRelatedField(queryset=AnswerOption.objects.all(), many=True, slug_field='text')
    # direct_indicator_key = serializers.StringRelatedField(source='question.direct_indicator')
    
    class Meta:
        model = QuestionResponse
        fields = ['id', 'question', 'direct_indicator_id', 'values', 'value', 'auditstatus', 'doc_request_note', 'doc_upload_note', 'note']

    # Validates whether the question response is of the correct datatype (unfinished)
    def validate(self, data):
        value = data['value']
        if value:
            if data["direct_indicator_id"] > 0: 
                Di = DirectIndicator.objects.get(id=data["direct_indicator_id"])

                if Di.datatype == 'integer':
                    try:
                        int(value)
                    except:
                        raise serializers.ValidationError('Question response should be of type integer')

                if Di.datatype == 'double':
                    try:
                        float(value)
                    except:
                        raise serializers.ValidationError('Question response should be of type double')

                if Di.datatype == 'date':
                    pass
                    # print('is it a date?')
                    # try:
                    # except:

                if Di.datatype in ['boolean', 'singlechoice']:
                    pass
                    # print('Is only one value returned?')
                    # try:
                    # except:

                if Di.datatype == 'multiplechoice':
                    pass
                    # print('is a list of QuestionOptions returned?')
                    # try:
                    # except:

        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Required because direct indicator-question is not a one to one relationship!
        representation['direct_indicator_key'] = instance.question.direct_indicator.first().key
        return representation
