from rest_framework.test import (
    APIRequestFactory,
    force_authenticate,
    APITestCase,
)
from rest_framework import status
from sea_core.models import User
from sea_core.views.survey_response import SurveyResponseViewset


class SurveyResponseTestCase(APITestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.get(email="test@test.test")

    # ENDPOINTS
    def test_calculate_valid(self):
        request = self.factory.get("")
        view = SurveyResponseViewset.as_view({"get": "calculations"})
        force_authenticate(request, user=self.user)
        response = view(
            request, organization_pk=4, method_pk=4, survey_pk=8, pk=3
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
