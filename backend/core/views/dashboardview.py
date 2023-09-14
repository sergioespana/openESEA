from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Dashboard
from ..serializers import DashboardSerializer

class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer

    def get_queryset(self):
        return Dashboard.objects.all()

    def create(self, request):
        data = { 'specification': request.data }
        serializer = DashboardSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk):
        dashboard = get_object_or_404(Dashboard, pk = pk)
        data = { 'specification': request.data }
        serializer = DashboardSerializer(instance = dashboard, data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
