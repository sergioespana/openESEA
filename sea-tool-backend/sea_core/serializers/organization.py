from rest_framework import serializers
from ..models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    methods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'
