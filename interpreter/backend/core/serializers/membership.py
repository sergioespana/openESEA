from rest_framework import serializers

from ..models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
    
    # Adds organisation name & description and network name & description to the JSON representation
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['organisation_name'] = instance.organisation.name
        representation['organisation_description'] = instance.organisation.description
        representation['network_name'] = instance.network.name
        representation['network_description'] = instance.network.description
        return representation