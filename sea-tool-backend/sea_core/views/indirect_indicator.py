from rest_framework import viewsets
from ..models import IndirectIndicator
from ..serializers import IndirectIndicatorSerializer


class IndirectIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndirectIndicatorSerializer

    def get_queryset(self):
        return IndirectIndicator.objects.filter(
            topic__method__organization__user=self.request.user,
            topic__method__organization=self.kwargs['organization_pk'],
            topic__method=self.kwargs['method_pk'],
        )

    def create(self, request, organization_pk, method_pk):
        request.data['method'] = int(method_pk)
        return super().create(request, organization_pk, method_pk)

    def update(self, request, organization_pk, method_pk, pk):
        request.data['method'] = int(method_pk)
        return super().update(request, organization_pk, method_pk, pk)
