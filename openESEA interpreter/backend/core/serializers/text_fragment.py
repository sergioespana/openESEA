from rest_framework import serializers

from ..models import TextFragment


class TextFragmentSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TextFragment
        fields = ['id', 'section', 'order', 'text']