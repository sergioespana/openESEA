from rest_framework import viewsets
from rest_framework.response import Response

from ..models import OrganisationMember, Organisation, Respondent
from ..serializers import OrganisationMemberSerializer


class OrganisationMemberViewSet(viewsets.ModelViewSet):
    serializer_class=OrganisationMemberSerializer

    def get_queryset(self):
        return OrganisationMember.objects.filter(organisation=int(self.kwargs['organisation_pk']))

    def create(self, request, organisation_pk):
        request.data['organisation'] = int(organisation_pk)
        serializer = OrganisationMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def update(self, request, organisation_pk, *args, **kwargs):
        request.data['organisation'] = organisation_pk
        instance = self.get_object()
        organisation = Organisation.objects.get(id=organisation_pk)

        serializer = OrganisationMemberSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Makes sure that only 1 admin exists in the organisation
        if request.data['role'] == 3:
            oldOrganisationAdmins = OrganisationMember.objects.filter(organisation=organisation_pk, role=3).exclude(user=instance.user)
            if len(oldOrganisationAdmins):
                for admin in oldOrganisationAdmins:
                    admin.role = 1
                    admin.save()
                
                organisation.owner = instance.user
                organisation.save()

        # Makes sure that only 1 esea accountant exists in the organisation
        if request.data['role'] == 2:
            oldEseaAccountants = OrganisationMember.objects.filter(organisation=organisation_pk, role=2).exclude(user=instance.user)
            if len(oldEseaAccountants):
                for eseaAccountant in oldEseaAccountants:
                    eseaAccountant.role = 1
                    eseaAccountant.save()
        
        Respondent.objects.get_or_create(organisation=organisation, email="accountant@mail.com", first_name="Accountant", last_name=f"of {organisation.name}")
        return Response(serializer.data)
