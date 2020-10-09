from rest_framework import viewsets
from django.contrib.auth.models import Group
from ..serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
