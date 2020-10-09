from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from ..models import Method, Organization
from ..serializers import MethodSerializer


class MethodViewSet(viewsets.ModelViewSet):
    serializer_class = MethodSerializer

    def get_queryset(self):
        return Method.objects.filter(
            organization=self.kwargs['organization_pk'],
            organization__user=self.request.user,
        )

    def perform_create(self, serializer):
        organization = get_object_or_404(
            Organization, pk=self.kwargs['organization_pk'],
        )
        serializer.save(organization=organization)
