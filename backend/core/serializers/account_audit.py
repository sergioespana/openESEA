from rest_framework import serializers

from ..models import AccountAudit, CustomUser
from .survey_audit import SurveyAuditSerializer

class AccountAuditSerializer(serializers.ModelSerializer):
    auditor = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    # auditor = serializers.StringRelatedField(read_only=True)
    # auditor = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), querywrite_only=True)
    survey_audits = SurveyAuditSerializer(many=True, required=False, read_only=True)


    class Meta:
        model = AccountAudit
        fields = ['id', 'auditor', 'created_at', 'finish_date', 'assurance', 'assurance_declaration', 'status', 'esea_account', 'survey_audits']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['organisation'] = instance.esea_account.organisation.name
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