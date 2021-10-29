from rest_framework import serializers
from ..models import Survey, StakeholderGroup

from .section import SectionSerializer


class SurveyDisplaySerializer(serializers.ModelSerializer):
    method_name = serializers.ReadOnlyField(source='method.name')
    response_type = serializers.ChoiceField(choices=Survey.RESPONSE_TYPES)
    stakeholdergroup = serializers.SlugRelatedField(queryset=StakeholderGroup.objects.all(), slug_field="name", required=False)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'method', 'method_name', 'name', 'description', 'response_type', 'min_threshold', 'anonymous', 'stakeholdergroup', 'welcome_text', 'closing_text', 'sections']