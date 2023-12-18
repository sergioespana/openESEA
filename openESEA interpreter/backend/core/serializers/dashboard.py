from rest_framework import serializers

from ..models import Dashboard


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ['id', 'specification']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['specification'] = instance.specification
    #     return representation
    