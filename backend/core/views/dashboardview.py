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
        serializer = DashboardSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise e
        finally:
            print('Hello')
            print(request.data)
            print(serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
