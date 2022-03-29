from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404

from ..models import Organisation
from ..serializers import OrganisationSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
   
    def get_queryset(self):

        myorganisations = self.request.GET.get('myorganisations', None)
        allorganisations = self.request.GET.get('allorganisations', None)
        network = self.request.GET.get('network', None)
        excludenetwork = self.request.GET.get('excludenetwork', None)
        method = self.request.GET.get('method', None)
        excludemethod = self.request.GET.get('excludemethod', None)
        campaign = self.request.GET.get('campaign', None)
        excludecampaign = self.request.GET.get('excludecampaign', None)

        if myorganisations is not None:
            return Organisation.objects.filter(teammembers__user=self.request.user)
        if allorganisations is not None:
            if self.request.user.is_superuser:
                return Organisation.objects.all()
            else:
                orgs = Organisation.objects.filter(Q(teammembers__user=self.request.user) | Q(ispublic = True)).distinct()
                return orgs
        if (network is not None) and (excludecampaign is not None):
            return Organisation.objects.filter(networks=network).exclude(esea_accounts__campaign=excludecampaign)
        if network is not None:
            if method is not None:
                return Organisation.objects.filter(networks=network, esea_accounts=method).distinct()
            if excludemethod is not None:
                return Organisation.objects.filter(networks=network).exclude(esea_accounts=excludemethod)
            return Organisation.objects.filter(networks=network)
        if excludenetwork is not None:
            return Organisation.objects.exclude(Q(networks=excludenetwork) | Q(network_requests__network=excludenetwork))
        if campaign is not None:
            return Organisation.objects.filter(esea_accounts__campaign=campaign)
        return Organisation.objects.all()
    
    def create(self, request, ):
        serializer = OrganisationSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data)