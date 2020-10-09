from rest_framework import serializers
from ..models import Method


class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = '__all__'
        read_only_fields = ['organization']
