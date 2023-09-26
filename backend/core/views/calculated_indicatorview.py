from rest_framework import viewsets
from rest_framework.response import Response

from ..models import IndirectIndicator, DirectIndicator, EseaAccount, QuestionResponse
from ..serializers import IndirectIndicatorSerializer, DirectIndicatorSerializer2, EseaAccountSerializer, QuestionResponseSerializer

class CalculatedIndicatorViewSet(viewsets.ModelViewSet):
    
    def list(self, *args, **kwargs):
        # Get organisation and method from request
        organisation = self.kwargs.get('organisation_pk')
        method = self.kwargs.get('method_pk')

        # Collect values for indicators
        indicatorValues = self.collectIndicatorValues(organisation, method)

        # Create a custom data object
        custom_data = {"value": 100, "key": 0}

        # Return the custom data as a response
        return Response(data = custom_data, status = 200)

    def collectIndicatorValues(self, organisation, method):
        
        # List all corresponding indicator objects
        indirectIndicatorObjects = list(IndirectIndicator.objects.filter(method = method))
        directIndicatorObjects = list(DirectIndicator.objects.filter(method = method))
        
        # Serialize objects into data
        directIndicators = [DirectIndicatorSerializer2(directIndicator).data for directIndicator in directIndicatorObjects]
        indirectIndicators = [IndirectIndicatorSerializer(indirectIndicator).data for indirectIndicator in indirectIndicatorObjects]

        # List all esea accounts
        eseaAccountObjects = list(EseaAccount.objects.filter(organisation = organisation, method = method))

        # Serialize objects into data
        eseaAccounts = [EseaAccountSerializer(eseaAccount).data for eseaAccount in eseaAccountObjects]

        # # Get question responses 
        # questionResponseObjects = list(QuestionResponse.objects.filter(organisation = organisation))

        # # Serialize objects into data
        # questionResponses = [QuestionResponseSerializer(questionResponse).data for questionResponse in questionResponseObjects]

        print(directIndicators, indirectIndicators, eseaAccounts)
        return []

