from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404

from ..models import Topic, Method
from ..serializers import TopicSerializer


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(method=self.kwargs['method_pk']) 

    def perform_create(self, serializer):
        method = get_object_or_404(Method, pk=self.kwargs['method_pk'])
        serializer.save(method=method)