from rest_framework import serializers
from ..models import Survey, StakeholderGroup
from .direct_indicator import DirectIndicatorSerializer


class SurveyOverviewSerializer(serializers.ModelSerializer):
    stakeholder = serializers.CharField(max_length=120)

    class Meta:
        model = Survey
        fields = [
            'id',
            'name',
            'description',
            'rate',
            'anonymous',
            'questions',
            'method',
            'stakeholder',
        ]
        read_only_fields = ['method']

    def update(self, instance, validated_data):
        if 'stakeholder' in validated_data:
            validated_data['stakeholder_group'] = self.update_stakeholder(
                stakeholder_group=instance.stakeholder_group,
                name=validated_data['stakeholder'],
                method=instance.method,
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        internal = {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'rate': instance.rate,
            'anonymous': instance.anonymous,
            'questions': instance.questions,
            'method': instance.method,
            'stakeholder': instance.stakeholder_group,
        }
        return super().to_representation(internal)

    def update_stakeholder(self, stakeholder_group, name, method):
        if len(stakeholder_group.surveys.all()) > 1:
            stakeholder, _ = StakeholderGroup.objects.get_or_create(
                name=name, method=method,
            )
            return stakeholder
        return stakeholder_group.update(name=name)


class SurveyQuestionOptionSerializer(serializers.Serializer):
    text = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)


class SurveySubTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = DirectIndicatorSerializer(many=True)


class SurveyTopicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    questions = DirectIndicatorSerializer(many=True)
    sub_topics = SurveySubTopicSerializer(many=True)


class SurveyDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    method = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    topics = SurveyTopicSerializer(many=True)

    def to_representation(self, instance):
        direct_indicators = instance.questions.all()
        topics = {}
        sub_topics = {}

        for direct_indicator in direct_indicators:
            topic_list = topics
            topic = direct_indicator.topic

            if topic.parent_topic:
                topic_list = sub_topics

            if topic.name not in topic_list.keys():
                topic_list[topic.name] = {
                    'id': topic.id,
                    'name': topic.name,
                    'description': topic.description,
                    'parent_topic': topic.parent_topic,
                    'questions': [direct_indicator],
                    'sub_topics': [],
                }
            else:
                topic_list[topic.name]['questions'].append(direct_indicator)

        for _, sub_topic in sub_topics.items():
            parent = sub_topic['parent_topic']
            if parent.name not in topics:
                topics[parent.name] = {
                    'id': parent.id,
                    'name': parent.name,
                    'description': parent.description,
                    'questions': [],
                    'sub_topics': [],
                }

            sub_topic['parent_topic'] = sub_topic['parent_topic'].name
            parent = sub_topic['parent_topic']
            if 'sub_topics' in topics[parent]:
                topics[parent]['sub_topics'].append(sub_topic)
            else:
                topics[parent] = {
                    **topics[parent],
                    'sub_topics': [sub_topic],
                }

        topic_list = []
        for _, topic in topics.items():
            topic_list.append(topic)

        return super().to_representation(
            {
                'id': instance.id,
                'name': instance.name,
                'description': instance.description,
                'method': instance.method,
                'topics': topic_list,
            }
        )
