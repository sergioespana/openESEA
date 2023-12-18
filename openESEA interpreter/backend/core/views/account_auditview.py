from rest_framework import viewsets
from rest_framework.response import Response

from ..models import AccountAudit, CustomUser
from ..serializers import AccountAuditSerializer


class AccountAuditViewSet(viewsets.ModelViewSet):
    serializer_class=AccountAuditSerializer
    
    def get_queryset(self):
        campaign = self.request.GET.get('campaign', None)
        audit_selection = self.request.GET.get('audit-selection', None)
        if campaign is not None and audit_selection is not None:
            return AccountAudit.objects.filter(esea_account__campaign=campaign, status__in=['in progress', 'finished'])
        return AccountAudit.objects.filter(esea_account=self.kwargs['esea_account_pk'])
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        serializer = AccountAuditSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
