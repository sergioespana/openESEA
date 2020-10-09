from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Organization, User
from ..serializers import (
    OrganizationSerializer,
    UserEmailSerializer,
    UserSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(users=[self.request.user])


class OrganizationUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        # user = self.request.user
        organization_pk = self.kwargs['organization_pk']
        return User.objects.filter(organization=organization_pk)

    def create(self, request, organization_pk):
        """Add a user to a organization"""
        organization = get_object_or_404(Organization, pk=organization_pk)

        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, email=serializer.validated_data['email']
        )
        organization.users.add(user)

        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def update(self, request, organization_pk, pk, partial=False):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, organization_pk, pk):
        """Remove user from organization"""
        organization = get_object_or_404(Organization, pk=organization_pk)

        organization.users.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
