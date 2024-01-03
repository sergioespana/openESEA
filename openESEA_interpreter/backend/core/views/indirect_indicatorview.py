from rest_framework import viewsets
from rest_framework.response import Response

from ..models import IndirectIndicator
from ..serializers import IndirectIndicatorSerializer


class IndirectIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndirectIndicatorSerializer

    def get_queryset(self):
        return IndirectIndicator.objects.filter(method=self.kwargs['method_pk'])

    def create(self, request, method_pk):
        request.data['method'] = int(method_pk)
        serializer = IndirectIndicatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)