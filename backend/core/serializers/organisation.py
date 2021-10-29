from rest_framework import serializers
from ..models import Organisation, OrganisationMember, CustomUser, Network


class OrganisationSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    created_by_id = serializers.ReadOnlyField(source='created_by.id')
    owner = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username', required=False)
    owner_id = serializers.ReadOnlyField(source='owner.id')
    
    esea_accounts = serializers.StringRelatedField(read_only=True, many=True)
    networks = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all(), many=True, required=False)

    class Meta:
        model = Organisation
        fields = ['id', 'ispublic', 'name', 'description', 'image', 'owner', 'owner_id', 'created_by', 'created_by_id', 'networks', 'esea_accounts']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user=self.context['request'].user

        # Sets acces level of user to the organisation
        if user.is_superuser:
            representation['accesLevel'] = "admin"
        else:
            try:
                member = OrganisationMember.objects.get(organisation=instance, user=user)
            except OrganisationMember.DoesNotExist:
                member = None
            
            if member:
                representation['accesLevel'] = member.get_role_display()
        return representation