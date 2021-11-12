from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from ..serializers import RegisterUserSerializer, UserSerializer
from ..models import CustomUser, Organisation, StakeholderGroup, Respondent, SurveyResponse

import os
import csv
import string
import random


class RegisterUserView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterUserSerializer


class UsersViewSet(viewsets.ModelViewSet): # ReadOnlyModelViewSet ?
    model = CustomUser
    serializer_class = UserSerializer

    def get_queryset(self):
        currentuser = self.request.GET.get('currentuser', None)
        network = self.request.GET.get('network', None)
        excludenetwork = self.request.GET.get('excludenetwork', None)
        organisation = self.request.GET.get('organisation', None)
        excludeorganisation = self.request.GET.get('excludeorganisation', None)

        if currentuser is not None:
            return CustomUser.objects.filter(id=self.request.user.id)
        if network is not None:
            return CustomUser.objects.filter(teams__network=network).distinct()
        if excludenetwork is not None:
            return CustomUser.objects.exclude(teams__network=excludenetwork)
        if organisation is not None:
            return CustomUser.objects.filter(teams__organisation=organisation)
        if excludeorganisation is not None:
            return CustomUser.objects.exclude(organisationteams__organisation=excludeorganisation)
        return CustomUser.objects.all()