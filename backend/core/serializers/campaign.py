from rest_framework import serializers

from ..models import Campaign, EseaAccount, Method, Network, Respondent, SurveyResponse, Survey
from .esea_account import EseaAccountSerializer
from datetime import datetime
import pytz


class CampaignSerializer(serializers.ModelSerializer):
    organisation_accounts = EseaAccountSerializer(many=True, read_only=True)
    network = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all())
    method = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all())
    method_name = serializers.ReadOnlyField(source='method.name')
    
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'image', 'network', 'method', 'method_name', 'organisation_accounts', 'year', 'open_survey_date', 'close_survey_date', 'close_validation_date']
        depth = 1

    def validate_close_survey_date(self, value):
        try:
            start_date = datetime.strptime(self.initial_data['open_survey_date'], '%Y-%m-%dT%H:%M:%S%z') #.%f
        except:
            start_date = datetime.strptime(self.initial_data['open_survey_date'], '%Y-%m-%dT%H:%M:%S.%f%z')

        if start_date > value:
            raise serializers.ValidationError('Closing date must be after Opening date.')

        return value

    def validate_close_validation_date(self, value):
        try:
            close_date = datetime.strptime(self.initial_data['close_survey_date'], '%Y-%m-%dT%H:%M:%S%z') #.%f
        except:
            close_date = datetime.strptime(self.initial_data['close_survey_date'], '%Y-%m-%dT%H:%M:%S.%f%z')
        
        if close_date > value:
            raise serializers.ValidationError('Campaign must be closed before closing the validation period')
        
        return value