from rest_framework import serializers

from ..models import SurveyAudit, CustomUser


class SurveyAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAudit
        fields = ['id', 'account_audit', 'survey', 'created_at', 'finish_date', 'status', 'deadline', 'sample_size', 'sample']
        extra_kwargs = {'sample': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['auditor'] = instance.account_audit.auditor.username
        representation['survey_name'] = instance.survey.name
        representation['survey_type'] = instance.survey.response_type
        # try:
        #     go = SomeModel.objects.get(foo='bar')
        # except SomeModel.DoesNotExist:
        #     go = None
        # d = OrganisationMember.objects.filter(organisation__esea_accounts=instance.esea_account)
        # l = list()
        # for member in d:
        #     l.append(member.user.username)
        # representation['auditors'] = l

        return representation