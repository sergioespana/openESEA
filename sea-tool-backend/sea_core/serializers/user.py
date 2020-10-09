from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from ..models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        user = super().update(instance, validated_data)
        user.set_password(password)
        user.save()
        return user


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)


class RegisterUserSerializer(UserSerializer):
    organization = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = UserSerializer.Meta.model
        fields = ['email', 'password', 'organization']

    def create(self, validated_data):
        organization = validated_data.pop('organization')
        user = super().create(validated_data)
        user.organizations.create(name=organization)
        return user


class UserTokenSerializer(UserSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        payload = jwt_payload_handler(instance)
        token = jwt_encode_handler(payload)
        return {'token': token, 'user': ret}
