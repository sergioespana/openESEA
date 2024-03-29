from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Survey, Method, Organisation, SurveyResponse, DirectIndicator, StakeholderGroup
from ..serializers import SurveyDisplaySerializer


class BaseModelViewSet(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = ''
    permission_classes = (IsAuthenticated,)

    # Refer to https://stackoverflow.com/a/35987077/1677041
    permission_classes_by_action = {
        'create': permission_classes,
        'list': permission_classes,
        'retrieve': permission_classes,
        'update': permission_classes,
        'destroy': permission_classes,
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get('permission_classes')
            else:
                permission_classes = None

            return [permission() for permission in (permission_classes or self.permission_classes)]


class SurveyViewSet(BaseModelViewSet):
    authentication_classes = []
    serializer_class = SurveyDisplaySerializer # SurveyOverviewSerializer
    permission_classes_by_action = {
        'create': (AllowAny,),
        'list': (AllowAny,),                # Should be isAuthenticated, need to find a way to access retrieve survey with an unauthenticated user, and list with authenticated user!
        'retrieve': (AllowAny,),
        'update': (AllowAny,),
        'destroy': (AllowAny,),
        'all': (IsAuthenticated,)
    }
    permission_classes = [AllowAny,]

    def get_queryset(self):
        '''
        organisation = self.request.GET.get('organisation', None)
        completedbyorganisation = self.request.GET.get('completedbyorganisation', None)
        esea_account = self.request.GET.get('esea-account', None)
        
        if esea_account is not None:
            return Survey.objects.all()
        if organisation or completedbyorganisation is not None:
            try:
                org = Organisation.objects.get(id=organisation or completedbyorganisation)
                #print(userorganisation)
            except:
                return Survey.objects.none()
            #ids = userorganisation.stakeholdergroups.values_list('id', flat=True)
            #print(ids)
            if organisation:
                return Survey.objects.filter(method=self.kwargs['method_pk'])
                # return Survey.objects.filter(method__networks__organisations=org, stakeholder_groups__pk__in=ids).exclude(responses__in=SurveyResponse.objects.filter(user_organisation=userorganisation, finished=True))
            if completedbyorganisation:
                print('ch')
                return Survey.objects.filter(method__networks__organisations=org) #, stakeholder_groups__pk__in=ids, responses__user_organisation=userorganisation).distinct() #responses__finished=True
        '''
        return Survey.objects.filter(method=self.kwargs['method_pk'])

    def create(self, request, method_pk):
        request.data['method'] = int(method_pk)
        serializer = SurveyDisplaySerializer(data=request.data)   # SurveyOverviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, method_pk, *args, **kwargs):
        request.data['method'] = method_pk

        if 'stakeholdergroup' in request.data.keys():
            cleanedName = request.data['stakeholdergroup'].lower()
            request.data['stakeholdergroup'], _ = StakeholderGroup.objects.get_or_create(name=cleanedName)

        return super().update(request, *args, **kwargs)

    def retrieve(self, request, method_pk, pk):
        print('check')
        survey = get_object_or_404(Survey, pk=pk)
        serializer = SurveyDisplaySerializer(survey) # SurveyDetailSerializer(survey)
        return Response(serializer.data) 