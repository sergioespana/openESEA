from rest_framework import serializers

from ..models import Method
from .survey2 import SurveyDisplaySerializer
from .direct_indicator2 import DirectIndicatorSerializer2


class MinimalMethodSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Method
        fields = ('id', 'created_by', 'ispublic', 'name', 'description', 'version', 'certification_theshold', 'surveys', 'topics', 'networks')


class SubTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    parent_topic_name = serializers.StringRelatedField(source='parent_topic', read_only=True)
    questions = serializers.StringRelatedField(many=True)
    direct_indicators = DirectIndicatorSerializer2(read_only=True, many=True)


class TopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = serializers.StringRelatedField(many=True) #serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    direct_indicators = DirectIndicatorSerializer2(read_only=True, many=True)
    sub_topics = SubTopicSerializer(many=True)


class MethodSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    surveys = SurveyDisplaySerializer(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)
    networks = serializers.StringRelatedField(read_only=True, many=True)
    version = serializers.FloatField(required=False)

    class Meta:
        model = Method
        fields = ['id', 'created_by', 'ispublic', 'name', 'description', 'version', 'certification_theshold', 'surveys', 'topics', 'networks']

    # Makes sure the version has a max of 2 decimal points
    def validate_version(self, value):
        value = round(value, 2)
        return value

    # Sets the correct representation of a method with nested Topics
    def to_representation(self, instance):
        mytopics = {}

        for topic in instance.topics.all():
            if topic.parent_topic:
                parent = topic.parent_topic
                if parent.name not in mytopics.keys():
                    mytopics[parent.name] = {
                        'id': parent.id,
                        'name': parent.name,
                        'description': parent.description,
                        'questions': parent.questions,
                        'direct_indicators': parent.direct_indicators,
                        'sub_topics': [],
                    }
                mytopics[parent.name]['sub_topics'].append(
                    {
                        'id': topic.id,
                        'name': topic.name,
                        'description': topic.description,
                        'questions': topic.questions,
                        'direct_indicators': topic.direct_indicators,
                    })
            else:
                if topic.name not in mytopics.keys():
                    mytopics[topic.name] = {
                            'id': topic.id,
                            'name': topic.name,
                            'description': topic.description,
                            'questions': topic.questions,
                            'direct_indicators': topic.direct_indicators,
                            'sub_topics': []
                            }
        
        topic_list = []
        for _, topic in mytopics.items():
            topic_list.append(topic)

        representation = super().to_representation({
            'id': instance.id,
            'created_by': instance.created_by,
            'name': instance.name,
            'ispublic': instance.ispublic,
            'description': instance.description,
            'version': instance.version,
            'certification_theshold': instance.certification_theshold,
            'surveys': instance.surveys,
            'networks': instance.networks,
            'topics': topic_list
        })
        return representation