from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Campaign
from ..serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        # May be removed if nothing is affected by this
        # if  int(self.kwargs['network_pk']) == 0:
        #     return Campaign.objects.all()
        return Campaign.objects.filter(network=int(self.kwargs['network_pk']))

    def create(self, request, network_pk):
        request.data['network'] = int(network_pk)
        serializer = CampaignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, network_pk, *args, **kwargs):
        request.data['network'] = network_pk
        return super().update(request, *args, **kwargs)